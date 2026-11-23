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
        endpoint=os.getenv("MODEL_ENDPOINT")
        model_deployment=os.getenv("MODEL_NAME")
        speech_file_path = Path(__file__).parent / "speech.mp3"


        # Azure OpenAI クライアントを作成
        token_provider = get_bearer_token_provider(
            DefaultAzureCredential(), "https://ai.azure.com/.default"
        )

        client = AzureOpenAI(
            azure_endpoint=endpoint,
            azure_ad_token_provider=token_provider,
            api_version="2025-03-01-preview"
        )


        # 音声を生成してファイルに保存
        with client.audio.speech.with_streaming_response.create(
            model=model_deployment,
            voice="alloy",
            input="私の声がパスポートです!",
            instructions="真剣なトーンで話してください。",
        ) as response:
            response.stream_to_file(speech_file_path)


        # 生成された音声ファイルを再生
        playsound(speech_file_path)

    except Exception as ex:
        print(ex)

if __name__ == "__main__":
    main()
