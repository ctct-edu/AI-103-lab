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
    pass  # コードを追加したら、この行は削除してかまいません

    # Content Understanding を使用して画像を分析





if __name__ == "__main__":
    main()
