---
lab:
    title: 'テキストと音声の翻訳'
    description: 'Foundry Tools の Azure Translator と Azure Speech を使用して翻訳を実装する。'
    level: 300
    duration: 30
    islab: true
    status: 'released'
---

# テキストと音声の翻訳

**Foundry Tools の Azure Translator** は、言語間でテキストを翻訳できるサービスです。同様に、**Foundry Tools の Azure Speech** は音声の翻訳サービスを提供します。この演習では、これらを使用して、サポートされている任意の言語の入力を、選択したターゲット言語に翻訳する翻訳アプリを作成します。

この演習の所要時間は約 **30** 分です。

> **注意**: この演習で使用する一部のテクノロジーはプレビュー中または開発中のため、予期しない動作、警告、またはエラーが発生する場合があります。

## 前提条件

この演習を開始する前に、以下を準備してください。

- 1 日目の演習 01 の完了（1 日目で作成した Foundry プロジェクトを共用します）
- Visual Studio Code、Python 3.13 以降、Azure CLI（演習環境にはインストール済みです）

## 共用の Foundry プロジェクトの確認

この演習では、1 日目の演習 01 で作成した **East US 2** の Foundry プロジェクトを使用します。

1. Web ブラウザーで [Microsoft Foundry ポータル](https://ai.azure.com)（`https://ai.azure.com`）を開き、1 日目の演習 01 で作成したプロジェクト（例: **AI103-Lab01-YYYYMMDD-XX**）のホーム ページを表示します。

    > **ヒント**: **Foundry リソース名** を確認しておいてください。Foundry リソース名は、**[プロジェクト エンドポイント]**（`https://<Foundry リソース名>.services.ai.azure.com/api/projects/<プロジェクト名>`）のホスト名の先頭部分です。リソース名はプロジェクト名から推測できないため、必ずエンドポイントに表示された名前を、そのまま使用してください。

## ポータルでの Azure Translator in Foundry Tools の探索

Foundry ポータルの Azure Translator プレイグラウンドを使用して、サービスを試すことができます。

1. 左側のナビゲーション ペインで **[サービス]**（Services）を選択します。Foundry Tools の Azure サービス（Document Intelligence and Content Understanding、Speech、Language、Translator）の一覧が表示されます。

    ![Foundry ポータルの [サービス] ページのスクリーンショット。赤枠は左側の [サービス] と [Translator]。](../Media/d3e07-01-services-translator.png)

1. **Translator** を選択し、プレイグラウンドの一覧から **Text Translation** を選択します。**Azure Translator - テキスト翻訳**（Azure Translator - Text translation）のプレイグラウンドが開きます。

    ![Translator のプレイグラウンド一覧のスクリーンショット。赤枠は [Text Translation]。](../Media/d3e07-02-translator-text-translation.png)

1. **[翻訳ツール]**（Translator）タブの **[ソース テキスト]**（Source text）領域に、`こんにちは、世界!` と入力します。次に、**[対象言語の選択]**（Select target language）で **English**（英語）を選択し、**[翻訳]**（Translate）ボタンを使用して翻訳を生成します（例: `Hello, World!`）。

    ![テキスト翻訳のプレイグラウンドのスクリーンショット。青枠は [ソース テキスト]、赤枠は対象言語の English、[翻訳] ボタン、翻訳結果。](../Media/d3e07-03-translator-translate.png)

1. 他のいくつかの言語も試します。

1. **[コード]**（Code）タブを選択して、Azure Translator を使用するサンプル コードを表示します。REST API のコードで使用されている **ENDPOINT** 変数に注目してください。`https://{Foundry リソース名}.cognitiveservices.azure.com/` のような形式になっているはずです。

    ![[コード] タブのスクリーンショット。赤枠は [コード] タブと ENDPOINT の行。](../Media/d3e07-04-translator-code-endpoint.png)

    このエンドポイントは Azure AI Services の以前の形式ですが、Foundry リソース内の Azure Translator リソースに接続するために現在も使用されています。Azure Speech ツールへの接続にも使用できます。

    > **ヒント**: このエンドポイントはあとで必要になります。

## スターター コードを開く

アプリケーションの初期ファイルは、演習環境に配置済みです。

1. Visual Studio Code を開きます。

1. **[ファイル] > [フォルダーを開く]** を選択し、配置済みの `Labfiles/07-translation` フォルダーを開きます。

## テキスト翻訳アプリケーションの作成

1. エクスプローラー ペインで **Python/translators** フォルダーを展開します。アプリケーション ファイルは次のとおりです。
    - **.env**（アプリケーションの構成ファイル）
    - **requirements.txt**（インストールが必要な Python パッケージの依存関係）
    - **translate-text.py**（テキスト アプリケーションのコード ファイル）
    - **translate-speech.py**（音声アプリケーションのコード ファイル）
    - **message_ja.wav**（「マイクが使えない場合」で使用する日本語の音声ファイル）
    - **message_2.wav**（英語の音声ファイル。英語でも試せます）

### テキスト翻訳アプリケーションの構成

1. **translators** フォルダーを右クリックし、**[統合ターミナルで開く]** を選択します。ターミナルが **translators** フォルダーで開いていることを確認します。

1. ターミナルで次のコマンドを入力して、演習用にあらかじめ構築済みの仮想環境 (`labenv`) を有効化します。

    ```
    .\labenv\Scripts\Activate.ps1
    ```

    > **注意**: 必要な Python パッケージ (Azure Translator SDK、Speech SDK など) は `labenv` に事前インストール済みです。`pip install` を再実行する必要はありません。

1. **.env** ファイルを開き、`your_foundry_endpoint` を Foundry リソースの Cognitive Services **エンドポイント** に置き換えます。

    > **重要**: エンドポイントは `https://{Foundry リソース名}.cognitiveservices.azure.com/` の形式にします。Foundry ポータルのプロジェクト エンドポイントをそのまま貼り付けると接続エラーになります。[演習 04](04-azure-speech.md) と同様に、ドメインを `.services.ai.azure.com` から `.cognitiveservices.azure.com` に変更し、末尾の `/api/projects/{プロジェクト名}` を削除して、末尾に `/` を付けてください。Foundry リソース名の部分は変えません。

    変更後、**Ctrl+S** キーを押して構成ファイルを保存します。

### テキストを翻訳するコードの追加

1. **translate-text.py** ファイルを開き、既存のコードを確認します。Azure Translator を使用するコードを追加していきます。

1. ファイルの先頭の既存の参照の下にあるコメント **名前空間のインポート** を見つけて、Translator SDK を使用するために必要な名前空間をインポートする以下のコードを追加します。

    ```python
    # 名前空間のインポート
    from azure.identity import DefaultAzureCredential
    from azure.ai.translation.text import *
    from azure.ai.translation.text.models import InputTextItem
    ```

1. **main** 関数では、既存のコードが構成設定を読み込んでいます。コメント **エンドポイントと資格情報を使用してクライアントを作成** を見つけて、以下のコードを追加します。

    ```python
    # エンドポイントと資格情報を使用してクライアントを作成
    credential = DefaultAzureCredential()
    client = TextTranslationClient(credential=credential, endpoint=foundry_endpoint)
    ```

1. コメント **ターゲット言語を選択** を見つけて、以下のコードを追加します。

    ```python
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
    ```

1. コメント **テキストを翻訳** を見つけて、以下のコードを追加します。

    ```python
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
    ```

1. コード ファイルに加えた変更を保存します。次に、ターミナル ペインで次のコマンドを使用して Azure にサインインします。

    ```
    az login
    ```

1. メッセージに従って Azure にサインインします。

1. サインインしたら、次のコマンドを入力してアプリケーションを実行します。

    ```
    python translate-text.py
    ```

1. プロンプトが表示されたら、表示されたリンク先の一覧にある有効なターゲット言語を入力します。

1. 翻訳するフレーズを入力し（例: `こんにちは、元気ですか？` や `明日の会議は10時に始まります。`）、結果を確認します。翻訳元の言語が検出され、テキストがターゲット言語に翻訳されるはずです。

    > **ヒント**: 翻訳元の言語は自動的に検出されるため、言語を指定する必要はありません。英語（たとえば `This is a test`）やフランス語（`C'est un test`）のフレーズを入力して、ターゲット言語 `ja` への翻訳を試すこともできます。ターゲット言語は、`en` のほかに `fr`（フランス語）や `ko`（韓国語）なども試せます。

    **出力例**（ターゲット言語 `en`。サポートされる言語の数は変わる場合があります）:

    ```output
    156 言語がサポートされています。
    ...
    翻訳するテキストを入力してください ('quit' で終了):'こんにちは、元気ですか？' は ja から en に翻訳されました: 'Hello, how are you?'
    翻訳するテキストを入力してください ('quit' で終了):'明日の会議は10時に始まります。' は ja から en に翻訳されました: 'Tomorrow's meeting starts at 10 o'clock.'
    ```

1. 終わったら、`quit` と入力します。アプリケーションをもう一度実行して、別のターゲット言語を選択することもできます。

## 音声翻訳アプリケーションの作成

### 音声翻訳アプリケーションの構成

1. **translators** フォルダーの **.env** ファイルに、Foundry リソースの **エンドポイント** が設定されていることを確認します（Azure Speech は、Azure Translator と同じ情報を使用して Foundry リソースに接続できます）。

1. ターミナルが **translators** フォルダーで開いていて、プロンプトの先頭に **(labenv)** と表示されていることを確認します。

### 音声を翻訳するコードの追加

1. **translate-speech.py** ファイルを開き、既存のコードを確認します。Azure Speech を使用するコードを追加していきます。

1. ファイルの先頭の既存の参照の下にあるコメント **名前空間のインポート** を見つけて、Speech SDK を使用するために必要な名前空間をインポートする以下のコードを追加します。

    ```python
    # 名前空間のインポート
    from azure.identity import DefaultAzureCredential
    import azure.cognitiveservices.speech as speech_sdk
    ```

1. **main** 関数の、コメント **構成設定を取得** の下で、構成ファイルで定義したエンドポイントをコードが読み込んでいます。

1. コメント **翻訳を構成** を見つけて、Azure Speech 用の Foundry エンドポイントへの接続を構成し、日本語の音声を英語、フランス語、スペイン語、ヒンディー語に翻訳する準備をする、以下のコードを追加します。

    ```python
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
    ```

    `speech_recognition_language` には、話される言語（ここでは日本語の `ja-JP`）を指定します。`add_target_language` には、翻訳先の言語を指定します。この演習では、英語（`en`）、フランス語（`fr`）、スペイン語（`es`）、ヒンディー語（`hi`）に翻訳します。

1. **SpeechTranslationConfig** は音声をテキストに翻訳するために使用しますが、翻訳結果を音声に合成するためには **SpeechConfig** も使用します。コメント **翻訳の音声合成用に音声を構成** の下に、次のコードを追加します。

    ```python
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
    ```

    `voices` は、翻訳先の言語コードと、その言語を読み上げる音声名の対応表です。翻訳先の言語を増やす場合は、その言語の音声名もこの表に追加します。

1. 次に、システムのマイクから入力されたユーザーの音声を翻訳するコードを追加します。コメント **ユーザーの音声を翻訳** を見つけて、以下のコードを追加します。

    ```python
    # ユーザーの音声を翻訳
    print("話してください...")
    translation_results = translator.recognize_once_async().get()
    print(f"'{translation_results.text}' を翻訳しています")
    ```

1. 結果が返されると、アプリケーションは翻訳結果を順に処理し、テキストを表示して、合成した音声を既定のシステム スピーカーで再生します。コメント **翻訳結果を表示して読み上げ** を見つけて、以下のコードを追加します。

    ```python
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
    ```

1. コード ファイルに加えた変更を保存します。次に、ターミナル ペインで、まだ Azure にサインインしていない場合（またはセッションの有効期限が切れている場合）は、次のコマンドを使用して Azure にサインインします。

    ```
    az login
    ```

1. サインインしたら、次のコマンドを入力してアプリケーションを実行します。

    ```
    python translate-speech.py
    ```

1. プロンプトが表示されたら、何か話します（たとえば、日本語で「*こんにちは!*」）。

    プログラムは、コードで指定された言語（英語、フランス語、スペイン語、ヒンディー語）に翻訳し、翻訳結果を表示して読み上げます。

    > **注意**: ヒンディー語への翻訳は、文字エンコードの問題により、ターミナルで正しく表示されない場合があります。

    > **注意**: 認識する音声の言語は、コードで `ja-JP`（日本語）に設定しています。英語で話す場合は、`speech_recognition_language` を `en-US`（米国英語）に変更します。設定した言語以外の言語で話すと、その言語として認識されるため、正しく翻訳されません。

## マイクが使えない場合

マイクが使えない環境では、翻訳する音声を、**マイクの代わりに音声ファイル** から入力できます。入力には、日本語の音声ファイル（**message_ja.wav**）を使用します。この音声ファイルは、**translators** フォルダーに配置されています。また、翻訳結果の音声は、スピーカーではなく **ファイル** に保存できます。

> **注意**: 完成版のコードは、解答フォルダーの **translate-speech_file.py** にあります。**message_ja.wav** は日本語（`ja-JP`）の音声です。英語の音声ファイル **message_2.wav**（米国英語、`en-US`）を使う場合は、`speech_recognition_language` を `'en-US'` に、`AudioConfig(filename=...)` のファイル名を `message_2.wav` に変更します。

1. **translate-speech.py** をコピーして、**translate-speech_file.py** という名前で保存します。

1. **translate-speech_file.py** で、コメント **翻訳を構成** の下のコードを、次のように変更します。音声の入力に、既定のマイクではなく音声ファイルを使用します。

    ```python
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
    audio_in_cfg = speech_sdk.AudioConfig(filename="message_ja.wav")
    translator = speech_sdk.translation.TranslationRecognizer(
        translation_config=translation_cfg,
        audio_config=audio_in_cfg
    )
    print('翻訳の準備ができました。入力言語:', translation_cfg.speech_recognition_language)
    ```

1. コメント **ユーザーの音声を翻訳** の下のコードを、次のように変更します。

    ```python
    # ユーザーの音声を翻訳
    print("音声ファイル message_ja.wav を翻訳します...")
    translation_results = translator.recognize_once_async().get()
    print(f"'{translation_results.text}' を翻訳しています")
    ```

1. コメント **翻訳結果を表示して読み上げ** の下のコードを、次のように変更します。翻訳結果の音声は、スピーカーではなく `translation_` で始まる名前の音声ファイルに保存されます。

    ```python
    # 翻訳結果を表示して読み上げ
    translations = translation_results.translations
    for translation_language in translations:

        print(f"{translation_language}: '{translations[translation_language]}'")

        speech_cfg.speech_synthesis_voice_name = voices.get(translation_language)
        output_file = f"translation_{translation_language}.wav"
        audio_out_cfg = speech_sdk.audio.AudioOutputConfig(filename=output_file)
        speech_synthesizer = speech_sdk.SpeechSynthesizer(speech_cfg, audio_out_cfg)
        speak = speech_synthesizer.speak_text_async(translations[translation_language]).get()

        if speak.reason == speech_sdk.ResultReason.SynthesizingAudioCompleted:
            print(f"音声を {output_file} に保存しました")
        else:
            print(speak.reason)
    ```

1. 変更を保存して、次のコマンドを入力してアプリケーションを実行します。

    ```
    python translate-speech_file.py
    ```

1. 出力を確認します。翻訳されたテキストが言語ごとに表示され、**translators** フォルダーに `translation_en.wav`、`translation_fr.wav`、`translation_es.wav`、`translation_hi.wav` が作成されます。

    **出力例**（翻訳結果は実行のたびに変わる場合があります）:

    ```output
    翻訳の準備ができました。入力言語: ja-JP
    音声サービスの準備ができました。
    音声ファイル message_ja.wav を翻訳します...
    '鈴木です。明日の会議は10時に始まります。会議室でお待ちしています。' を翻訳しています
    en: 'This is Suzuki. Tomorrow's meeting starts at 10 o'clock. We will be waiting for you in the conference room.'
    音声を translation_en.wav に保存しました
    fr: 'Ici Suzuki. La réunion de demain commence à 10 heures. Nous vous attendrons dans la salle de conférence.'
    音声を translation_fr.wav に保存しました
    es: 'Esta es Suzuki. La reunión de mañana empieza a las 10 en punto. Te estaremos esperando en la sala de conferencias.'
    音声を translation_es.wav に保存しました
    hi: 'यह सुजुकी है। कल की बैठक 10 बजे शुरू होगी। हम तुम्हारा इंतजार कॉन्फ्रेंस रूम में करेंगे।'
    音声を translation_hi.wav に保存しました
    ```

    スピーカーがなくても、これらのファイルが作成されていて、ファイルサイズが 0 より大きいことを確認すれば、音声が生成されたことを確認できます。VS Code のエクスプローラーでファイルを選択すると、スピーカーがある環境では再生もできます。

## クリーンアップ

> **重要**: この演習では、リソースを削除しません。**Foundry プロジェクトとモデル（gpt-4o-mini-tts、gpt-4o-mini-transcribe など）、エージェント、演習 05 で使用したストレージ アカウント（`ai103stgXXYYYYMMDD`）は、まだ削除しないでください。** 1 日目の演習 01 で作成した Foundry プロジェクトは、4 日目の演習でも使用します。リソース グループ（**AI103StudentXX**）を削除すると、共用のプロジェクトも削除され、4 日目の演習が実施できなくなります。

リソースの削除は、**4 日目の演習 06「ナレッジ マイニング ソリューションの作成」の「クリーンアップ」**で、1〜4 日目の分をまとめて **1 回だけ**行います。

演習 05 で SAS URL を保存したテキスト ファイルは、最終クリーンアップのときに、ローカル コンピューターから削除してください。
