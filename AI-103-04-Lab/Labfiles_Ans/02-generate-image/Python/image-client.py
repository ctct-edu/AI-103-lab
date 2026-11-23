import os
import json

# 参照の追加
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from openai import OpenAI
import requests
import base64


def main():

    # コンソールをクリア
    os.system('cls' if os.name=='nt' else 'clear')

    try:

        # 構成設定を取得
        load_dotenv()
        endpoint = os.getenv("ENDPOINT")
        model_deployment =  os.getenv("MODEL_DEPLOYMENT")

        # クライアントを初期化
        token_provider = get_bearer_token_provider(
            DefaultAzureCredential(exclude_environment_credential=True,
                exclude_managed_identity_credential=True),
            "https://cognitiveservices.azure.com/.default"
        )

        client = OpenAI(
            base_url=endpoint,
            api_key=token_provider(),
        )


        img_no = 0
        # ユーザーが 'quit' と入力するまでループ
        while True:
            # 入力テキストを取得
            input_text = input("プロンプトを入力してください ('quit' で終了): ")
            if input_text.lower() == "quit":
                break
            if len(input_text) == 0:
                print("プロンプトを入力してください。")
                continue

            # 画像を生成
            img = client.images.generate(
                model=model_deployment,
                prompt=input_text,
                n=1
            )

            json_response = json.loads(img.model_dump_json())
            image_data = json_response["data"][0].get("b64_json")
            image_data_in_bytes = base64.b64decode(image_data)

            # 画像を保存
            img_no += 1
            file_name = f"image_{img_no}.png"
            save_image(image_data_in_bytes, file_name)


    except Exception as ex:
        print(ex)

def save_image (image_data, file_name):
    # 保存する画像のディレクトリを設定
    image_dir = os.path.join(os.getcwd(), 'images')

    # ディレクトリが存在しない場合は作成
    if not os.path.isdir(image_dir):
        os.mkdir(image_dir)

    # 画像のパスを初期化 (ファイルの種類は png にします)
    image_path = os.path.join(image_dir, file_name)

    # 生成された画像を保存
    with open(image_path, "wb") as image_file:
        image_file.write(image_data)
    print (f"画像を保存しました: {image_path}")


if __name__ == '__main__':
    main()
