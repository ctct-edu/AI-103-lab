# AI-103 4日目 演習教材 — Azure のビジュアル データから分析情報を抽出する

AI-103 コースの 4 日目で使用する演習教材です。ビジョン対応のチャット、画像の生成、Azure Content Understanding（画像・ドキュメント・音声・ビデオ）、ナレッジ マイニングの演習を、日本語の手順書とスターター コードで進めます。

- 必要な環境: Windows、Visual Studio Code、Python 3.13 以降

## マニュアルの見かた

| 知りたいこと | 開くファイル |
|---|---|
| 演習の全体像と依存関係 | [ラボ一覧](Instructions/Exercises/README.md) |
| 環境の準備、共用リソース、エンドポイントの種類 | [演習環境 構築ガイド（共通）](Instructions/Exercises/00-environment-setup.md) |
| 各演習の手順 | [Instructions/Exercises](Instructions/Exercises/) の `01-gen-ai-vision.md` 〜 `06-knowledge-mining.md` |
| スターター コード（コメントの位置にコードを追加します）とデータ | [Labfiles](Labfiles/) |
| 完成形のコード（URL 画像版の別解 `image-chat-app_url.py` を含む） | [Labfiles_Ans](Labfiles_Ans/) |

## 演習の進めかた

1. [演習環境 構築ガイド](Instructions/Exercises/00-environment-setup.md) を読みます。
1. 演習 01 で、1 日目で作成した Foundry プロジェクトを開き、gpt-5.2 モデルをデプロイします（4 日目では新しいプロジェクトを作成せず、1〜4 日目で共用します。gpt-5.2 は演習 02〜05 でも使用します）。
1. 各演習の手順書に従い、スターター コードのコメント位置にコードを追加して実行します。
1. 行き詰まったら、`Labfiles_Ans` の完成形と比較します。
1. すべての演習が終わったら、演習 06 の「クリーンアップ」で、1〜4 日目のリソースをまとめて削除します。

## 出典

この教材は、Microsoft Learning の MIT ライセンスの教材（`mslearn-ai-vision` と `mslearn-ai-information-extraction`）を元にした、CTC テクノロジーの演習教材です。出典の詳細と、元の演習との対応は [SOURCES.md](SOURCES.md) を、ライセンスは [LICENSE](LICENSE)（`mslearn-ai-vision`）と [LICENSE-information-extraction](LICENSE-information-extraction)（`mslearn-ai-information-extraction`）を参照してください。

> **注意**: 本教材の作成時点では、Azure 上での動作確認と、実機での画面キャプチャの撮影は行っていません。
