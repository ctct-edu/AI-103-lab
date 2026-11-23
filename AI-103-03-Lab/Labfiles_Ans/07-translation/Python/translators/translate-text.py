from dotenv import load_dotenv
import os

# 名前空間のインポート
from azure.identity import DefaultAzureCredential
from azure.ai.translation.text import *
from azure.ai.translation.text.models import InputTextItem


def main():
    try:
        # コンソールをクリア
        os.system('cls' if os.name == 'nt' else 'clear')

        # 構成設定を取得
        load_dotenv()
        foundry_endpoint = os.getenv('FOUNDRY_ENDPOINT')

        # エンドポイントと資格情報を使用してクライアントを作成
        credential = DefaultAzureCredential()
        client = TextTranslationClient(credential=credential, endpoint=foundry_endpoint)


        # ターゲット言語を選択
        languagesResponse = client.get_supported_languages(scope="translation")
        print("{} 言語がサポートされています。".format(len(languagesResponse.translation)))
        print("(https://learn.microsoft.com/azure/ai-services/translator/language-support#translation を参照してください)")
        print("翻訳のターゲット言語コードを入力してください (例: 'en'):")
        targetLanguage = "xx"
        supportedLanguage = False
        while supportedLanguage == False:
            targetLanguage = input()
            if targetLanguage in languagesResponse.translation.keys():
                supportedLanguage = True
            else:
                print("{} はサポートされていない言語です。".format(targetLanguage))


        # テキストを翻訳
        inputText = ""
        while inputText.lower() != "quit":
            inputText = input("翻訳するテキストを入力してください ('quit' で終了):")
            if inputText != "quit":
                input_text_elements = [InputTextItem(text=inputText)]
                translationResponse = client.translate(body=input_text_elements, to_language=[targetLanguage])
                translation = translationResponse[0] if translationResponse else None
                if translation:
                    sourceLanguage = translation.detected_language
                    for translated_text in translation.translations:
                        print(f"'{inputText}' は {sourceLanguage.language} から {translated_text.to} に翻訳されました: '{translated_text.text}'")


    except Exception as ex:
        print(ex)


if __name__ == "__main__":
    main()
