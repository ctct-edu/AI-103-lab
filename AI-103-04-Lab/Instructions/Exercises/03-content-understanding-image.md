---
lab:
    title: 'Azure Content Understanding による画像の分析'
    description: 'Azure Content Understanding を使用して画像を分析し、説明的なメタデータを生成する方法を学ぶ。'
    level: 300
    duration: 35
    islab: true
    status: 'released'
---

# Azure Content Understanding による画像の分析

Foundry Tools の Azure Content Understanding は、生成 AI を使用して、ドキュメント、画像、音声、ビデオなど、さまざまな種類の非構造化コンテンツを分析し、ユーザー定義のスキーマに従った構造化された出力を生成する機能です。

画像は、説明的なメタデータがないと検索や整理が困難です。この演習では、Content Understanding Studio で画像アナライザーを作成し、サンプル画像から、インデックス作成と検索のメタデータとして使用できる説明を生成します。

この演習の所要時間は約 **35** 分です。

> **注意**: この演習で使用する一部のテクノロジーはプレビュー中または開発中のため、予期しない動作、警告、またはエラーが発生する場合があります。

## 前提条件

この演習を完了するには、次のものが必要です。

- [演習 01](01-gen-ai-vision.md) の完了（Foundry プロジェクトとモデルを共用します）
- Visual Studio Code、Python 3.13 以降、Azure CLI（演習環境にはインストール済みです）

## 共用の Foundry プロジェクトの確認

1 日目の演習 01 で作成した **East US 2** の Foundry プロジェクト（4 日目の演習 01 で開いたもの）を使用します。East US 2 が [Azure Content Understanding がサポートするリージョン](https://learn.microsoft.com/azure/ai-services/content-understanding/language-region-support#region-support) に含まれている必要があります。

1. Web ブラウザーで [Microsoft Foundry ポータル](https://ai.azure.com)（`https://ai.azure.com`）を開き、1 日目の演習 01 で作成したプロジェクト（例: **AI103-Lab01-YYYYMMDD-XX**）のホーム ページを表示して、プロジェクトの詳細を確認します。
## Azure ストレージ アカウントの確認

Azure Content Understanding で分析するコンテンツ資産のために、Azure ストレージ アカウントが必要です。この研修では、**2 日目の演習 03 で作成したストレージ アカウント `ai103stgXXYYYYMMDD`**（XX は自分の番号、YYYYMMDD は 2 日目の日付）を再利用します。新しいストレージ アカウントを作成する必要はありません。

> **注意**: このストレージ アカウントは、[演習 04](04-content-understanding-multimodal.md) でも使用します。演習 06 のクリーンアップまで削除しないでください。Content Understanding は専用の新しいコンテナー（`content-understanding`）にデータを保存するため、他の演習で作成したコンテナー（2 日目の演習 03 の `contosoproducts`、3 日目の演習 05 の `files` など）には影響しません。

1. 新しいブラウザー タブで [Azure ポータル](https://portal.azure.com)（`https://portal.azure.com`）を開き、リソース グループ（**AI103StudentXX**）に、ストレージ アカウント **ai103stgXXYYYYMMDD**（East US 2）があることを確認します。

    > **注意**: 2 日目の演習 03 でストレージ アカウントを作成していない場合だけ、リソース グループに次の設定で新しい **ストレージ アカウント** リソースを作成し、作成されるまで待ちます。
    >
    > - **ストレージ アカウント名**: `ai103stgXXYYYYMMDD`（小文字と数字のみ。使用済みの場合は末尾に数字を付けます）
    > - **リージョン**: Foundry リソースと同じリージョン（East US 2）
    > - **主要サービス**: Azure Blob Storage または Azure Data Lake Storage Gen 2
    > - **パフォーマンス**: Standard
    > - **冗長性**: ローカル冗長ストレージ (LRS)

## Azure Content Understanding での画像アナライザーの作成

1. 新しいブラウザー タブで [Content Understanding Studio](https://contentunderstanding.ai.azure.com/home)（`https://contentunderstanding.ai.azure.com/home`）に移動し、メッセージが表示されたら Azure の資格情報でサインインします。

    > **注意**: Content Understanding Studio の画面は英語で表示されます。

1. 右上の **設定**（Settings、歯車）アイコンを選択して、Azure Content Understanding のアカウント設定を表示します。

1. **[Setup Azure resource]**（Azure リソースのセットアップ）ページで、**[Add resource]**（リソースの追加）ボタンを選択します。

    ![Content Understanding Studio の [Setup Azure resource] ページのスクリーンショット。赤枠は設定（歯車）アイコンと [Add resource] ボタン。](../Media/d4e03-01-cu-settings-add-resource.png)

1. **[Set up your default resource]** ダイアログの **[Select resource]** で、サブスクリプション、リソース グループ（**AI103StudentXX**）、Foundry リソース（例: **AI103-Lab01-YYYYMMDD-XX-resource**）を選択します。

1. **[Enable auto-deployment for required models if no default deployment available]**（既定のデプロイが利用できない場合、必要なモデルの自動デプロイを有効にする）チェック ボックスがオンになっていることを確認し（既定でオン）、**[Next]** を選択します。

    ![[Set up your default resource] ダイアログのスクリーンショット。赤枠は [Resource group name]、[Resource name]、自動デプロイのチェック ボックス、[Next] ボタン。](../Media/d4e03-02-cu-select-foundry-resource.png)

1. **[Review configuration]** で、**[Model deployment]** のチャット完了モデル（**gpt-5**、**gpt-5-mini**。1 日目にデプロイ済み）と、埋め込みモデル（**text-embedding-3-large**）が **Auto-configured** になっていることを確認し、**[Save]** を選択します。

    ![[Review configuration] のスクリーンショット。赤枠は [Model deployment] のチャット完了モデルと埋め込みモデル、[Save] ボタン。](../Media/d4e03-03-cu-review-models.png)

    デプロイ処理には数分かかる場合があります（text-embedding-3-large がデプロイされます）。処理が終わると、接続済みのリソースとして自分の Foundry リソースが表示されます。

    ![[Setup Azure resource] ページのスクリーンショット。赤枠は接続済みの Foundry リソースと、チャット完了モデル（gpt-5、gpt-5-mini）・埋め込みモデル（text-embedding-3-large）。](../Media/d4e03-04-cu-connected-resource.png)

    > **ヒント**: このリソースの接続は、演習 04・05 でも使用します。すでに接続済みの場合は、この手順をやり直す必要はありません。

1. メニュー バーで **[Build]**（構築）を選択し、**[Create]**（作成）ボタンを選択します。

    ![[Build] ページのスクリーンショット。赤枠はメニュー バーの [Build] と [Create] ボタン。](../Media/d4e03-05-cu-build-create-project.png)

1. **[Create a new project]** ダイアログで、次の設定を入力します。
    - **Project name**（プロジェクト名）: `Image analysis XX`（XX は自分の番号）
    - **Description**（説明）: `Image analysis project`
    - **Workflow kind**（プロジェクトの種類）: **Extract content and field with custom schema**（既定）

    ![[Create a new project] ダイアログのスクリーンショット。青枠は [Project name] と [Description]、赤枠は [Extract content and field with custom schema]。](../Media/d4e03-06-cu-new-project-name.png)

1. ダイアログを下にスクロールして **[Advanced settings]** を展開し、次のように設定して **[Create]** を選択します。
    - **Storage account**: `ai103stgXXYYYYMMDD`
    - **Blob container**: **[Create a new container]** を選択し、`content-understanding` と入力して **[OK]**（一覧に **(new) content-understanding** と表示されます）
    - **Chat completion model**: **gpt-5-mini**（既定の gpt-5 から変更します）

    ![[Advanced settings] のスクリーンショット。赤枠は [Storage account]、[Blob container] の (new) content-understanding、[Chat completion model] の gpt-5-mini、[Create] ボタン。](../Media/d4e03-07-cu-new-project-storage-model.png)

1. プロジェクトが作成されたら、演習環境に配置済みの **lion.jpg**（`Labfiles/03-content-understanding-image` フォルダー）を、**[Browse for files]** を使用して Content Understanding プロジェクトにアップロードします。

1. **[Choose a template]** ダイアログで **[Image Analysis]** が選択され、スキーマが **[Start From Scratch]** になっていることを確認して、**[Save]** を選択します。

    ![[Choose a template] ダイアログのスクリーンショット。赤枠は [Image Analysis]、Start From Scratch、[Save] ボタン。](../Media/d4e03-08-cu-choose-template.png)

1. **[Schema]** ペインで **[Add new field]** を使用して、スキーマに次のフィールドを追加します。

    | フィールド名 | フィールドの説明 | 値の型 | メソッド |
    |--|--|--|--|
    | `Description` | `Image description` | String | Generate |
    | `Tags` | `Image tags` | List of Strings | Generate |

    > **注意**: フィールド名（`Description` と `Tags`）は、このあとのアプリケーション コードが参照する名前です。大文字と小文字も含めて、この表のとおりに入力してください。

    > **ヒント**: フィールド名を入力して Tab キーを押すと、[Field Description] にフィールド名の小文字が自動で入ります。表のとおりの説明に書き換えてください。

1. **[Save]** を選択して、スキーマへの変更を保存します。

    ![[Schema] ペインのスクリーンショット。赤枠は [Add new field]、値の型とメソッド、[Save] ボタン、青枠はフィールド名と説明。](../Media/d4e03-09-cu-schema-fields.png)

1. **[Run analysis]** を選択して画像に対してアナライザーを実行し、**[Test]** タブの **[Fields]** で生成されたフィールドを確認します。画像の正確な説明と、関連するタグのコレクションが含まれているはずです。

    ![[Run analysis] の結果のスクリーンショット。赤枠は [Run analysis] ボタンと、生成された Description と Tags。](../Media/d4e03-10-cu-run-analysis-result.png)

1. アナライザーがフィールドに正確な値を返したことに満足したら、**[Build analyzer]** を選択し、**[Name]** に `imageanalyzer01`、**[Description]** に `Image analyzer` のような説明を入力して **[Build]** を選択します。

    ![[Build a Content Understanding analyzer] ダイアログのスクリーンショット。赤枠は [Build analyzer] と [Build] ボタン、青枠は [Name] と [Description]。](../Media/d4e03-11-cu-build-analyzer.png)

    > **ヒント**: アプリケーション コードでアナライザーを識別するために、この名前（`imageanalyzer01`）があとで必要になります。

1. **Built successfully** と表示されたら **[Jump to analyzer list]** を選択して、アナライザーの一覧（**[Analyzer list]**）に移動し、一覧に表示され、[Status] が **Ready** であることを確認します。

1. 一覧で自分のアナライザーを選択して開き、**[Code Example]**（コード例）タブを表示して、アナライザーを使用するために必要なコードを確認します。

    ![アナライザーの [Code Example] タブのスクリーンショット。赤枠は [Code Example] タブと言語の Python。リソース キーは黒塗り。](../Media/d4e03-12-cu-analyzer-code-example.png)

1. Python のコード例を確認します。**main** 関数で、Content Understanding リソースの **エンドポイント** に注目してください。次のような形式になっているはずです。

    ```
    https://{Foundry リソース名}.services.ai.azure.com/
    ```

1. コード例の下に **リソース キー** が表示されています。この演習では、キーではなく Microsoft Entra ID 認証を使用します。

## 画像アナライザー アプリケーションの作成

### スターター コードを開く

アプリケーションの初期ファイルは、演習環境に配置済みです。

1. Visual Studio Code を開きます。

1. **[ファイル] > [フォルダーを開く]** を選択し、配置済みの `Labfiles/03-content-understanding-image` フォルダーを開きます。

### アプリケーションの構成の準備

1. VS Code のエクスプローラー ペインで **Python** フォルダーを展開し、フォルダー内のファイルを確認します。

    - `.env` - アプリケーション設定の構成ファイル
    - `analyze-image.py` - 画像アナライザー アプリケーションの Python コード ファイル
    - `requirements.txt` - パッケージの依存関係を一覧にしたファイル
    - `images` - 分析用の画像を含むフォルダー

1. **Python** フォルダーを右クリックし、**[統合ターミナルで開く]** を選択します。ターミナルが **Python** フォルダーで開いていることを確認します。

1. ターミナルで次のコマンドを入力して、演習用にあらかじめ構築済みの仮想環境 (`labenv`) を有効化します。

    ```
    .\labenv\Scripts\Activate.ps1
    ```

    > **注意**: 必要な Python パッケージは `labenv` に事前インストール済みです。`pip install` を再実行する必要はありません。

1. **.env** ファイルを開き、リソースの **エンドポイント** の値（Content Understanding Studio のコード例からコピーしたもの）と、アナライザーの名前で更新します。

    > **重要**: 必ず `https://{リソース名}.services.ai.azure.com` の形式の Foundry リソース エンドポイントを指定してください。プロジェクト エンドポイントや Azure OpenAI エンドポイントでは <u>ありません</u>。

    変更後、**Ctrl+S** キーを押して構成ファイルを保存します。

### 画像を分析して説明を生成するコードの記述

1. VS Code で `analyze-image.py` ファイルを開きます。

1. コメント **参照の追加** を見つけて、必要なインポートの以下のコードを追加します。

    ```python
    # 参照の追加
    from azure.ai.contentunderstanding import ContentUnderstandingClient
    from azure.ai.contentunderstanding.models import AnalysisInput, AnalysisResult
    from azure.core.exceptions import AzureError
    from azure.identity import DefaultAzureCredential
    ```

1. **main** 関数では、環境ファイルから構成値を取得するコードが用意されています。

1. コメント **Content Understanding クライアントをセットアップ** を見つけて、以下のコードを追加します。

    ```python
    # Content Understanding クライアントをセットアップ
    credential = DefaultAzureCredential()
    client = ContentUnderstandingClient(
        endpoint=endpoint,
        credential=credential,
        api_version=api_version)
    ```

1. ユーザーがファイル番号を入力するか、プログラムを終了するためのコードが用意されています。

1. コメント **ファイルを分析** を見つけて、以下のコードを追加します。

    ```python
    # ファイルを分析
    try:
        poller = client.begin_analyze(
            analyzer_id=analyzer_id,
            inputs=[AnalysisInput(data=file_bytes)],
        )
        result: AnalysisResult = poller.result()
    except AzureError as err:
        print(f"[Azure エラー]: {err.message}")
        sys.exit(1)
    except Exception as ex:
        print(f"[予期しないエラー]: {ex}")
        sys.exit(1)

    for field in result.contents[0].fields:
        if field == "Description":
            print(f"{field}:\n{result.contents[0].fields[field].value_string}\n")
        elif field == "Tags":
            print(f"{field}:")
            for tag in result.contents[0].fields[field].value_array:
                print("  -", tag.value_string)
    ```

1. ファイルを保存します（**Ctrl+S**）。

### アプリのテスト

1. ターミナル ペインで、次のコマンドを使用して Azure にサインインします。

    ```
    az login
    ```

1. メッセージに従って Azure にサインインします。

1. サインインしたら、次のコマンドを入力してアプリケーションを実行します。

    ```
    python analyze-image.py
    ```

1. プロンプトが表示されたら、次の画像のいずれかに対応する番号を入力します。

    |![キリン。](../../Labfiles/03-content-understanding-image/Python/images/image1.jpg) | ![ゾウ。](../../Labfiles/03-content-understanding-image/Python/images/image2.jpg) | ![ライオン。](../../Labfiles/03-content-understanding-image/Python/images/image3.jpg)
    |--|--|--|
    | 1 | 2 | 3 |

1. 出力を確認します。選択した画像の説明と、適切なタグのコレクションが含まれているはずです。

1. 終わったら、1、2、3 以外の値を入力して終了します。

## クリーンアップ

この演習で作成した **ストレージ アカウント、アナライザー、Foundry プロジェクトは、まだ削除しないでください。** リソースの削除は、[演習 06](06-knowledge-mining.md) の「クリーンアップ」で、1〜4 日目の分をまとめて行います。
