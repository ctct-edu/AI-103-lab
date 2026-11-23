import os
from urllib.request import urlopen, Request
import base64
from pathlib import Path
from dotenv import load_dotenv

# 参照の追加


def main():

    # コンソールをクリア
    os.system('cls' if os.name=='nt' else 'clear')

    try:

        # 構成設定を取得
        load_dotenv()
        openai_endpoint = os.getenv("ENDPOINT")
        model_deployment =  os.getenv("MODEL_DEPLOYMENT")


        # OpenAI クライアントを作成



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



    except Exception as ex:
        print(ex)


if __name__ == '__main__':
    main()
