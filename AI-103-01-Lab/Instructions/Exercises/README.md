# 1 日目 ラボ一覧

画像の枠: **赤枠** ＝ クリック・選択・確認する場所、**青枠** ＝ 入力する場所。

> **1 日目の演習 01 で作成する Foundry リソースとプロジェクト（East US 2）、およびデプロイする gpt-5-mini・gpt-5（いずれも TPM 10K）は、1〜4 日目のすべての演習で共用します。** 4 日目の演習 06 の「クリーンアップ」まで削除しないでください。

| ラボ | タイトル | 前提 | 特記事項 |
|------|----------|------|----------|
| **01** | [AI 開発プロジェクトの準備](01-explore-ai-studio.md) | なし | Foundry リソース `AI103-Lab01-YYYYMMDD-XX-resource` とプロジェクト `AI103-Lab01-YYYYMMDD-XX` を作成し、gpt-5-mini（TPM 10K）をデプロイ |
| **02** | [モデルの探索と比較](02-model-catalog-evaluation.md) | 01 | gpt-5（TPM 10K）を追加でデプロイし、gpt-5-mini と比較・評価。評価の完了まで 30〜45 分程度かかることがある |
| **03** | [生成 AI チャット アプリを作成する](03-foundry-sdk.md) | 01 | Azure OpenAI エンドポイントと gpt-5-mini を使用 |
| **04a** | [ツールを使用する生成 AI アプリを作成する](04a-use-own-data.md) | 01 | プレイグラウンドで Web 検索ツールを試す |
| **06** | [ガードレールを適用して有害なコンテンツの出力を防ぐ](06-explore-content-filters.md) | 01 | カスタム ガードレール `ai103-strict-guardrail-XX` を gpt-5-mini に適用 |
