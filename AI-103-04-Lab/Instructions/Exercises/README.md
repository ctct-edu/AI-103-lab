# AI-103 4日目 ビジュアル データ — ラボ一覧

画像の枠: **赤枠** ＝ クリック・選択・確認する場所、**青枠** ＝ 入力する場所。

4日目のコースでは、Microsoft Foundry と Azure Content Understanding を使って、画像やドキュメント、音声、動画などのビジュアル データから分析情報を抽出するスキルを習得します。

---

## コース全体の流れ

```
00 環境構築ガイド（共通リファレンス）

01 ─┬─ 02
    └─ 03 ─┬─ 04
           └─ 05

06（独立ラボ）
```

> **1 日目の演習 01 で作成した Foundry プロジェクト（East US 2）は、1〜4 日目のすべての演習で共用します。** 4 日目では新しいプロジェクトを作成せず、1 日目の演習 01 でデプロイした gpt-5-mini モデル（TPM 10K）を、演習 01・03〜05 で使用します。  
> **演習 06 のみ独立したラボです**。専用の Azure AI Search リソースとストレージ アカウントが必要なため、共用プロジェクトを使用しません。最後の演習として、**1〜4 日目すべてのリソースのクリーンアップ**もここで実施します。

---

## ラボ一覧

| ラボ | タイトル | スライド | 前提 | 特記事項 |
|------|----------|----------|------|----------|
| **00** | [演習環境 構築ガイド（共通）](00-environment-setup.md) | ― | なし | 環境の全体像を示すリファレンス。実手順は演習 01 を参照 |
| **01** | [ビジョン対応チャット アプリの開発](01-gen-ai-vision.md) | S9 | 1 日目の演習 01 | **1 日目で作成した Foundry プロジェクト（East US 2）を開き、1 日目にデプロイした gpt-5-mini（TPM 10K）で画像入力を試す。03〜05 で共用** |
| **02** | [AI による画像の生成](02-generate-image.md) | S17 | 01 | `gpt-image-1-mini` をデプロイ（レート制限 3）。ビデオ生成（Sora 2）の演習は扱わない |
| **03** | [Azure Content Understanding による画像の分析](03-content-understanding-image.md) | S24 | 01 | Content Understanding Studio のセットアップ（gpt-5・gpt-5-mini を構成、text-embedding-3-large を自動デプロイ）。2 日目のストレージ アカウント `ai103stgXXYYYYMMDD` を再利用し、プロジェクト `Image analysis XX`・アナライザー `imageanalyzer01` を作成 |
| **04** | [マルチモーダル コンテンツからの情報の抽出](04-content-understanding-multimodal.md) | S31 | 01・03 | ポータル中心（Python コードなし）。請求書・スライド・音声・ビデオ |
| **05** | [Content Understanding クライアント アプリケーションの開発](05-content-understanding-api.md) | S35 | 01・03 | `biz-card.json` の完了モデル（既定 `gpt-5.2`）を `gpt-5-mini` に書き換えて使用（埋め込みは `text-embedding-3-large`）。API キーを使用 |
| **06** | [ナレッジ マイニング ソリューションの作成](06-knowledge-mining.md) | S43 | なし | **独立ラボ**: 専用の Azure AI Search `ai103searchXXYYYYMMDD`（Basic。時間課金）とストレージ アカウント `ai103kmstgXXYYYYMMDD` を作成。**1〜4 日目すべてのリソースのクリーンアップはここで実施** |

---

## 共通の事前準備

必要なソフトウェア、リソース グループ（**AI103StudentXX**）、サインインなどの事前準備は、[演習環境 構築ガイド（共通）](00-environment-setup.md) を参照してください。
