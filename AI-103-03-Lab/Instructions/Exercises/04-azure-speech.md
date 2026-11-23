---
lab:
    title: '音声の認識と合成'
    description: 'Foundry Tools の Azure Speech を使用して音声機能を実装する。'
    level: 300
    duration: 30
    islab: true
    status: 'released'
---

# 音声の認識と合成

**Foundry Tools の Azure Speech** は、次のような音声関連の機能を提供するサービスです。

- *音声テキスト変換* API: 音声認識（話された言葉をテキストに変換する）を実装できます。
- *テキスト読み上げ* API: 音声合成（テキストを音声に変換する）を実装できます。

この演習では、これら 2 つの API を使用して、ボイスメール アシスタントを実装します。

この演習の所要時間は約 **30** 分です。

> **注意**: この演習で使用する一部のテクノロジーはプレビュー中または開発中のため、予期しない動作、警告、またはエラーが発生する場合があります。

## 前提条件

この演習を開始する前に、以下を準備してください。

- 1 日目の演習 01 の完了（1 日目で作成した Foundry プロジェクトを共用します）
- Visual Studio Code、Python 3.13 以降、Azure CLI（演習環境にはインストール済みです）

## 共用の Foundry プロジェクトの確認

この演習では、新しいプロジェクトは作成しません。1 日目の演習 01 で作成した **East US 2** の Foundry プロジェクトを使用します。

1. Web ブラウザーで [Microsoft Foundry ポータル](https://ai.azure.com)（`https://ai.azure.com`）を開き、1 日目の演習 01 で作成したプロジェクト（例: **AI103-Lab01-YYYYMMDD-XX**）のホーム ページを表示します。

    > **ヒント**: **Foundry リソース名** を確認しておいてください。このあとの手順でエンドポイントを組み立てるときに必要になります。Foundry リソース名は、**[プロジェクト エンドポイント]**（`https://<Foundry リソース名>.services.ai.azure.com/api/projects/<プロジェクト名>`）のホスト名の先頭部分です。リソース名はプロジェクト名から推測できないため、必ずエンドポイントに表示された名前を、そのまま使用してください。

## スターター コードを開く

アプリケーションの初期ファイルは、演習環境に配置済みです。

1. Visual Studio Code を開きます。

1. **[ファイル] > [フォルダーを開く]** を選択し、配置済みの `Labfiles/04-azure-speech` フォルダーを開きます。

1. エクスプローラー ペインで **Python/voice-mail** フォルダーを展開します。アプリケーション ファイルは次のとおりです。
    - **messages**（メッセージの音声録音を含むサブフォルダー。英語の `message_1.wav`、`message_2.wav` と、日本語の `message_ja_1.wav`、`message_ja_2.wav` があります）
    - **.env**（アプリケーションの構成ファイル）
    - **requirements.txt**（インストールが必要な Python パッケージの依存関係）
    - **voice-mail.py**（アプリケーションのコード ファイル）

## アプリケーションの構成

1. **voice-mail** フォルダーを右クリックし、**[統合ターミナルで開く]** を選択します。ターミナルが **voice-mail** フォルダーで開いていることを確認します。

1. ターミナルで次のコマンドを入力して、演習用にあらかじめ構築済みの仮想環境 (`labenv`) を有効化します。

    ```
    .\labenv\Scripts\Activate.ps1
    ```

    > **注意**: 必要な Python パッケージ (Azure AI Speech SDK など) は `labenv` に事前インストール済みです。`pip install` を再実行する必要はありません。

1. **.env** ファイルを開き、`your_foundry_endpoint` を Foundry リソースの Cognitive Services **エンドポイント** に置き換えます。

    > **⚠️ 重要: この演習の `.env` に設定するエンドポイントは、これまでの演習（演習 01 など）と値が異なります。** Foundry ポータルからコピーしたエンドポイントをそのまま貼り付けると、接続エラーになります。**必ず次のように修正してから** `.env` に設定してください。

    **修正のポイント（3 点）**:

    1. ドメインを **`.services.ai.azure.com`** から **`.cognitiveservices.azure.com`** に変更する
    1. 末尾の **`/api/projects/{プロジェクト名}`** を **削除** する
    1. 末尾に **`/`**（スラッシュ）を付ける

    **例**（プロジェクト名が `AI103-Lab01-20261119-01` の場合）:

    | | エンドポイント |
    |---|---|
    | **変更前**（Foundry ポータルからコピーした値） | `https://ai103-lab01-20261119-01-resource.`**`services.ai`**`.azure.com`**`/api/projects/AI103-Lab01-20261119-01`** |
    | **変更前**（演習 01 の `.env` で使用した値） | `https://ai103-lab01-20261119-01-resource.`**`services.ai`**`.azure.com` |
    | **変更後**（この演習の `.env` に設定する値） | `https://ai103-lab01-20261119-01-resource.`**`cognitiveservices`**`.azure.com`**`/`** |

    > **注意**: **Foundry リソース名**（例: `ai103-lab01-20261119-01-resource`）の部分は変えません。プロジェクト名ではなく、コピーしたエンドポイントのホスト名の先頭部分をそのまま使います。

    変更後、**Ctrl+S** キーを押して構成ファイルを保存します。

## 音声を合成するコードの追加

1. **voice-mail.py** ファイルを開き、既存のコードを確認します。Azure Speech SDK を使用するコードを追加していきます。

1. ファイルの先頭の既存の参照の下にあるコメント **名前空間のインポート** を見つけて、Speech SDK を使用するために必要な名前空間をインポートする以下のコードを追加します。

    ```python
    # 名前空間のインポート
    from azure.identity import DefaultAzureCredential
    import azure.cognitiveservices.speech as speech_sdk
    ```

1. **main** 関数では、構成ファイルからエンドポイントを読み込むコードがすでに用意されています。コメント **Entra ID 認証を使用して speech_config を作成** を見つけて、Speech の構成オブジェクトを作成する以下のコードを追加します。

    ```python
    # Entra ID 認証を使用して speech_config を作成
    credential = DefaultAzureCredential()
    speech_config = speech_sdk.SpeechConfig(
        token_credential=credential,
        endpoint=foundry_endpoint)
    ```

1. **main** 関数の残りのコードを確認します。ユーザーが次の 3 つのオプションから 1 つを選択できるループが実装されています。
    1. 音声の挨拶を録音する
    1. メッセージを文字起こしする
    1. アプリケーションを終了する

1. **record_greeting** 関数を見つけます。この関数を実装して、音声の挨拶を音声ファイルとして録音（合成）します。

1. **record_greeting** 関数の中で、コメント **挨拶メッセージを音声ファイルに合成** を見つけて、ユーザーが入力したテキストから音声を合成し、音声ファイルとして保存する以下のコードを追加します。

    ```python
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
    ```

    使用している音声（`ja-JP-Nanami:DragonHDLatestNeural`）は **日本語（日本）** の音声です。次の手順で入力する挨拶は日本語にしてください。

    > **ヒント**: 日本語の音声には、ほかに `ja-JP-NanamiNeural`（女性）や `ja-JP-KeitaNeural`（男性）などがあります。英語の挨拶を合成する場合は、英語の音声（例: `en-US-Serena:DragonHDLatestNeural`）に変更します。

1. 変更を保存します。次に、ターミナル ペインで次のコマンドを使用して Azure にサインインします。

    ```
    az login
    ```

1. メッセージに従って Azure にサインインします。サブスクリプションの詳細を確認します。

1. サインインしたら、次のコマンドを入力してアプリケーションを実行します。

    ```
    python voice-mail.py
    ```

1. プロンプトが表示されたら、**1** を入力して挨拶を録音します。

1. 次のような挨拶を入力します。

    ```
    お電話ありがとうございます。ただいま席を外しております。メッセージをお残しください。
    ```

1. 音声が合成されて音声ファイルとして保存されるまで待ちます。

    **voice-mail** フォルダーに生成された *greeting.wav* ファイルを選択すると、Visual Studio Code で再生できます。スピーカーが使えない場合も、ファイルが作成されていて、サイズが 0 より大きいことを確認すれば、音声が生成されたことを確認できます。

## 音声を認識するコードの追加

1. **voice-mail.py** コード ファイルで **transcribe_messages** 関数を見つけます。この関数を実装して、**messages** サブフォルダー内の各ボイスメッセージを文字起こしします。

    この関数には、**messages** フォルダー内のファイルを順に処理するコードがすでに含まれています。

1. **transcribe_messages** 関数の中で、コメント **音声ファイルを文字起こし** を見つけて、音声を文字起こしする以下のコードを追加します。

    ```python
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
    ```

    音声の入力は `AudioConfig(filename=...)` でファイルを指定しています。

    `SpeechRecognizer` は、言語を指定しないと英語（`en-US`）として認識するため、日本語のメッセージは、ローマ字風の文字列になり、正しく文字起こしされません。そこで、`AutoDetectSourceLanguageConfig` に候補の言語（`ja-JP` と `en-US`）を渡して、メッセージごとに言語を自動検出します。

    > **ヒント**: メッセージの言語が 1 つに決まっている場合は、`speech_config.speech_recognition_language = "ja-JP"` のように言語を指定して認識することもできます。

1. 変更を保存します。次に、ターミナルで次のコマンドを入力してアプリケーションを実行します。

    ```
    python voice-mail.py
    ```

1. プロンプトが表示されたら、**2** を入力してメッセージを文字起こしします。

1. 各メッセージの文字起こしを確認します。各ファイルは自動的に再生されるため、メッセージを聞くこともできます。

    **出力例**:

    ```output
    message_1.wav を文字起こししています...
    検出された言語: en-US
    文字起こし結果: Hi, this is Ava. Just calling to remind you about your appointment tomorrow. Call me back ON555123456 if you have any questions.

    message_2.wav を文字起こししています...
    検出された言語: en-US
    文字起こし結果: Hi, Adam here. Are you still on for coffee this afternoon?

    message_ja_1.wav を文字起こししています...
    検出された言語: ja-JP
    文字起こし結果: 田中です。明日のお約束の確認でお電話しました。折り返しをお願いします。

    message_ja_2.wav を文字起こししています...
    検出された言語: ja-JP
    文字起こし結果: もしもし、鈴木です。今日の午後コーヒーでもどうですか？
    ```

    > **注意**: `recognize_once_async` は、最初の 1 つの発話（長い無音があるところまで）を認識します。メッセージの途中に長い無音があると、その手前までしか文字起こしされません。`message_ja_1.wav` と `message_ja_2.wav` は、続けて話す 1 つの発話にしています。

    > **ヒント**: スピーカーが使えない環境では、`playsound(file_path)` の行でエラーが表示されて処理が止まることがあります。その場合は、**transcribe_messages** 関数の `playsound(file_path)` の行の先頭に `#` を付けてコメントアウトし、もう一度実行してください。

## クリーンアップ

この演習で使用した **Foundry プロジェクトとリソースは、後続の演習（05〜07）でも使用します。まだ削除しないでください。** リソースの削除は、**4 日目の演習 06「ナレッジ マイニング ソリューションの作成」の「クリーンアップ」**で、1〜4 日目の分をまとめて行います。

## 関連情報

**音声テキスト変換** API と **テキスト読み上げ** API の詳細については、[音声テキスト変換のドキュメント](https://learn.microsoft.com/azure/ai-services/speech-service/index-speech-to-text) と [テキスト読み上げのドキュメント](https://learn.microsoft.com/azure/ai-services/speech-service/index-text-to-speech) を参照してください。
