from dotenv import load_dotenv
import os

# 名前空間のインポート
from azure.identity import DefaultAzureCredential
from azure.ai.textanalytics import TextAnalyticsClient


def main():
    try:
        # コンソールをクリア
        os.system('cls' if os.name == 'nt' else 'clear')

        # 構成設定を取得
        load_dotenv()
        foundry_endpoint = os.getenv('FOUNDRY_ENDPOINT')


        # エンドポイントを使用してクライアントを作成
        credential = DefaultAzureCredential()
        ai_client = TextAnalyticsClient(endpoint=foundry_endpoint, credential=credential)


        # reviews フォルダー内の各テキスト ファイルを分析
        reviews_folder = 'reviews'
        for file_name in os.listdir(reviews_folder):
            # ファイルの内容を読み取り
            print('\n-------------\n' + file_name)
            text = open(os.path.join(reviews_folder, file_name), encoding='utf8').read()
            print('\n' + text)

            # 言語を取得
            detectedLanguage = ai_client.detect_language(documents=[text])[0]
            print('\n言語: {}'.format(detectedLanguage.primary_language.name))


            # エンティティを取得
            entities = ai_client.recognize_entities(documents=[text])[0].entities
            if len(entities) > 0:
                print("\nエンティティ")
                for entity in entities:
                    print('\t{} ({})'.format(entity.text, entity.category))


            # PII を取得
            pii_result = ai_client.recognize_pii_entities(documents=[text])[0]
            pii_entities = pii_result.entities
            if len(pii_entities) > 0:
                print("\nPII エンティティ")
                for pii_entity in pii_entities:
                    print('\t{} ({})'.format(pii_entity.text, pii_entity.category))
                print("編集済みテキスト:\n {}".format(pii_result.redacted_text))


    except Exception as ex:
        print(ex)


if __name__ == "__main__":
    main()
