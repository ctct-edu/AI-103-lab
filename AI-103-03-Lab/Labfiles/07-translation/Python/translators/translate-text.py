from dotenv import load_dotenv
import os

# 名前空間のインポート



def main():
    try:
        # コンソールをクリア
        os.system('cls' if os.name == 'nt' else 'clear')

        # 構成設定を取得
        load_dotenv()
        foundry_endpoint = os.getenv('FOUNDRY_ENDPOINT')

        # エンドポイントと資格情報を使用してクライアントを作成



        # ターゲット言語を選択



        # テキストを翻訳



    except Exception as ex:
        print(ex)


if __name__ == "__main__":
    main()
