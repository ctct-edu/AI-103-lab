# AI-103 ラボマニュアル

## はじめに

本マニュアルはCTCテクノロジー主催「AI-103」（4日間コース）のラボマニュアルになります。

## マニュアルの見かた

講師の指示に従い、該当する日のフォルダーへ移動してください。
各フォルダー内の `Instructions` に、演習ごとのラボマニュアルが掲載されています。
ラボマニュアルに従って演習を実施してください。

| 日 | フォルダー | 内容 | 手順書 |
|---|---|---|---|
| 1日目 | [AI-103-01-Lab](AI-103-01-Lab/) | 生成 AI アプリの開発（AI-3016 ベース） | [Exercises](AI-103-01-Lab/Instructions/Exercises/) |
| 2日目 | [AI-103-02-Lab](AI-103-02-Lab/) | AI エージェントの開発（AI-3026 ベース） | [Exercises](AI-103-02-Lab/Instructions/Exercises/) |
| 3日目 | [AI-103-03-Lab](AI-103-03-Lab/) | 自然言語ソリューション（テキスト分析・音声・翻訳） | [Exercises](AI-103-03-Lab/Instructions/Exercises/) |
| 4日目 | [AI-103-04-Lab](AI-103-04-Lab/) | ビジュアル データ（画像・Content Understanding・ナレッジ マイニング） | [Exercises](AI-103-04-Lab/Instructions/Exercises/) |

## リソースの共用

Foundry リソースとプロジェクトは、**1〜4 日目で共用**します。

- **1 日目の演習 01** で、Foundry リソースとプロジェクトを **East US 2** に作成します。2 日目以降は、新しいプロジェクトを作成せず、このプロジェクトを開きます。
- リソースの削除（クリーンアップ）は、**4 日目の演習 06** で 1〜4 日目の分をまとめて 1 回だけ行います。途中の日では、リソース グループ（`AI103StudentXX`）やモデルを削除しないでください。
- **Foundry リソース名** と **プロジェクト名** は別の名前です。プロジェクトのホーム ページの **[プロジェクト エンドポイント]**（`https://<Foundry リソース名>.services.ai.azure.com/api/projects/<プロジェクト名>`）で、ホスト名の先頭部分がリソース名です。

## フォルダー構成

各日のフォルダーは共通して次の構成です。

| フォルダー | 内容 |
|---|---|
| `Instructions/` | 演習の手順書（Markdown）と画像 |
| `Labfiles/` | スターター コード（コメントの位置にコードを追加します） |
| `Labfiles_Ans/` | 完成形のコード |

## 出典

本リポジトリは、Microsoft Learning の MIT ライセンス教材（[Microsoft Learn](https://learn.microsoft.com/training/) のトレーニング パスに付随するリポジトリ）を元に作成されています。
