import os
from urllib.request import urlopen, Request
import base64
from pathlib import Path
from dotenv import load_dotenv

# 参照の追加
from openai import OpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider


def main():

    # コンソールをクリア
    os.system('cls' if os.name=='nt' else 'clear')

    try:

        # 構成設定を取得
        load_dotenv()
        openai_endpoint = os.getenv("ENDPOINT")
        model_deployment =  os.getenv("MODEL_DEPLOYMENT")


        # OpenAI クライアントを作成
        credential = DefaultAzureCredential()
        token_provider = get_bearer_token_provider(credential, "https://ai.azure.com/.default")
        client = OpenAI(
            base_url=openai_endpoint,
            api_key=token_provider()
        )


        # プロンプトを初期化
        system_message = "あなたは果物を販売する食料品店の AI アシスタントです。青果に関する質問に詳しく回答します。"
        prompt = ""

        # ユーザーが 'quit' と入力するまでループ
        while True:
            prompt = input("\n画像について質問してください\n('quit' と入力すると終了します)\n")
            if prompt.lower() == "quit":
                break
            elif len(prompt) == 0:
                    print("質問を入力してください。\n")
            else:
                print("応答を取得しています ...\n")


                # 画像入力に対する応答を取得
                image_url = "https://microsoftlearning.github.io/mslearn-ai-vision/Labfiles/gen-ai-vision/orange.jpeg"
                response = client.responses.create(
                    model=model_deployment,
                    input=[
                        {"role": "developer", "content": system_message},
                        { "role": "user", "content": [
                            { "type": "input_text", "text": prompt},
                            { "type": "input_image", "image_url": image_url}
                        ]}
                    ]
                )
                print(response.output_text)


    except Exception as ex:
        print(ex)


if __name__ == '__main__':
    main()
