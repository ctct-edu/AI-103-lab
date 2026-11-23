# AI-103 3日目 演習教材 — Azure で自然言語ソリューションを開発する

AI-103 コースの 3 日目で使用する演習教材です。テキストの分析、エージェントと MCP、音声対応の生成 AI、Azure Speech、Voice Live、翻訳の演習を、日本語の手順書とスターター コードで進めます。

- 必要な環境: Windows、Visual Studio Code、Python 3.13 以降

## マニュアルの見かた

| 知りたいこと | 開くファイル |
|---|---|
| 演習の全体像と依存関係 | [ラボ一覧](Instructions/Exercises/README.md) |
| 環境の準備、共用リソース、エンドポイントの種類 | [演習環境 構築ガイド（共通）](Instructions/Exercises/00-environment-setup.md) |
| 各演習の手順 | [Instructions/Exercises](Instructions/Exercises/) の `01-analyze-text.md` 〜 `07-translation.md` |
| スターター コード（コメントの位置にコードを追加します） | [Labfiles](Labfiles/) |
| 完成形のコード（マイクなしの別解 `translate-speech_file.py` を含む） | [Labfiles_Ans](Labfiles_Ans/) |

## 演習の進めかた

1. [演習環境 構築ガイド](Instructions/Exercises/00-environment-setup.md) を読みます。
1. 1 日目の演習 01 で作成した Foundry プロジェクトを開きます（3 日目では新しいプロジェクトを作成せず、1〜4 日目で共用します）。
1. 各演習の手順書に従い、スターター コードのコメント位置にコードを追加して実行します。
1. 行き詰まったら、`Labfiles_Ans` の完成形と比較します。
1. 3 日目の演習 07 が終わっても、リソースは削除しません。リソースの削除は、4 日目の演習 06 の「クリーンアップ」でまとめて行います。

## 出典

この教材は、Microsoft Learning の MIT ライセンスの教材（`mslearn-ai-language`）を元にした、CTC テクノロジーの演習教材です。出典の詳細と、元の演習との対応は [SOURCES.md](SOURCES.md) を、ライセンスは [LICENSE](LICENSE) を参照してください。

> **注意**: 本教材の作成時点では、Azure 上での動作確認と画面キャプチャの撮影は行っていません。
