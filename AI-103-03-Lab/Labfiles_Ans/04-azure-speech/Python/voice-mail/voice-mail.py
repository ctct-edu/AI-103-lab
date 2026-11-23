from dotenv import load_dotenv
import os
from playsound3 import playsound

# 名前空間のインポート
from azure.identity import DefaultAzureCredential
import azure.cognitiveservices.speech as speech_sdk


def main():
    try:
        # コンソールをクリア
        os.system('cls' if os.name == 'nt' else 'clear')

        # 構成設定を取得
        load_dotenv()
        foundry_endpoint = os.getenv('FOUNDRY_ENDPOINT')

        # Entra ID 認証を使用して speech_config を作成
        credential = DefaultAzureCredential()
        speech_config = speech_sdk.SpeechConfig(
            token_credential=credential,
            endpoint=foundry_endpoint)


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
    output_file = "greeting.wav"
    audio_config = speech_sdk.audio.AudioOutputConfig(filename=output_file)

    speech_config.speech_synthesis_voice_name = "ja-JP-Nanami:DragonHDLatestNeural"

    speech_synthesizer = speech_sdk.SpeechSynthesizer(
        speech_config=speech_config,
        audio_config=audio_config
    )

    result = speech_synthesizer.speak_text_async(greeting_message).get()

    if result.reason == speech_sdk.ResultReason.SynthesizingAudioCompleted:
        print(f"挨拶を録音して {output_file} に保存しました")
        speech_synthesizer = None  # シンセサイザーのリソースを解放
    else:
        print("挨拶の録音でエラーが発生しました: {}".format(result.reason))



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
            audio_config = speech_sdk.audio.AudioConfig(filename=file_path)
            # 日本語と英語のメッセージを認識できるように、言語を自動検出する
            auto_detect_config = speech_sdk.languageconfig.AutoDetectSourceLanguageConfig(
                languages=["ja-JP", "en-US"]
            )
            speech_recognizer = speech_sdk.SpeechRecognizer(
                speech_config=speech_config,
                auto_detect_source_language_config=auto_detect_config,
                audio_config=audio_config
            )
            result = speech_recognizer.recognize_once_async().get()
            if result.reason == speech_sdk.ResultReason.RecognizedSpeech:
                detected_language = speech_sdk.AutoDetectSourceLanguageResult(result).language
                print(f"検出された言語: {detected_language}")
                print(f"文字起こし結果: {result.text}")
            else:
                print("メッセージの文字起こしでエラーが発生しました: {}".format(result.reason))


if __name__ == "__main__":
    main()
