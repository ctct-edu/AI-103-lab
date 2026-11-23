# 演習環境 構築ガイド（共通）

**対象**: AI-103 3日目「Azure で自然言語ソリューションを開発する」の全演習（演習 01〜07）  
**作業ディレクトリ**: 各演習の Labfiles フォルダー内にある、Python フォルダー配下のアプリ フォルダー

> 本書は共通のリファレンスです。実際の手順は [演習 01](01-analyze-text.md) から順に、各演習の手順書に従ってください。**1 日目の演習 01 で作成した Foundry プロジェクト（East US 2）は、1〜4 日目のすべての演習で共用します。** 3 日目では、新しいプロジェクトを作成しません。

---

## 1. 必要なソフトウェアのインストール

以下のソフトウェアがインストールされていることを確認してください（演習環境にはインストール済みです）。

| ソフトウェア | バージョン | ダウンロード |
|---|---|---|
| Visual Studio Code | 最新版 | https://code.visualstudio.com/ |
| Python | **3.13 以上**（3.13.12 で動作確認済み） | https://www.python.org/downloads/ |
| Azure CLI | 最新版 | https://learn.microsoft.com/cli/azure/install-azure-cli |

### バージョン確認コマンド

```bash
python --version
az --version
```

---

## 2. VS Code 拡張機能

この日の演習では、Foundry の操作を Web ブラウザーの Microsoft Foundry ポータル（`https://ai.azure.com`）で行い、コードの編集と実行を VS Code で行います。VS Code では **Python** 拡張機能（Microsoft 製）を使用します。インストール済みでない場合は、拡張機能ビューからインストールしてください。

---

## 3. 共有リソースの方針（1〜4 日目で共用）

1〜4 日目の演習では、次のリソースを**共用**します。1 日目の演習 01 で作成し、4 日目の演習 06 のクリーンアップでまとめて削除します。3 日目の途中では削除しません。

| 項目 | 内容 | 作成する演習 | 使用する演習 |
|---|---|---|---|
| リソース グループ | 各自に割り当て済みの **AI103StudentXX**（XX は受講者番号）。新規作成はしません | （割り当て済み） | 1〜4 日目のすべて |
| Foundry プロジェクト | 例: **AI103-Lab01-YYYYMMDD-XX**（YYYYMMDD は実施日） | 1 日目 演習 01 | 3 日目 演習 01〜07（ほか 2・4 日目） |
| リージョン | **East US 2** | 1 日目 演習 01 | 3 日目 演習 01〜07（ほか 2・4 日目） |
| モデル（音声） | `gpt-4o-mini-tts`、`gpt-4o-mini-transcribe` | 03 | 03 |
| エージェント用のチャット モデル | `gpt-5-mini`（1 日目の演習 01 でデプロイ済み、TPM 10K。エージェントの作成時に既定で選ばれる gpt-5 から変更） | 1 日目の 01 | 02、05、06 |
| エージェント | `Text-Analysis-Agent`（02）、`speech-agent`（05）、`chat-agent`（06） | 02、05、06 | 各演習 |
| ストレージ アカウント | `ai103stgXXYYYYMMDD`（2 日目の演習 03 で作成したものを再利用）の `files` コンテナーと SAS URL | 2 日目の 03（コンテナーは 05） | 05 |
| MCP ツールの接続 | `azure-language-tool-XX`（02）、`azure-speech-tool-XX`（05） | 02、05 | 02、05 |

> **注意**: 3 日目の演習では、新しいプロジェクトを作成せず、1 日目の演習 01 で作成したプロジェクトを開いてください。

### リージョンに関する注意

- 演習 03 の音声モデルは **East US 2** で提供されるバージョンとデプロイの種類に基づいています。そのため、共用のプロジェクトは、1 日目の演習 01 で **East US 2** に作成します。
- 演習 02・05・06 は、Foundry Agent Service の MCP ツールを使用するため、**West US 3 以外**のリージョンで実施します。
- モデルの提供状況とクォータは、リージョンとサブスクリプションによって変わります。

---

## 4. Foundry プロジェクトを開く

プロジェクトは **1 日目の演習 01** で作成済みです。[演習 01](01-analyze-text.md) の「共用の Foundry プロジェクトを開く」に従って、そのプロジェクトを開いてください。ソース コードは演習環境に配置済みです。

---

## 5. モデルのデプロイ

- 演習 03: `gpt-4o-mini-tts` と `gpt-4o-mini-transcribe` を、カスタム設定（TPM は 5K）でデプロイします。[演習 03](03-gen-ai-speech.md) の「モデルのデプロイ」に従ってください。
- 演習 02・05・06: エージェントで使用するチャット モデルには、1 日目の演習 01 でデプロイした `gpt-5-mini`（TPM 10K）を選択します（新しくデプロイする必要はありません）。

---

## 6. エンドポイントの種類

演習によって、必要なエンドポイントの種類が異なります。**コピーするエンドポイントを間違えない**ように、次の表で確認してください。

| 種類 | 形式 | 使用する演習 |
|---|---|---|
| Foundry リソースのエンドポイント | `https://<Foundry リソース名>.services.ai.azure.com` | 01、06 |
| Foundry プロジェクトのエンドポイント | `https://<Foundry リソース名>.services.ai.azure.com/api/projects/<プロジェクト名>` | 02、05 |
| Cognitive Services のエンドポイント | `https://<Foundry リソース名>.cognitiveservices.azure.com/` | 04、07 |
| Azure OpenAI（モデル デプロイ）のエンドポイント | `https://<Foundry リソース名>.openai.azure.com/` | 03 |

> **ヒント**: **Foundry リソース名** と **プロジェクト名** は別の名前です。プロジェクトのホーム ページの **[プロジェクト エンドポイント]**（`https://<Foundry リソース名>.services.ai.azure.com/api/projects/<プロジェクト名>`）で、ホスト名の先頭部分が Foundry リソース名、`/projects/` の後ろがプロジェクト名です。Foundry リソース名はプロジェクト名から推測できないため、必ずエンドポイントに表示された名前を、そのまま使用してください。MCP ツール（演習 02・05）の `foundry-resource-name` にも、プロジェクト名ではなくこの Foundry リソース名を入力します。

---

## 7. Python 仮想環境のセットアップ

演習ごとにフォルダーが分かれており、各演習のアプリ フォルダーに専用の仮想環境 (`labenv`) を使用します。

- **演習 01**: 受講者が自分で仮想環境を作成し、パッケージをインストールします。演習 01 のアプリ フォルダーをターミナルで開き、次を実行します。

    ```bash
    python -m venv labenv
    .\labenv\Scripts\Activate.ps1
    pip install -r requirements.txt
    ```

- **演習 02 ～ 07**: 時間を節約するため、`labenv` はあらかじめ構築済みで、必要なパッケージも事前インストール済みです。各演習の手順で `.\labenv\Scripts\Activate.ps1` を実行して有効化するだけで、`pip install` は不要です。

> **注意**: `Activate.ps1` が実行できない場合は、`Set-ExecutionPolicy -Scope Process Bypass` を実行してから、もう一度有効化します。

### 演習ごとの主なパッケージ

| 演習 | アプリ フォルダー | 主なパッケージ（requirements.txt） |
|---|---|---|
| 01 | `text-analysis` | `azure-ai-textanalytics==5.3.0`、`azure-identity` |
| 02 | `text-agent` | `azure-ai-projects==2.0.0b4`、`openai<3`、`azure-identity` |
| 03 | `generate-speech`、`transcribe-speech` | `openai`、`azure-identity`、`playsound3` |
| 04 | `voice-mail` | `azure-cognitiveservices-speech==1.48.2`、`azure-identity`、`playsound3` |
| 05 | `speech-client` | `azure-ai-projects==2.0.0b4`、`openai<3`、`azure-identity` |
| 06 | `chat-client` | `aiohttp`、`pyaudio`（手順書の追加パッケージ: `azure-ai-voicelive`、`azure-ai-projects`） |
| 07 | `translators` | `azure-ai-translation-text==1.0.1`、`azure-cognitiveservices-speech==1.48.2` |

---

## 8. .env ファイルの設定

各演習のアプリ フォルダーにある **.env** には、`your_...` 形式のプレースホルダーが入っています。手順書に従って、実際の値に置き換えて保存します（**Ctrl+S**）。

| 演習 | 変数 | 設定する値 |
|---|---|---|
| 01 | `FOUNDRY_ENDPOINT` | Foundry リソースのエンドポイント（`/api/projects/...` を除く） |
| 02 | `FOUNDRY_ENDPOINT`、`AGENT_NAME` | プロジェクトのエンドポイント、`Text-Analysis-Agent` |
| 03 | `MODEL_ENDPOINT`、`MODEL_NAME` | Azure OpenAI のエンドポイント、モデルのデプロイ名 |
| 04 | `FOUNDRY_ENDPOINT` | Cognitive Services のエンドポイント |
| 05 | `FOUNDRY_ENDPOINT`、`AGENT_NAME` | プロジェクトのエンドポイント、`speech-agent` |
| 06 | `AZURE_VOICELIVE_ENDPOINT`、`AZURE_VOICELIVE_PROJECT_NAME`、`AZURE_VOICELIVE_AGENT_ID` | Foundry リソースのエンドポイント、プロジェクト名、`chat-agent` |
| 07 | `FOUNDRY_ENDPOINT` | Cognitive Services のエンドポイント |

> **注意**: キー、SAS URL などの秘密情報は、`.env` を含めてファイルに保存した内容を共有しないでください。

---

## 9. Azure 認証

```bash
az login
```

ブラウザーが開くので、Azure アカウントにサインインしてください。サインインのウィンドウは VS Code の裏側に表示されることがあります。複数のテナントがある場合は、`--tenant` パラメーターでテナントを指定します。

---

## 10. 動作確認

最初の演習（[演習 01](01-analyze-text.md)）で次のコマンドを実行して、`reviews` フォルダー内の各レビューの言語・エンティティ・PII が表示されることを確認します。

```bash
python text-analysis.py
```

---

## クリーンアップ（演習終了後）

このプロジェクトとモデルは 1〜4 日目のすべての演習で共用します。**3 日目の演習 07 が終わっても、削除しないでください**（4 日目の演習が残っています）。リソースの削除は、4 日目の演習 06「ナレッジ マイニング ソリューションの作成」の「クリーンアップ」に従って、1〜4 日目のリソースをまとめて削除してください。

---

## 仮想環境の終了

```bash
deactivate
```
