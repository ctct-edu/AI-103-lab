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


        # メイン ループ
        while True:
            # ユーザー入力を取得
            prompt = input("ユーザー プロンプト（終了するには 'quit'）: ")
            if prompt == "quit" or len(prompt) == 0:
                break
            else:
                # エージェントを使用して応答を取得
                response = openai_client.responses.create(
                    input=[{"role": "user", "content": prompt}],
                    extra_body={"agent_reference": {"name": agent_name, "type": "agent_reference"}},
                )

                print(f"{agent_name}: {response.output_text}")


    except Exception as ex:
        print(ex)

if __name__ == "__main__":
    main()
