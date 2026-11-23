import os
from dotenv import load_dotenv


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

        # 翻訳を構成
        credential = DefaultAzureCredential()
        translation_cfg = speech_sdk.translation.SpeechTranslationConfig(
            token_credential=credential,
            endpoint=foundry_endpoint
        )
        translation_cfg.speech_recognition_language = 'ja-JP'
        translation_cfg.add_target_language('en')
        translation_cfg.add_target_language('fr')
        translation_cfg.add_target_language('es')
        translation_cfg.add_target_language('hi')
        audio_in_cfg = speech_sdk.AudioConfig(use_default_microphone=True)
        translator = speech_sdk.translation.TranslationRecognizer(
            translation_config=translation_cfg,
            audio_config=audio_in_cfg
        )
        print('翻訳の準備ができました。入力言語:', translation_cfg.speech_recognition_language)


        # 翻訳の音声合成用に音声を構成
        speech_cfg = speech_sdk.SpeechConfig(
            token_credential=credential, endpoint=foundry_endpoint)
        voices = {
            "en": "en-US-JennyNeural",
            "fr": "fr-FR-HenriNeural",
            "es": "es-ES-ElviraNeural",
            "hi": "hi-IN-MadhurNeural"
        }
        print('音声サービスの準備ができました。')


        # ユーザーの音声を翻訳
        print("話してください...")
        translation_results = translator.recognize_once_async().get()
        print(f"'{translation_results.text}' を翻訳しています")


        # 翻訳結果を表示して読み上げ
        translations = translation_results.translations
        for translation_language in translations:

            print(f"{translation_language}: '{translations[translation_language]}'")

            speech_cfg.speech_synthesis_voice_name = voices.get(translation_language)
            audio_out_cfg = speech_sdk.audio.AudioOutputConfig(use_default_speaker=True)
            speech_synthesizer = speech_sdk.SpeechSynthesizer(speech_cfg, audio_out_cfg)
            speak = speech_synthesizer.speak_text_async(translations[translation_language]).get()

            if speak.reason != speech_sdk.ResultReason.SynthesizingAudioCompleted:
                print(speak.reason)


    except Exception as ex:
        print(ex)


if __name__ == "__main__":
    main()
