from dotenv import load_dotenv
import os
import json
from azure.ai.contentunderstanding import ContentUnderstandingClient
from azure.core.credentials import AzureKeyCredential


def main():

    # コンソールをクリア
    os.system('cls' if os.name=='nt' else 'clear')

    try:

        # 名刺のスキーマを取得
        with open("biz-card.json", "r") as file:
            schema_json = json.load(file)

        card_schema = json.dumps(schema_json)

        # 構成設定を取得
        load_dotenv()
        ai_svc_endpoint = os.getenv('ENDPOINT')
        ai_svc_key = os.getenv('KEY')
        analyzer = os.getenv('ANALYZER_NAME')

        # アナライザーを作成
        create_analyzer (card_schema, analyzer, ai_svc_endpoint, ai_svc_key)

        print("\n")

    except Exception as ex:
        print(ex)



def create_analyzer (schema, analyzer, endpoint, key):
    pass  # コードを追加したら、この行は削除してかまいません

    # Content Understanding アナライザーを作成





if __name__ == "__main__":
    main()
