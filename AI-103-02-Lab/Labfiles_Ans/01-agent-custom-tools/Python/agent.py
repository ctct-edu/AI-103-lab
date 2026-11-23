import os
import json
from dotenv import load_dotenv

# 参照の追加
# 参照の追加
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import FunctionTool
from azure.identity import DefaultAzureCredential
from azure.ai.projects.models import PromptAgentDefinition, FunctionTool
from openai.types.responses.response_input_param import FunctionCallOutput, ResponseInputParam
from functions import next_visible_event, calculate_observation_cost, generate_observation_report

def main():
    # コンソールをクリア
    os.system('cls' if os.name=='nt' else 'clear')

    # .env ファイルから環境変数を読み込む
    load_dotenv()
    project_endpoint = os.getenv("PROJECT_ENDPOINT")
    model_deployment = os.getenv("MODEL_DEPLOYMENT_NAME")

    # プロジェクト クライアントに接続
    # プロジェクト クライアントに接続
    with (
        DefaultAzureCredential() as credential,
        AIProjectClient(endpoint=project_endpoint, credential=credential) as project_client,
        project_client.get_openai_client() as openai_client,
    ):

        # イベント関数ツールを定義
        # イベント関数ツールを定義
        event_tool = FunctionTool(
            name="next_visible_event",
            description="Get the next visible event in a given location.",
            parameters={
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "continent to find the next visible event in (e.g. 'north_america', 'south_america', 'australia')",
                    },
                },
                "required": ["location"],
                "additionalProperties": False,
            },
            strict=True,
        )

        # 観測コスト計算関数ツールを定義
        # 観測コスト計算関数ツールを定義
        cost_tool = FunctionTool(
            name="calculate_observation_cost",
            description="Calculate the cost of an observation based on the telescope tier, number of hours, and priority level.",
            parameters={
                "type": "object",
                "properties": {
                    "telescope_tier": {
                        "type": "string",
                        "description": "the tier of the telescope (e.g. 'standard', 'advanced', 'premium')",
                    },
                    "hours": {
                        "type": "number",
                        "description": "the number of hours for the observation",
                    },
                    "priority": {
                        "type": "string",
                        "description": "the priority level of the observation (e.g. 'low', 'normal', 'high')",
                    },
                },
                "required": ["telescope_tier", "hours", "priority"],
                "additionalProperties": False,
            },
            strict=True,
        )

        # 観測レポート生成関数ツールを定義
        # 観測レポート生成関数ツールを定義
        report_tool = FunctionTool(
        name="generate_observation_report",
        description="Generate a report summarizing an astronomical observation",
        parameters={
            "type": "object",
            "properties": {
                "event_name": {
                    "type": "string",
                    "description": "the name of the astronomical event being observed",
                },
                "location": {
                    "type": "string",
                    "description": "the location of the observer",
                },
                "telescope_tier": {
                    "type": "string",
                    "description": "the tier of the telescope used for the observation (e.g. 'standard', 'advanced', 'premium')",
                },
                "hours": {
                    "type": "number",
                    "description": "the number of hours the telescope was used for the observation",
                },
                "priority": {
                    "type": "string",
                    "description": "the priority level of the observation (e.g. 'low', 'normal', 'high')",
                },
                "observer_name": {
                    "type": "string",
                    "description": "the name of the person who conducted the observation",
                },                   
            },
            "required": ["event_name", "location", "telescope_tier", "hours", "priority", "observer_name"],
            "additionalProperties": False,
        },
        strict=True,
        )

        # 関数ツールを使用して新しいエージェントを作成
        # 関数ツールを使用して新しいエージェントを作成
        agent = project_client.agents.create_version(
        agent_name="astronomy-agent",
        definition=PromptAgentDefinition(
            model=model_deployment,
            instructions=
                """You are an astronomy observations assistant that helps users find 
                information about astronomical events and calculate telescope rental costs. 
                Use the available tools to assist users with their inquiries.""",
            tools=[event_tool, cost_tool, report_tool],
        ),
        )

        # チャット セッション用のスレッドを作成
        # チャット セッション用のスレッドを作成
        conversation = openai_client.conversations.create()

        # エージェントに送り返す関数呼び出し出力のリストを作成
        # エージェントに送り返す関数呼び出し出力のリストを作成
        input_list: ResponseInputParam = []

        while True:
            user_input = input("天文学エージェントへのプロンプトを入力してください。終了するには 'quit' を入力します。\nUSER: ").strip()
            if user_input.lower() == "quit":
                print("チャットを終了します。")
                break

            # エージェントにプロンプトを送信
            # エージェントにプロンプトを送信
            openai_client.conversations.items.create(
                conversation_id=conversation.id,
                items=[{"type": "message", "role": "user", "content": user_input}],
            )

            # エージェントの応答を取得（関数呼び出しが含まれる場合あり）
            # エージェントの応答を取得（関数呼び出しが含まれる場合あり）
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
                    # Retrieve the matching function tool
                    function_name = item.name
                    result = None
                    if item.name == "next_visible_event":
                        result = next_visible_event(**json.loads(item.arguments))
                    elif item.name == "calculate_observation_cost":
                        result = calculate_observation_cost(**json.loads(item.arguments))
                    elif item.name == "generate_observation_report":
                        result = generate_observation_report(**json.loads(item.arguments))
                        
                    # 出力テキストを追加
                    input_list.append(
                        FunctionCallOutput(
                            type="function_call_output",
                            call_id=item.call_id,
                            output=result,
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
            # エージェントの応答を表示
            print(f"AGENT: {response.output_text}")

        # 完了後にエージェントを削除
        # 完了後にエージェントを削除
        project_client.agents.delete_version(agent_name=agent.name, agent_version=agent.version)
        print("Deleted agent.")

if __name__ == '__main__':
    main()
