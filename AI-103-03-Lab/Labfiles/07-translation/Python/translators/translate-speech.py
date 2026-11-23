import os
from dotenv import load_dotenv


# 名前空間のインポート



def main():
    try:

        # コンソールをクリア
        os.system('cls' if os.name == 'nt' else 'clear')

        # 構成設定を取得
        load_dotenv()
        foundry_endpoint = os.getenv('FOUNDRY_ENDPOINT')

        # 翻訳を構成



        # 翻訳の音声合成用に音声を構成



        # ユーザーの音声を翻訳



        # 翻訳結果を表示して読み上げ



    except Exception as ex:
        print(ex)


if __name__ == "__main__":
    main()
