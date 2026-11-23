from dotenv import load_dotenv
import os
import sys
import json
from azure.ai.contentunderstanding import ContentUnderstandingClient
from azure.core.credentials import AzureKeyCredential


def main():

    # コンソールをクリア
    os.system('cls' if os.name=='nt' else 'clear')

    try:

        # 名刺を取得
        image_file = 'biz-card-1.png'
        if len(sys.argv) > 1:
            image_file = sys.argv[1]

        # 構成設定を取得
        load_dotenv()
        ai_svc_endpoint = os.getenv('ENDPOINT')
        ai_svc_key = os.getenv('KEY')
        analyzer = os.getenv('ANALYZER_NAME')

        # 名刺を分析
        analyze_card (image_file, analyzer, ai_svc_endpoint, ai_svc_key)

        print("\n")

    except Exception as ex:
        print(ex)



def analyze_card (image_file, analyzer, endpoint, key):

    # Content Understanding を使用して画像を分析
    print(f"{image_file} を分析しています")

    # Content Understanding クライアントを作成
    client = ContentUnderstandingClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(key)
    )

    # 画像データを読み取り
    with open(image_file, "rb") as file:
        image_data = file.read()

    # 分析のために画像を送信
    print("要求を送信しています...")
    poller = client.begin_analyze_binary(
        analyzer_id=analyzer,
        binary_input=image_data
    )

    # 分析の完了を待機
    result = poller.result()
    print("分析に成功しました:\n")

    # JSON の結果をファイルに保存
    output_file = "results.json"
    with open(output_file, "w") as json_file:
        json.dump(dict(result), json_file, indent=4, default=str)
        print(f"応答を {output_file} に保存しました\n")

    # コンテンツを順に処理してフィールドを抽出
    for content in result.contents:
        if hasattr(content, 'fields') and content.fields:
            for field_name, field_data in content.fields.items():
                value = field_data.value if hasattr(field_data, 'value') else None
                print(f"{field_name}: {value}")





if __name__ == "__main__":
    main()
