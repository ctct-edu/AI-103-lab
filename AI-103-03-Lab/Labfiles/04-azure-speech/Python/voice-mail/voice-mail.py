from dotenv import load_dotenv
import os
from playsound3 import playsound

# 名前空間のインポート



def main():
    try:
        # コンソールをクリア
        os.system('cls' if os.name == 'nt' else 'clear')

        # 構成設定を取得
        load_dotenv()
        foundry_endpoint = os.getenv('FOUNDRY_ENDPOINT')

        # Entra ID 認証を使用して speech_config を作成



        # ユーザーが終了するまでループ
        inputText = ""
        while inputText.lower() != "3":
            inputText = input("オプションを選択してください:\n1: 挨拶を録音\n2: メッセージを文字起こし\n3: 終了\n")
            if inputText != "3":
                if inputText == "1":
                    record_greeting(speech_config)
                elif inputText == "2":
                    transcribe_messages(speech_config)
                elif inputText == "3":
                    print("終了します...")
                    return
                else:
                    print("無効なオプションです。もう一度お試しください。")



    except Exception as ex:
        print(ex)

# record_greeting 関数
def record_greeting(speech_config):
    print("挨拶を録音しています...")

    # ユーザーから挨拶メッセージを取得
    greeting_message = input("挨拶メッセージを入力してください: ")


    # 挨拶メッセージを音声ファイルに合成




# transcribe_messages 関数
def transcribe_messages(speech_config):
    print("メッセージを文字起こししています...")

    messages_folder = 'messages'
    for file_name in os.listdir(messages_folder):
        if file_name.endswith('.wav'):
            print(f"\n{file_name} を文字起こししています...")
            file_path = os.path.join(messages_folder, file_name)
            playsound(file_path)

            # 音声ファイルを文字起こし



if __name__ == "__main__":
    main()
