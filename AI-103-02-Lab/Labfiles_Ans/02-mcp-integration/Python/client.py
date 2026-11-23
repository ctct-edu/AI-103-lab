import os
import asyncio
import json
from dotenv import load_dotenv
from contextlib import AsyncExitStack
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import FunctionTool
from azure.identity import DefaultAzureCredential
from azure.ai.projects.models import PromptAgentDefinition, FunctionTool
from openai.types.responses.response_input_param import FunctionCallOutput, ResponseInputParam

# 参照の追加
# 参照の追加
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# コンソールをクリア
os.system('cls' if os.name=='nt' else 'clear')

# .env ファイルから環境変数を読み込む
load_dotenv()
project_endpoint = os.getenv("PROJECT_ENDPOINT")
model_deployment = os.getenv("MODEL_DEPLOYMENT_NAME")

async def connect_to_server(exit_stack: AsyncExitStack):
    server_params = StdioServerParameters(
        command="python",
        args=["server.py"],
        env=None
    )

    # MCP サーバーを起動
    # MCP サーバーを起動
    stdio_transport = await exit_stack.enter_async_context(stdio_client(server_params))
    stdio, write = stdio_transport

    # MCP クライアント セッションを作成
    # MCP クライアント セッションを作成
    session = await exit_stack.enter_async_context(ClientSession(stdio, write))
    await session.initialize()

    # 利用可能なツールを一覧表示
    # 利用可能なツールを一覧表示
    response = await session.list_tools()
    tools = response.tools
    print("\nConnected to server with tools:", [tool.name for tool in tools]) 



    return session

async def chat_loop(session):

    # エージェント クライアントに接続
    with (
        DefaultAzureCredential() as credential,
        AIProjectClient(endpoint=project_endpoint, credential=credential) as project_client,
        project_client.get_openai_client() as openai_client,
    ):

        # サーバーから利用可能な MCP ツールを取得
        response = await session.list_tools()
        tools = response.tools

        # 各ツールの関数を構築
        # 各ツールの関数を構築
        def make_tool_func(tool_name):
            async def tool_func(**kwargs):
                result = await session.call_tool(tool_name, kwargs)
                return result
            
            tool_func.__name__ = tool_name
            return tool_func

        # 関数呼び出し処理時にアクセスしやすいよう関数を辞書に格納
        functions_dict = {tool.name: make_tool_func(tool.name) for tool in tools}

        # エージェント用の FunctionTool 定義を作成
        # エージェント用の FunctionTool 定義を作成
        mcp_function_tools: FunctionTool = []
        for tool in tools:
            function_tool = FunctionTool(
                name=tool.name,
                description=tool.description,
                parameters={
                    "type": "object",
                    "properties": {},
                    "additionalProperties": False,
                },
                strict=True
            )
            mcp_function_tools.append(function_tool)

        # エージェントを作成
        # エージェントを作成
        agent = project_client.agents.create_version(
            agent_name="inventory-agent",
            definition=PromptAgentDefinition(
                model=model_deployment,
                instructions="""
                あなたは在庫アシスタントです。以下の一般的なガイドラインに従ってください:
                - 在庫が 10 未満かつ週間販売数が 15 以上の場合は補充を推奨
                - 在庫が 20 超かつ週間販売数が 5 未満の場合はクリアランスを推奨
                """,
                tools=mcp_function_tools
            ),
        )

        # チャット セッション用のスレッドを作成
        conversation = openai_client.conversations.create()

        # モデルに送り返す関数呼び出し出力を保持する入力リストを作成
        input_list: ResponseInputParam = []

        while True:
            user_input = input("在庫エージェントへのプロンプトを入力してください。終了するには 'quit' を入力します。\nUSER: ").strip()
            if user_input.lower() == "quit":
                print("チャットを終了します。")
                break

            # エージェントにプロンプトを送信
            openai_client.conversations.items.create(
                conversation_id=conversation.id,
                items=[{"type": "message", "role": "user", "content": user_input}],
            )

            # エージェントの応答を取得（MCP サーバー ツールへの関数呼び出しが含まれる場合あり）
            response = openai_client.responses.create(
                conversation=conversation.id,
                extra_body={"agent_reference": {"name": agent.name, "type": "agent_reference"}},
                input=input_list,
            )

            # 実行ステータスのエラーを確認
            if response.status == "failed":
                print(f"Response failed: {response.error}")

            # 関数呼び出しを処理
            # 関数呼び出しを処理
            for item in response.output:
                if item.type == "function_call":
                    # 対応する関数ツールを取得
                    function_name = item.name
                    kwargs = json.loads(item.arguments)
                    required_function = functions_dict.get(function_name)

                    # 関数を呼び出す
                    output = await required_function(**kwargs)

                    # 出力テキストを追加
                    input_list.append(
                    FunctionCallOutput(
                        type="function_call_output",
                        call_id=item.call_id,
                        output=output.content[0].text,
                    )
                    )

            # 関数呼び出しの出力をモデルに返して応答を取得
            # 関数呼び出しの出力をモデルに返して応答を取得
            if input_list:
                response = openai_client.responses.create(
                    input=input_list,
                    previous_response_id=response.id,
                    extra_body={"agent_reference": {"name": agent.name, "type": "agent_reference"}},
                )
            print(f"Agent response: {response.output_text}")


        # 完了後にエージェントを削除
        print("エージェントをクリーンアップしています:")
        project_client.agents.delete_version(agent_name=agent.name, agent_version=agent.version)
        print("在庫エージェントを削除しました。")


async def main():
    import sys
    exit_stack = AsyncExitStack()
    try:
        session = await connect_to_server(exit_stack)
        await chat_loop(session)
    finally:
        await exit_stack.aclose()

if __name__ == "__main__":
    asyncio.run(main())
