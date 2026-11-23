import os
from dotenv import load_dotenv

# 参照の追加
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition, MCPTool, Reasoning
from openai.types.responses.response_input_param import McpApprovalResponse, ResponseInputParam

# .env ファイルから環境変数を読み込む
load_dotenv()
project_endpoint = os.getenv("PROJECT_ENDPOINT")
model_deployment = os.getenv("MODEL_DEPLOYMENT_NAME")

# gpt-5-mini は reasoning モデルのため、reasoning トークン消費で可視の回答が
# 空になることがある。effort="low" を指定すると TPM=1000 でも安定して動作する。
# (agent_reference 使用時は responses.create() 側に reasoning を渡すと
#  "Not allowed when agent is specified" で拒否されるため、エージェント定義側で指定する)
REASONING_EFFORT = "low"

# エージェント クライアントに接続
with (
    DefaultAzureCredential() as credential,
    AIProjectClient(endpoint=project_endpoint, credential=credential) as project_client,
    project_client.get_openai_client() as openai_client,
):

    # エージェント MCP ツールを初期化
    mcp_tool = MCPTool(
        server_label="api-specs",
        server_url="https://learn.microsoft.com/api/mcp",
        require_approval="always",
    )

    # MCP ツールを使用して新しいエージェントを作成
    agent = project_client.agents.create_version(
        agent_name="MyAgent",
        definition=PromptAgentDefinition(
            model=model_deployment,
            instructions="あなたは MCP ツールを使用してユーザーを支援するエージェントです。利用可能な MCP ツールを使用して質問に答え、タスクを実行してください。",
            tools=[mcp_tool],
            reasoning=Reasoning(effort=REASONING_EFFORT),
        ),
    )
    print(f"Agent created (id: {agent.id}, name: {agent.name}, version: {agent.version})")

    # 会話スレッドを作成
    conversation = openai_client.conversations.create()
    print(f"Created conversation (id: {conversation.id})")

    # MCP ツールをトリガーする初回リクエストを送信
    response = openai_client.responses.create(
        conversation=conversation.id,
        input="Give me the Azure CLI commands to create an Azure Container App with a managed identity.",
        extra_body={"agent_reference": {"name": agent.name, "type": "agent_reference"}},
    )

    # MCP 承認リクエストが無くなるまでラウンドを繰り返す
    # (承認 → mcp_call → さらに承認、のように複数ラウンドになることがあるため)
    while True:
        # 生成された MCP 承認リクエストを処理
        input_list: ResponseInputParam = []
        for item in response.output:
            if item.type == "mcp_approval_request":
                if item.server_label == "api-specs" and item.id:
                    # エージェントが続行できるよう MCP リクエストを自動承認
                    input_list.append(
                        McpApprovalResponse(
                            type="mcp_approval_response",
                            approve=True,
                            approval_request_id=item.id,
                        )
                    )

        if not input_list:
            break

        # 承認応答を返して応答を取得
        response = openai_client.responses.create(
            input=input_list,
            previous_response_id=response.id,
            extra_body={"agent_reference": {"name": agent.name, "type": "agent_reference"}},
        )

    print(f"\nAgent response: {response.output_text}")

    # エージェント バージョンを削除してリソースをクリーンアップ
    project_client.agents.delete_version(agent_name=agent.name, agent_version=agent.version)
    print("Agent deleted")
