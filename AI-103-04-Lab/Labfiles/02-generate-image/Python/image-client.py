import os
import json

# 参照の追加


def main():

    # コンソールをクリア
    os.system('cls' if os.name=='nt' else 'clear')

    try:

        # 構成設定を取得
        load_dotenv()
        endpoint = os.getenv("ENDPOINT")
        model_deployment =  os.getenv("MODEL_DEPLOYMENT")

        # クライアントを初期化




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
