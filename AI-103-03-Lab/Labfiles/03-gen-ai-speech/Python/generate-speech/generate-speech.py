import os
from pathlib import Path
from playsound3 import playsound
from dotenv import load_dotenv

# 名前空間のインポート



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



        # 音声を生成してファイルに保存



        # 生成された音声ファイルを再生
        playsound(speech_file_path)

    except Exception as ex:
        print(ex)

if __name__ == "__main__":
    main()
