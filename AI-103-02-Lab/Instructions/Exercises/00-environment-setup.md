# 演習環境 構築ガイド（共通）

**対象演習**: AI エージェントでのカスタム関数の使用  
**作業ディレクトリ**: `Labfiles/01-agent-custom-tools/Python/`

> 本書は演習環境の全体像を示すリファレンスです。実際の手順は [演習 01](01-agent-custom-tools.md) に従ってください。**1 日目の演習 01 で作成した Foundry プロジェクト（East US 2）は、1〜4 日目のすべての演習で共用します。** 1 日目の演習 01 でデプロイした gpt-5-mini モデル（TPM 10K）を、2 日目の演習 01・02・04・05 で使用します。

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

Foundry Toolkit 拡張機能（Microsoft 製）は演習環境にインストール済みです。インストール作業は不要です。

> **注意**: 一部の UI では **AI Toolkit** と表示される場合がありますが、同じ拡張機能です。

---

## 3. Foundry プロジェクトの設定

新しいプロジェクトは作成しません。**1 日目の演習 01** で作成したプロジェクトを、[演習 01](01-agent-custom-tools.md) の「VS Code 用 Foundry Toolkit 拡張機能での Foundry プロジェクトの設定」に従って、Foundry Toolkit の既定のプロジェクトとして設定してください。ソース コードは演習環境に配置済みのため、クローンは不要です。

---

## 4. gpt-5-mini モデルのデプロイ

gpt-5-mini は **1 日目の演習 01 で TPM（1 分あたりのトークン数）10K（10,000）でデプロイ済み**です。[演習 01](01-agent-custom-tools.md) の「モデルのデプロイ」で、そのデプロイが使えることを確認してください（新しくデプロイする必要はありません。デプロイしていない場合だけ、TPM を **10K（10000）** にしてデプロイします）。

---

## 5. プロジェクト エンドポイントのコピー

1. Foundry Toolkit ペインの **[MY RESOURCES]** に表示されたプロジェクト名の横にある歯車アイコンを選択
2. **[Copy Project Endpoint]** を選択してクリップボードにコピー

> このURL は次のステップで `.env` ファイルに設定します。

---

## 6. Python 仮想環境のセットアップ

`Labfiles/01-agent-custom-tools/Python/` フォルダーをターミナルで開き、以下を実行します。

```bash
python -m venv labenv
.\labenv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### インストールされるパッケージ（requirements.txt）

| パッケージ | 用途 |
|---|---|
| `python-dotenv` | `.env` ファイルの読み込み |
| `azure-identity` | Azure 認証 |
| `azure-ai-projects==2.0.0b4` | Azure AI Foundry SDK |
| `openai` | OpenAI クライアント |

---

## 7. .env ファイルの設定

`Labfiles/01-agent-custom-tools/Python/.env` を開き、以下を設定します。

```
PROJECT_ENDPOINT="<手順 5 でコピーしたエンドポイント URL>"
MODEL_DEPLOYMENT_NAME="gpt-5-mini"
```

**Ctrl+S** で保存してください。

---

## 8. Azure 認証

```bash
az login
```

ブラウザが開くので Azure アカウントにサインインしてください。

---

## 9. 動作確認

```bash
python agent.py
```

以下のプロンプトを入力してエージェントが応答することを確認します。

```
南米から見える次の天文イベントを教えてください。また、通常優先度でプレミアム望遠鏡を 5 時間使用した場合のコストも教えてください。
```

期待される出力例:

```
AGENT: 南米から観測できる次の天文イベントは Jupiter-Venus Conjunction で、5月1日に起こります。
通常優先度のプレミアム望遠鏡 5 時間の観測コストは $1,875 です。
```

終了するには `quit` を入力します。

---

## クリーンアップ（演習終了後）

このプロジェクトとモデルは 1〜4 日目のすべての演習で共用します。**4 日目の演習 06 まですべて完了するまでは削除しないでください**。すべて完了したら、4 日目の演習 06「ナレッジ マイニング ソリューションの作成」の「クリーンアップ」に従って、1〜4 日目のリソースをまとめて削除してください。

---

## 仮想環境の終了

```bash
deactivate
```
