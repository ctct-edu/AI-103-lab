---
lab:
    title: 'テキストの分析'
    description: 'Foundry Tools の Azure Language を使用してテキストを分析する。'
    level: 300
    duration: 40
    islab: true
    status: 'released'
---

# テキストの分析

**Foundry Tools の Azure Language** は、言語の検出、エンティティの認識、PII の編集など、テキストの分析をサポートします。

たとえば、旅行代理店が自社 Web サイトに投稿されたホテルのレビューを処理するとします。Azure Language を使用すると、各レビューが何語で書かれているかを判定し、レビューに登場する場所・ランドマーク・人物などの名前付きエンティティを特定し、Web サイトに公開する前に個人を特定できる情報 (PII) を編集できます。この演習では、Azure Language の Python SDK を使用して、簡単なホテル レビュー分析アプリケーションを実装します。

この演習の所要時間は約 **40** 分です。

> **注意**: この演習で使用する一部のテクノロジーはプレビュー中または開発中のため、予期しない動作、警告、またはエラーが発生する場合があります。

## 前提条件

この演習を開始する前に、以下を準備してください。

- アクティブな [Azure サブスクリプション](https://azure.microsoft.com/free/)
- Visual Studio Code、Python 3.13 以降、Azure CLI（演習環境にはインストール済みです。詳細は [演習環境 構築ガイド（共通）](00-environment-setup.md) を参照してください）

## 共用の Foundry プロジェクトを開く

Microsoft Foundry では、プロジェクトを使用して、AI ソリューションの開発に使用するモデル、リソース、データ、その他の資産を整理します。

> **重要**: この演習では、新しいプロジェクトは作成しません。**1 日目の演習 01** で作成した Foundry プロジェクト（**East US 2**）を、1〜4 日目のすべての演習で共用します。**4 日目の演習 06 の「クリーンアップ」まで削除しないでください。**

1. Web ブラウザーで [Microsoft Foundry ポータル](https://ai.azure.com)（`https://ai.azure.com`）を開き、Azure の資格情報でサインインします。初回サインイン時に表示されるヒントやクイック スタートのペインは閉じ、必要に応じて左上の Foundry ロゴを選択してホーム ページに移動します。

    > **注意**: 初回サインイン時に、既定の名前（`{アカウント名}-XXXX`）のプロジェクトとエージェント **my-first-agent** が自動作成されることがあります。このプロジェクトは **East US 2 以外**（West US 3 など）に作成される場合があるため、使用しません。

1. ページ上部のツール バーで **[新しい Foundry]**（New Foundry）トグルがオフの場合は、オンにします。ページ左上のプロジェクト名の横にある **⌄** を選択し、1 日目の演習 01 で作成したプロジェクト（例: **AI103-Lab01-YYYYMMDD-XX**）を選択します。

    > **注意**: このプロジェクトのリージョンは、この演習で使用する [Azure Language がサポートするリージョン](https://learn.microsoft.com/azure/ai-services/language-service/concepts/regional-support) に含まれている必要があります。また、3 日目以降の演習は **East US 2** が前提です。プロジェクトが **East US 2** にない場合や、1 日目のプロジェクトが見つからない場合は、講師に確認してください。

1. プロジェクトのホーム ページに、**[API キー]**、**[プロジェクト エンドポイント]**、**[Azure OpenAI エンドポイント]** が表示されていることを確認します。

    > **ヒント**: このあとの手順でプロジェクト エンドポイントが必要になります。**Foundry リソース名** も控えておいてください。Foundry リソース名は、**[プロジェクト エンドポイント]**（`https://<Foundry リソース名>.services.ai.azure.com/api/projects/<プロジェクト名>`）のホスト名の先頭部分です。リソース名はプロジェクト名から推測できないため、必ずエンドポイントに表示された名前を、そのまま使用してください。

## スターター コードを開く

アプリケーションの初期ファイルは、演習環境に配置済みです。

1. Visual Studio Code を開きます。

1. **[ファイル] > [フォルダーを開く]** を選択し、配置済みの `Labfiles/01-analyze-text` フォルダーを開きます。

1. エクスプローラー ペインで **Python/text-analysis** フォルダーを展開します。アプリケーション ファイルは次のとおりです。
    - **reviews**（レビュー文書を含むサブフォルダー。英語、フランス語、日本語など複数の言語で書かれています。`review6.txt` は日本語のレビューです）
    - **.env**（アプリケーションの構成ファイル）
    - **requirements.txt**（インストールが必要な Python パッケージの依存関係）
    - **text-analysis.py**（アプリケーションのコード ファイル）

## アプリケーションの構成

1. **text-analysis** フォルダーを右クリックし、**[統合ターミナルで開く]** を選択します。ターミナルが **text-analysis** フォルダーで開いていることを確認します。

1. ターミナルで次のコマンドを入力して、仮想環境を作成し、必要な Python パッケージをインストールします。

    ```
    python -m venv labenv
    .\labenv\Scripts\Activate.ps1
    pip install -r requirements.txt
    ```

    > **注意**: スクリプトの実行がブロックされて `Activate.ps1` が実行できない場合は、`Set-ExecutionPolicy -Scope Process Bypass` を実行してから、もう一度有効化してください。プロンプトの先頭に **(labenv)** と表示されれば、仮想環境が有効です。

1. **.env** ファイルを開き、`your_foundry_endpoint` を Foundry リソースのエンドポイントに置き換えます。Foundry ポータルのプロジェクト ホーム ページからコピーしたプロジェクト エンドポイントを貼り付け、**末尾の「/api/projects/{プロジェクト名}」を削除**してください。

    > **重要**: エンドポイントは `https://{Foundry リソース名}.services.ai.azure.com` の形式（`.com` ドメインまで）にします。

    変更後、**Ctrl+S** キーを押して構成ファイルを保存します。

## Azure Language に接続するコードの追加

1. **text-analysis.py** ファイルを開き、既存のコードを確認します。Azure Language の Text Analytics SDK を使用するコードを追加していきます。

    > **ヒント**: コードを追加するときは、正しいインデントを維持してください。コメントのインデント レベルを参考にしてください。

1. ファイルの先頭の既存の参照の下にあるコメント **名前空間のインポート** を見つけて、Text Analytics SDK を使用するために必要な名前空間をインポートする以下のコードを追加します。

    ```python
    # 名前空間のインポート
    from azure.identity import DefaultAzureCredential
    from azure.ai.textanalytics import TextAnalyticsClient
    ```

1. **main** 関数では、構成ファイルからエンドポイントを読み込むコードがすでに用意されています。コメント **エンドポイントを使用してクライアントを作成** を見つけて、Text Analytics API のクライアントを作成する以下のコードを追加します。

    ```python
    # エンドポイントを使用してクライアントを作成
    credential = DefaultAzureCredential()
    ai_client = TextAnalyticsClient(endpoint=foundry_endpoint, credential=credential)
    ```

1. コード ファイルを保存します（**Ctrl+S**）。次に、ターミナルで次のコマンドを使用して Azure にサインインします。

    ```
    az login
    ```

    > **注意**: ほとんどの場合は `az login` だけで十分です。複数のテナントにサブスクリプションがある場合は、`--tenant` パラメーターでテナントを指定する必要があります。詳細については、[Azure CLI を使用して対話形式で Azure にサインインする](https://learn.microsoft.com/cli/azure/authenticate-azure-cli-interactively) を参照してください。

1. メッセージに従って Azure にサインインします。サインインのウィンドウは Visual Studio Code ウィンドウの裏側に表示されることがあるので注意してください。コンソールに「Select a subscription and tenant (Type a number or Enter for no changes):」のようなメッセージが表示された場合は、Foundry リソースを含むサブスクリプションの番号を入力します。

1. サインインしたら、次のコマンドを入力してアプリケーションを実行します。

    ```
    python text-analysis.py
    ```

    > **ヒント**: 権限エラー（403 など）が表示された場合は、Foundry リソースに対するロールの割り当てを確認してください。

1. 出力を確認します。コードはエラーなく実行され、**reviews** フォルダー内の各レビュー テキスト ファイルの内容が表示されるはずです。

## 言語を検出するコードの追加

1. コード エディターで、コメント **言語を取得** を見つけます。次に、各レビュー文書の言語を検出するために必要なコードを追加します。

    ```python
    # 言語を取得
    detectedLanguage = ai_client.detect_language(documents=[text])[0]
    print('\n言語: {}'.format(detectedLanguage.primary_language.name))
    ```

    > **注意**: この例では、各レビューを個別に分析するため、ファイルごとにサービスへの呼び出しが発生します。別の方法として、ドキュメントのコレクションを作成し、1 回の呼び出しでサービスに渡すこともできます。どちらの方法でも、サービスからの応答はドキュメントのコレクションになります。上の Python コードで、応答の最初（かつ唯一）のドキュメントを示すインデックス ([0]) を指定しているのはそのためです。

1. 変更を保存して、プログラムを再実行します。

1. 出力を確認します。今回は、各レビューの言語が識別されていることに注目してください。

    **出力例**:

    ```output
    -------------
    review1.txt
    ...
    言語: English
    ```

    `review5.txt` のようにフランス語で書かれたレビューは `言語: French` のように、日本語で書かれた `review6.txt`（架空のホテルのレビュー）は `言語: Japanese` のように識別されます。

## エンティティを抽出するコードの追加

ドキュメントやその他のテキストには、人物、場所、期間、その他のエンティティが記載されていることがよくあります。Text Analytics API は、テキスト内の複数のカテゴリ（およびサブカテゴリ）のエンティティを検出できます。

1. コード エディターで、コメント **エンティティを取得** を見つけます。次に、各レビューに記載されているエンティティを特定するために必要なコードを追加します。

    ```python
    # エンティティを取得
    entities = ai_client.recognize_entities(documents=[text])[0].entities
    if len(entities) > 0:
        print("\nエンティティ")
        for entity in entities:
            print('\t{} ({})'.format(entity.text, entity.category))
    ```

1. 変更を保存して、プログラムを再実行します。

1. 出力を確認します。テキストから検出されたエンティティ（ホテル名や都市名など）とそのカテゴリが表示されます。

    **出力例**（日本語の `review6.txt` の抜粋。検出されるエンティティは実行時期により変わる場合があります）:

    ```output
    エンティティ
        ホテル (Location)
        スタッフ (PersonType)
        くら橋 (Location)
        東京都港区青葉町1-2-3 (Address)
        2026年3月15日 (DateTime)
        客室 (Location)
        駅から (Location)
        受付担当 (PersonType)
        山田花子 (Person)
        野菜 (Product)
        hanako.yamada@example.com (Email)
        翌日 (DateTime)
        090-0000-0000 (PhoneNumber)
    ```

    > **ヒント**: 日本語のレビューでも、人名・住所・日付・メール アドレス・電話番号が認識されます。ただし、「ホテル さくら橋」が `くら橋` と切り出されるなど、エンティティの区切りが不正確になる場合があります。`recognize_entities` と `recognize_pii_entities` は、`language` 引数を指定しないと英語（`en`）として処理されます。区切りを改善したい場合は、`language="ja"` のように言語を指定します。

## PII を編集するコードの追加

プライバシー ポリシーや法令によって、名前、住所、電話番号などの個人情報 (PII) をドキュメントから編集（マスク）することが求められる場合があります。

1. コード エディターで、コメント **PII を取得** を見つけます。次に、各レビューに記載されている PII エンティティを特定するために必要なコードを追加します。

    ```python
    # PII を取得
    pii_result = ai_client.recognize_pii_entities(documents=[text])[0]
    pii_entities = pii_result.entities
    if len(pii_entities) > 0:
        print("\nPII エンティティ")
        for pii_entity in pii_entities:
            print('\t{} ({})'.format(pii_entity.text, pii_entity.category))
        print("編集済みテキスト:\n {}".format(pii_result.redacted_text))
    ```

1. 変更を保存して、プログラムを再実行します。

1. 出力を確認します。識別された PII エンティティと、各ドキュメントの編集済みバージョンが表示されることに注目してください。たとえば `review1.txt` には連絡先のメール アドレスが含まれているため、PII として検出されることを確認します。

    **出力例**（`review1.txt` の抜粋。検出される PII は実行時期により変わる場合があります）:

    ```output
    PII エンティティ
        staff (PersonType)
        Royal Hotel, London, UK (Address)
        3/2/2018 (DateTime)
        Indian (PersonType)
        alex@contoso.com (Email)
    編集済みテキスト:
     ... Contact me at **************** for more details.
    ```

    > **注意**: メール アドレスのほかに、人物の種類（PersonType）や日付（DateTime）、住所（Address）なども PII として検出され、編集されます。

    **出力例**（`review6.txt` の抜粋。検出される PII は実行時期により変わる場合があります）:

    ```output
    PII エンティティ
        スタッフ (PersonType)
        東京都港区青葉町1-2-3 (Address)
        2026年3月15日 (DateTime)
        受付担当 (PersonType)
        山田花子 (Person)
        hanako.yamada@example.com (Email)
        翌日 (DateTime)
        090-0000-0000 (PhoneNumber)
    編集済みテキスト:
     素晴らしいホテルと****
    ホテル さくら橋、*************
    **********
    清潔な客室と丁寧な接客、そして駅から歩いてすぐの便利な立地でした。****の****さんがとても親切で、家族みんなで快適に過ごせました。
    朝食の和食は、地元の野菜がたくさん使われていて、本当においしかったです。
    チェックアウトのときに忘れ物をしたので、************************* にメールを送ったところ、**に連絡をいただけました。詳しいお問い合わせは ************* までお願いします。
    ```

1. 作業が終わったら、`deactivate` を入力して仮想環境を終了できます（次の演習でも同じフォルダー構成の仮想環境を新しく作成します）。

## クリーンアップ

この演習で使用した **Foundry プロジェクトとリソースは、後続の演習（02〜07）でも使用します。まだ削除しないでください。** リソースの削除は、**4 日目の演習 06「ナレッジ マイニング ソリューションの作成」の「クリーンアップ」**で、1〜4 日目の分をまとめて行います。
