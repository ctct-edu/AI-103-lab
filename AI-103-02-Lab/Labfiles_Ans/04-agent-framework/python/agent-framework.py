import os
import asyncio
from pathlib import Path
from dotenv import load_dotenv

# 参照の追加
# 参照の追加
from agent_framework import tool, Agent
from agent_framework_foundry import FoundryChatClient
from azure.identity import AzureCliCredential
from pydantic import Field
from typing import Annotated


async def main():
    # .env ファイルの設定を読み込む
    load_dotenv()

    # コンソールをクリア
    os.system('cls' if os.name=='nt' else 'clear')

    # 経費データ ファイルを読み込む
    script_dir = Path(__file__).parent
    file_path = script_dir / 'data.txt'
    with file_path.open('r') as file:
        data = file.read() + "\n"

    # プロンプトを入力してもらう
    user_prompt = input(f"ファイル内の経費データは次のとおりです:\n\n{data}\n\nどのように処理しますか?\n\n")

    # 非同期エージェント コードを実行
    await process_expenses_data(user_prompt, data)

async def process_expenses_data(prompt, expenses_data):
    project_endpoint = os.getenv("PROJECT_ENDPOINT")
    model_deployment = os.getenv("MODEL_DEPLOYMENT_NAME")

    # クライアントを作成し、ツールと手順でエージェントを初期化
    # クライアントを作成し、ツールと手順でエージェントを初期化
    credential = AzureCliCredential()
    async with (
        Agent(
            client=FoundryChatClient(
                credential=credential,
                model=model_deployment,
                project_endpoint=project_endpoint,
            ),
            instructions="""あなたは経費請求提出のための AI アシスタントです。
                        ユーザーのリクエストに応じて経費請求書を作成し、プラグイン関数を使用して件名「Expense Claim」、本文に明細と合計を含むメールを expenses@contoso.com に送信してください。
                        送信後はユーザーに完了を確認してください。ユーザーに追加情報を求めず、提供されたデータだけを使用してメールを作成してください。""",
            tools=[submit_claim],
        ) as agent,
    ):

        # エージェントを使用して経費データを処理
        # エージェントを使用して経費データを処理
        try:
            # 送信するメッセージのリストに入力プロンプトを追加
            prompt_messages = [f"{prompt}: {expenses_data}"]
            # メッセージを使用してエージェントを呼び出す
            response = await agent.run(prompt_messages)
            # 応答を表示
            print(f"\n# Agent:\n{response}")
        except Exception as e:
            # エラーが発生しました
            print (e)


# メール機能のツール関数を作成
# メール機能のツール関数を作成
@tool(approval_mode="never_require")
def submit_claim(
    to: Annotated[str, Field(description="Who to send the email to")],
    subject: Annotated[str, Field(description="The subject of the email.")],
    body: Annotated[str, Field(description="The text body of the email.")]):
        print("\nTo:", to)
        print("Subject:", subject)
        print(body, "\n")


if __name__ == "__main__":
    asyncio.run(main())
