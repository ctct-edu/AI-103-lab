import sys, os
from dotenv import load_dotenv

# 参照の追加




def main():
    # コンソールをクリア
    os.system('cls' if os.name == 'nt' else 'clear')

    # 構成設定を取得
    load_dotenv()
    endpoint = os.getenv("ENDPOINT")
    analyzer_id = os.getenv("ANALYZER")
    api_version = "2025-11-01"



    # Content Understanding クライアントをセットアップ



    while True:
        file_no = input('\nファイルを選択してください (1、2、3)。それ以外を入力すると終了します: ')
        if file_no not in ["1", "2", "3"]:
            break

        file_path = f"images/image{file_no}.jpg"

        with open(file_path, "rb") as f:
            file_bytes = f.read()

        print(f"{analyzer_id} アナライザーで分析しています...")
        print(f"  ファイル: {file_path}\n")


        # ファイルを分析




if __name__ == "__main__":
    main()
