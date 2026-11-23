# 演習環境 構築ガイド（共通）

**対象**: AI-103 4日目「Azure のビジュアル データから分析情報を抽出する」の全演習（演習 01〜06）  
**作業ディレクトリ**: 各演習の Labfiles フォルダー内にある、Python フォルダー配下のアプリ フォルダー

> 本書は共通のリファレンスです。実際の手順は [演習 01](01-gen-ai-vision.md) から順に、各演習の手順書に従ってください。**1 日目の演習 01 で作成した Foundry プロジェクト（East US 2）は、1〜4 日目のすべての演習で共用します。** 4 日目では新しいプロジェクトを作成せず、1 日目の演習 01 でデプロイした gpt-5-mini モデル（TPM 10K）を、演習 01・03〜05 で使用します。

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

この日の演習では、Foundry と Content Understanding の操作を Web ブラウザーで行い、コードの編集と実行を VS Code で行います。VS Code では **Python** 拡張機能（Microsoft 製）を使用します。インストール済みでない場合は、拡張機能ビューからインストールしてください。

---

## 3. 共有リソースの方針（1〜4 日目で共用）

1〜4 日目の演習では、次のリソースを**共用**します。Foundry プロジェクトは 1 日目の演習 01 で作成し、4 日目の演習 06 のクリーンアップで、1〜4 日目の分をまとめて削除します。

| 項目 | 内容 | 作成する演習 | 使用する演習 |
|---|---|---|---|
| リソース グループ | 各自に割り当て済みの **AI103StudentXX**（XX は受講者番号）。新規作成はしません | （割り当て済み） | 1〜4 日目のすべて |
| Foundry プロジェクト | 例: **AI103-Lab01-YYYYMMDD-XX**（YYYYMMDD は実施日） | 1 日目 演習 01 | 4 日目 演習 01〜05（ほか 2・3 日目） |
| リージョン | **East US 2** | 1 日目 演習 01 | 4 日目 演習 01〜06（ほか 2・3 日目） |
| モデル（ビジョン対応チャット） | `gpt-5-mini`（デプロイ名も `gpt-5-mini`、TPM 10K） | 1 日目の 01 | 01、03、04、05 |
| モデル（画像生成） | `gpt-image-1-mini`（デプロイ名も `gpt-image-1-mini`） | 02 | 02 |
| Content Understanding のモデル | 既定のモデルとして構成される `gpt-5`・`gpt-5-mini`（1 日目にデプロイ済み）と、自動デプロイで作成される `text-embedding-3-large` | 03（または 04） | 03、04、05 |
| ストレージ アカウント | `ai103stgXXYYYYMMDD`（2 日目の演習 03 で作成したものを再利用。コンテナー `content-understanding`） | 2 日目の 03 | 03、04 |
| Content Understanding のプロジェクトとアナライザー | プロジェクト `Image analysis XX`、アナライザー `imageanalyzer01` | 03 | 03 |
| Azure AI Search とストレージ アカウント | `ai103searchXXYYYYMMDD`（Basic）、`ai103kmstgXXYYYYMMDD` | 06 | 06 |
| Content Understanding のアナライザー | 画像（03）、請求書・スライド・ボイスメール・会議（04）、名刺（05） | 03、04、05 | 各演習 |

演習 06（ナレッジ マイニング）は、専用の Azure AI Search リソースとストレージ アカウントが必要な**独立ラボ**です。

> **注意**: 4 日目の演習では、新しいプロジェクトを作成せず、1 日目の演習 01 で作成したプロジェクトを開いてください。

### リージョンに関する注意

- Azure Content Understanding（演習 03〜05）は、特定のリージョンでのみ利用できます。共用のプロジェクトは、1 日目の演習 01 で **East US 2** に作成します。
- `gpt-image-1-mini` の提供状況とクォータは、リージョンとサブスクリプションによって変わります。デプロイできない場合の代替は、[演習 01](01-gen-ai-vision.md) の「モデルのデプロイ」を参照してください。

---

## 4. Foundry プロジェクトを開く

プロジェクトは **1 日目の演習 01** で作成済みです。[演習 01](01-gen-ai-vision.md) の「共用の Foundry プロジェクトを開く」に従って、そのプロジェクトを開いてください。ソース コードは演習環境に配置済みです。

---

## 5. モデルのデプロイ

- 演習 01: 新しいモデルはデプロイしません。1 日目の演習 01 でデプロイした `gpt-5-mini`（TPM 10K）を使用します。[演習 01](01-gen-ai-vision.md) の「モデルの確認」に従ってください。
- 演習 02: `gpt-image-1-mini` を、カスタム設定（**[1 分あたりの要求レート制限]** を **3** に設定）でデプロイします。モデルの検索には `image` のキーワードを使用します。[演習 02](02-generate-image.md) の「モデルのデプロイ」に従ってください。
- 演習 03: Content Understanding Studio で Foundry リソースを接続し、**[自動デプロイを有効にする]** をオンにして、必要なモデルをデプロイします。

> **注意**: 演習 05 の `biz-card.json` は、完了モデルとして `gpt-5.2` を指定しています。この研修では、演習 05 の手順に従って `gpt-5-mini` に書き換えてから使用します（埋め込みモデルは `text-embedding-3-large`）。

---

## 6. エンドポイントの種類

演習によって、必要なエンドポイントの種類が異なります。**コピーするエンドポイントを間違えない**ように、次の表で確認してください。

| 種類 | 形式 | 使用する演習 |
|---|---|---|
| Azure OpenAI のエンドポイント | `https://<Foundry リソース名>.openai.azure.com/openai/v1`（演習 02 は末尾に `/` を付けます） | 01、02 |
| Foundry リソースのエンドポイント | `https://<Foundry リソース名>.services.ai.azure.com/` | 03、05 |
| Azure AI Search のエンドポイント | `https://<サービス名>.search.windows.net` | 06 |

> **ヒント**: 演習 03 と 05 では、プロジェクト エンドポイント（`/api/projects/...` を含む URL）や Azure OpenAI エンドポイントではなく、**Foundry リソースのエンドポイント**を使用します。

> **ヒント**: **Foundry リソース名** と **プロジェクト名** は別の名前です。プロジェクトのホーム ページの **[プロジェクト エンドポイント]**（`https://<Foundry リソース名>.services.ai.azure.com/api/projects/<プロジェクト名>`）で、ホスト名の先頭部分が Foundry リソース名、`/projects/` の後ろがプロジェクト名です。Foundry リソース名はプロジェクト名から推測できないため、必ずエンドポイントに表示された名前を、そのまま使用してください。

---

## 7. Python 仮想環境のセットアップ

演習ごとにフォルダーが分かれており、各演習のアプリ フォルダーに専用の仮想環境 (`labenv`) を使用します。

- **演習 01**: 受講者が自分で仮想環境を作成し、パッケージをインストールします。演習 01 のアプリ フォルダーをターミナルで開き、次を実行します。

    ```bash
    python -m venv labenv
    .\labenv\Scripts\Activate.ps1
    pip install -r requirements.txt
    ```

- **演習 02 ～ 06**: 時間を節約するため、`labenv` はあらかじめ構築済みで、必要なパッケージも事前インストール済みです (演習 05 の `azure-ai-contentunderstanding` を含む)。各演習の手順で `.\labenv\Scripts\Activate.ps1` を実行して有効化するだけで、`pip install` は不要です。

> **注意**: `Activate.ps1` が実行できない場合は、`Set-ExecutionPolicy -Scope Process Bypass` を実行してから、もう一度有効化します。

### 演習ごとの主なパッケージ

| 演習 | アプリ フォルダー | 主なパッケージ（requirements.txt） |
|---|---|---|
| 01 | `Python` | `openai`、`azure-identity` |
| 02 | `Python` | `openai`、`azure-identity`、`requests` |
| 03 | `Python` | `azure-ai-contentunderstanding`、`azure-identity` |
| 04 | （Python コードなし。ポータル中心） | ― |
| 05 | `Python` | `python-dotenv`（手順書の追加パッケージ: `azure-ai-contentunderstanding`） |
| 06 | `Python` | `azure-search-documents==11.6.0` |

---

## 8. .env ファイルの設定

各演習のアプリ フォルダーにある **.env** には、`your_...` 形式のプレースホルダーが入っています。手順書に従って、実際の値に置き換えて保存します（**Ctrl+S**）。

| 演習 | 変数 | 設定する値 |
|---|---|---|
| 01 | `ENDPOINT`、`MODEL_DEPLOYMENT` | Azure OpenAI のエンドポイント、`gpt-5-mini`（`.env` の既定値 `gpt-5.2` から書き換える） |
| 02 | `ENDPOINT`、`MODEL_DEPLOYMENT` | Azure OpenAI のエンドポイント、`gpt-image-1-mini` |
| 03 | `ENDPOINT`、`ANALYZER` | Foundry リソースのエンドポイント、画像アナライザーの名前 |
| 05 | `ENDPOINT`、`KEY`、`ANALYZER_NAME` | Foundry リソースのエンドポイント、API キー、`businesscardanalyzer` |
| 06 | `SEARCH_ENDPOINT`、`QUERY_KEY`、`INDEX_NAME` | 検索のエンドポイント、クエリ キー、`margies-index` |

> **注意**: キーや SAS などの秘密情報は、`.env` 以外のファイルに貼り付けたり、共有したりしないでください。

---

## 9. Azure 認証

```bash
az login
```

ブラウザーが開くので、Azure アカウントにサインインしてください。サインインのウィンドウは VS Code の裏側に表示されることがあります。複数のテナントがある場合は、`--tenant` パラメーターでテナントを指定します。

---

## 10. 動作確認

最初の演習（[演習 01](01-gen-ai-vision.md)）で次のコマンドを実行し、画像について質問して、モデルが応答することを確認します。

```bash
python image-chat-app.py
```

終了するには `quit` を入力します。

---

## クリーンアップ（演習終了後）

このプロジェクトとモデルは 1〜4 日目のすべての演習で共用します。**4 日目の演習 06 まですべて完了するまでは削除しないでください**。すべて完了したら、[演習 06](06-knowledge-mining.md) の「クリーンアップ」に従って、1〜4 日目のリソースをリソース グループごとまとめて削除してください。

---

## 仮想環境の終了

```bash
deactivate
```
