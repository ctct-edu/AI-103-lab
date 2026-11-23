from dotenv import load_dotenv
import os
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient


def main():

    # コンソールをクリア
    os.system('cls' if os.name=='nt' else 'clear')

    try:

        # 構成設定を取得
        load_dotenv()
        search_endpoint = os.getenv('SEARCH_ENDPOINT')
        query_key = os.getenv('QUERY_KEY')
        index = os.getenv('INDEX_NAME')

        # 検索クライアントを取得
        search_client = SearchClient(search_endpoint, index, AzureKeyCredential(query_key))

         # ユーザーが 'quit' と入力するまでループ
        while True:
            # クエリ テキストを取得
            query_text = input("クエリを入力してください ('quit' で終了): ")
            if query_text.lower() == "quit":
                break
            if len(query_text) == 0:
                print("クエリを入力してください。")
                continue

            # コンソールをクリア
            os.system('cls' if os.name=='nt' else 'clear')

            # インデックスを検索
            found_documents = search_client.search(
                search_text=query_text,
                select=["title", "locations", "persons", "keyPhrases"],
                order_by=["title"],
                include_total_count=True
            )

            # 結果を解析
            print(f"\n検索結果: {found_documents.get_count()} 件のドキュメント")
            for document in found_documents:
                print(f"\nドキュメント: {document['title']}")
                print(" - 場所:")
                for location in document['locations']:
                    print(f"   - {location}")
                print(" - 人物:")
                for person in document['persons']:
                    print(f"   - {person}")
                print(" - キー フレーズ:")
                for phrase in document['keyPhrases']:
                    print(f"   - {phrase}")

    except Exception as ex:
        print(ex)



if __name__ == "__main__":
    main()
