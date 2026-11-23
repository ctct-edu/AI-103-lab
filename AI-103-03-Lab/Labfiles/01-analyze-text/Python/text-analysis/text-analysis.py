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


        # エンドポイントを使用してクライアントを作成


        # reviews フォルダー内の各テキスト ファイルを分析
        reviews_folder = 'reviews'
        for file_name in os.listdir(reviews_folder):
            # ファイルの内容を読み取り
            print('\n-------------\n' + file_name)
            text = open(os.path.join(reviews_folder, file_name), encoding='utf8').read()
            print('\n' + text)

            # 言語を取得



            # エンティティを取得



            # PII を取得



    except Exception as ex:
        print(ex)


if __name__ == "__main__":
    main()
