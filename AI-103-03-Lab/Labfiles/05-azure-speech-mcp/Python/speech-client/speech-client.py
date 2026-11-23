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
        agent_name = os.getenv('AGENT_NAME')


        # プロジェクト クライアントを取得


        # OpenAI クライアントを取得


        # メイン ループ
        while True:
            # ユーザー入力を取得
            prompt = input("ユーザー プロンプト（終了するには 'quit'）: ")
            if prompt == "quit" or len(prompt) == 0:
                break
            else:
                pass  # コードを追加したら、この行は削除してかまいません
                # エージェントを使用して応答を取得



    except Exception as ex:
        print(ex)

if __name__ == "__main__":
    main()
