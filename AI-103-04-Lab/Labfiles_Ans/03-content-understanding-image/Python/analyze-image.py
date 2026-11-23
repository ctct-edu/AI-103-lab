import sys, os
from dotenv import load_dotenv

# 参照の追加
from azure.ai.contentunderstanding import ContentUnderstandingClient
from azure.ai.contentunderstanding.models import AnalysisInput, AnalysisResult
from azure.core.exceptions import AzureError
from azure.identity import DefaultAzureCredential


def main():
    # コンソールをクリア
    os.system('cls' if os.name == 'nt' else 'clear')

    # 構成設定を取得
    load_dotenv()
    endpoint = os.getenv("ENDPOINT")
    analyzer_id = os.getenv("ANALYZER")
    api_version = "2025-11-01"



    # Content Understanding クライアントをセットアップ
    credential = DefaultAzureCredential()
    client = ContentUnderstandingClient(
        endpoint=endpoint,
        credential=credential,
        api_version=api_version)


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
        try:
            poller = client.begin_analyze(
                analyzer_id=analyzer_id,
                inputs=[AnalysisInput(data=file_bytes)],
            )
            result: AnalysisResult = poller.result()
        except AzureError as err:
            print(f"[Azure エラー]: {err.message}")
            sys.exit(1)
        except Exception as ex:
            print(f"[予期しないエラー]: {ex}")
            sys.exit(1)

        for field in result.contents[0].fields:
            if field == "Description":
                print(f"{field}:\n{result.contents[0].fields[field].value_string}\n")
            elif field == "Tags":
                print(f"{field}:")
                for tag in result.contents[0].fields[field].value_array:
                    print("  -", tag.value_string)



if __name__ == "__main__":
    main()
