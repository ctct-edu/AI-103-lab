import os
from pathlib import Path
from playsound3 import playsound
from dotenv import load_dotenv

# 名前空間のインポート
from openai import AzureOpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider


def main():
    try:
        # コンソールをクリア
        os.system('cls' if os.name == 'nt' else 'clear')

        # 構成設定を取得
        load_dotenv()
        endpoint = os.getenv("MODEL_ENDPOINT")
        model_deployment = os.getenv("MODEL_NAME")
        file_path = Path(__file__).parent / "speech_ja.wav"

        # 音声ファイルを再生
        playsound(file_path)

        # Azure OpenAI クライアントを作成
        token_provider = get_bearer_token_provider(
            DefaultAzureCredential(), "https://ai.azure.com/.default"
        )

        client = AzureOpenAI(
            azure_endpoint=endpoint,
            azure_ad_token_provider=token_provider,
            api_version="2025-03-01-preview"
        )


        # モデルを呼び出して音声ファイルを文字起こし
        audio_file = open(file_path, "rb")
        transcription = client.audio.transcriptions.create(
            model=model_deployment,
            file=audio_file,
            response_format="text"
        )

        print(transcription)


    except Exception as ex:
        print(ex)


if __name__ == "__main__":
    main()
