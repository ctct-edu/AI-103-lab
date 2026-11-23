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
        endpoint = os.getenv("MODEL_ENDPOINT")
        model_deployment = os.getenv("MODEL_NAME")
        file_path = Path(__file__).parent / "speech_ja.wav"

        # 音声ファイルを再生
        playsound(file_path)

        # Azure OpenAI クライアントを作成



        # モデルを呼び出して音声ファイルを文字起こし




    except Exception as ex:
        print(ex)


if __name__ == "__main__":
    main()
