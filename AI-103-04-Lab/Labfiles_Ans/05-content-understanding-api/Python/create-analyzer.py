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

    # Content Understanding アナライザーを作成
    print(f"{analyzer} を作成しています")

    # Content Understanding クライアントを作成
    client = ContentUnderstandingClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(key)
    )

    # スキーマ JSON を ContentAnalyzer オブジェクトに解析
    analyzer_definition = json.loads(schema)

    # SDK を使用してアナライザーを作成 (長時間実行操作)
    poller = client.begin_create_analyzer(
        analyzer_id=analyzer,
        resource=analyzer_definition,
        allow_replace=True
    )

    # 操作の完了を待機
    result = poller.result()
    print(f"アナライザー '{analyzer}' を作成しました。")
    print(f"ステータス: {result['status'] if isinstance(result, dict) else 'Succeeded'}")



if __name__ == "__main__":
    main()
