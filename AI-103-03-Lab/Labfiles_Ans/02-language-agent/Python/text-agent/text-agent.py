from dotenv import load_dotenv
import os

# 名前空間のインポート
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient


def main():
    try:
        # コンソールをクリア
        os.system('cls' if os.name == 'nt' else 'clear')

        # 構成設定を取得
        load_dotenv()
        foundry_endpoint = os.getenv('FOUNDRY_ENDPOINT')
        agent_name = os.getenv('AGENT_NAME')

        # プロジェクト クライアントを取得
        project_client = AIProjectClient(
            endpoint=foundry_endpoint,
            credential=DefaultAzureCredential(),
        )


        # OpenAI クライアントを取得
        openai_client = project_client.get_openai_client()


        # エージェントを使用して応答を取得
        prompt = input("ユーザー プロンプト: ")
        response = openai_client.responses.create(
            input=[{"role": "user", "content": prompt}],
            extra_body={"agent_reference": {"name": agent_name, "type": "agent_reference"}},
        )

        # ツールの承認待ち (mcp_approval_request) の場合は、承認の応答を返して続行
        for _ in range(5):
            approval_requests = [item for item in response.output if item.type == "mcp_approval_request"]
            if not approval_requests:
                break
            response = openai_client.responses.create(
                previous_response_id=response.id,
                input=[{"type": "mcp_approval_response", "approval_request_id": request.id, "approve": True} for request in approval_requests],
                extra_body={"agent_reference": {"name": agent_name, "type": "agent_reference"}},
            )

        print(f"{agent_name}: {response.output_text}")
        print(f"\n応答の詳細: {response.model_dump_json(indent=2)}")


    except Exception as ex:
        print(ex)

if __name__ == "__main__":
    main()
