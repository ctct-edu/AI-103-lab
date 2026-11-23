---
lab:
    title: 'エージェントでの Azure Speech の使用'
    description: 'Foundry Tools の Azure Speech MCP サーバーを使用して、エージェントに音声機能を追加する。'
    level: 300
    duration: 40
    islab: true
    status: 'released'
---

# エージェントでの Azure Speech の使用

**Foundry Tools の Azure Speech** は MCP サーバーを提供しており、これを使用すると、エージェントから音声認識と音声合成の機能を呼び出せるようになります。

この演習では、Foundry Tools の Azure Speech MCP サーバーを構成し、エージェントに接続します。

この演習の所要時間は約 **40** 分です。

> **注意**: この演習で使用する一部のテクノロジーはプレビュー中または開発中のため、予期しない動作、警告、またはエラーが発生する場合があります。

## 前提条件

この演習を開始する前に、以下を準備してください。

- 1 日目の演習 01 の完了（1 日目で作成した Foundry プロジェクトを共用します）
- [演習 02](02-language-agent.md) の完了（エージェントの作成とツール接続の流れを理解していること）
- Foundry Agent Service の MCP ツールを使用できること（Enterprise ティア。詳細は [Foundry Agent Service の MCP ツール](https://learn.microsoft.com/azure/foundry/agents/how-to/tools/azure-ai-speech#prerequisites) を参照）
- Visual Studio Code、Python 3.13 以降、Azure CLI（演習環境にはインストール済みです）

> **注意**: **1 日目の演習 01** で作成した **East US 2** のプロジェクトを使用します。Azure Speech の MCP ツールは、[サポートされているリージョン](https://learn.microsoft.com/azure/ai-services/speech-service/regions?tabs=mcp) のうち **West US 3** 以外のリージョンで使用してください。

## Azure ストレージ アカウントの準備

Azure Speech MCP サーバーは、生成された音声ファイルを保存するために Azure ストレージ アカウントを使用します。

この研修では、**2 日目の演習 03 で作成したストレージ アカウント `ai103stgXXYYYYMMDD`**（XX は自分の番号、YYYYMMDD は 2 日目の日付）を再利用し、新しいコンテナー **files** を追加します。新しいストレージ アカウントを作成する必要はありません。

> **注意**: このストレージ アカウントは、4 日目の演習 03・04 でも使用します。**4 日目の演習 06 の最終クリーンアップまで削除しないでください。**

1. [Azure ポータル](https://portal.azure.com)（`https://portal.azure.com`）を開き、Azure の資格情報でサインインします。

1. リソース グループ **AI103StudentXX** で、ストレージ アカウント **ai103stgXXYYYYMMDD** を開きます。

    > **注意**: 2 日目の演習 03 でストレージ アカウントを作成していない場合だけ、次の設定で新しい **Azure ストレージ アカウント** リソースを作成し、作成後にそのリソースに移動します。
    - **サブスクリプション**: *自分のサブスクリプション*
    - **リソース グループ**: 各自に割り当てられた既存のリソース グループ（**AI103StudentXX**）を選択します。新しいリソース グループは作成しません。
    > - **ストレージ アカウント名**: `ai103stgXXYYYYMMDD`（小文字と数字のみ。使用済みの場合は末尾に数字を付けます）
    > - **リージョン**: Foundry プロジェクトと同じ **East US 2**
    > - **主要サービス**: Azure Blob Storage または Azure Data Lake Storage Gen2
    > - **パフォーマンス**: Standard
    > - **冗長性**: ローカル冗長ストレージ (LRS)

1. ストレージ アカウントの左側のナビゲーション ペインで、**[データ ストレージ]** を展開し、**[コンテナー]** を選択します。

1. **[コンテナーの追加]** を選択し、**[新しいコンテナー]** ペインの **[名前]** に `files` と入力して **[作成]** を選択します。ここに、エージェントが生成した音声ファイルが保存されます。

    > **注意**: 一覧には、2 日目の演習 03 の `contosoproducts` など、ほかの演習で作成したコンテナーも表示されます。それらは変更しません。

    ![ストレージ アカウントの [コンテナー] ページのスクリーンショット。赤枠は左側の [コンテナー]、[コンテナーの追加]、[作成] ボタン、青枠は [名前] の入力欄。](../Media/d3e05-01-storage-add-files-container.png)

1. **files** コンテナーのコンテキスト メニュー（**...**）で **[SAS の生成]**（Generate SAS）を選択します。

    ![コンテナーの一覧のスクリーンショット。赤枠は files コンテナーの [...] と [SAS の生成]。](../Media/d3e05-02-files-generate-sas-menu.png)

1. 次の内容で SAS トークンを作成します。
    - **署名方法**: アカウント キー
    - **署名キー**: キー 1
    - **保存されているアクセス ポリシー**: なし
    - **アクセス許可**:
        - 読み取り (Read)
        - 追加 (Add)
        - 作成 (Create)
        - 書き込み (Write)
        - リスト (List)
    - **開始日時と有効期限**:
        - **開始**: 現在の日時
        - **有効期限**: 明日の午後 11:59
    - **使用できる IP アドレス**: 空白のまま
    - **許可されるプロトコル**: HTTPS のみ

    ![[SAS の生成] ペインのスクリーンショット。赤枠は [署名方法]、[署名キー]、[アクセス許可] の 5 項目。](../Media/d3e05-03-sas-permissions.png)

1. **[SAS トークンおよび URL を生成]** を選択します。

    ![[SAS の生成] ペインの下部のスクリーンショット。青枠は [有効期限]、赤枠は [HTTPS のみ] と [SAS トークンおよび URL を生成] ボタン。](../Media/d3e05-04-sas-expiry-protocol.png)

    > **重要**: 生成された SAS トークンと SAS URL をコピーして、いったんテキスト ファイルに保存しておいてください。あとの手順で必要になります。SAS URL はアクセス権を含む秘密情報です。**Labfiles フォルダー内のファイルや `.env` には貼り付けず**、他の人と共有しないでください。

## Foundry プロジェクトの確認

1. Web ブラウザーで [Microsoft Foundry ポータル](https://ai.azure.com)（`https://ai.azure.com`）を開き、1 日目の演習 01 で作成したプロジェクト（例: **AI103-Lab01-YYYYMMDD-XX**）を開きます。

1. プロジェクトのホーム ページで、API キー、プロジェクト エンドポイント、OpenAI エンドポイントが表示されていることを確認します。

    > **ヒント**: プロジェクト キーをクリップボードにコピーしておいてください。あとの手順で必要になります。**Foundry リソース名** も控えておいてください。

    > **Foundry リソース名の確認方法**: **[プロジェクト エンドポイント]** は `https://<Foundry リソース名>.services.ai.azure.com/api/projects/<プロジェクト名>` の形式です。ホスト名の先頭部分が **Foundry リソース名**、`/projects/` の後ろが **プロジェクト名** です。リソース名とプロジェクト名は別の名前なので、混同しないでください。リソース名はプロジェクト名から推測できないため、必ずエンドポイントに表示された名前を、そのまま使用してください。
    >
    > 例: `https://ai103-lab01-20261119-01-resource.services.ai.azure.com/api/projects/AI103-Lab01-20261119-01` の場合、Foundry リソース名は `ai103-lab01-20261119-01-resource`、プロジェクト名は `AI103-Lab01-20261119-01` です。

## エージェントの作成

1. プロジェクトのホーム ページの **[エージェントの構築]** で **[エージェントの作成]**（Create agent）を選択します（または、左側のナビゲーション ペインで **[エージェント]**（Agents）を選択します）。**[エージェントの作成]** ダイアログで、**[エージェント名]** に `speech-agent` と入力し、**[対話モデル]** は既定の **[テキスト]** のままにして、**[作成]** を選択します（画面は [演習 02](02-language-agent.md) と同じです）。

    エージェントの準備ができると、エージェント プレイグラウンドが開きます。

1. エージェント プレイグラウンドの **[モデル]** で、既定の gpt-5 から、1 日目の演習 01 でデプロイした **gpt-5-mini**（TPM 10K）に変更します。

1. エージェントに次の **指示**（Instructions）を設定します。

    ```
    あなたは、Azure AI Speech ツールを使用して音声の文字起こしと音声の生成を行う AI エージェントです。
    ```

1. **[保存]**（Save）ボタンで変更を保存します。

1. **[チャット]**（Chat）ペインに次のプロンプトを入力して、エージェントをテストします。

    ```
    あなたは何を手伝ってくれますか？
    ```

    エージェントが指示に基づいた適切な回答を返すはずです。

## Azure Speech in Foundry Tools の接続の作成

Foundry には Azure Speech in Foundry Tools の MCP サーバーが含まれており、これをプロジェクトに接続してエージェントで使用できます。

1. 左側のナビゲーション ペインで **[ツール]**（Tools）ページを選択します。

1. **[ツール]** タブで **[ツールを接続]** を選択し、**[ツールの選択]** ダイアログの **[カタログ]**（Catalog）タブで `Speech` を検索して **Azure Speech MCP Server** を選択し、**[作成]** を選択します。

    ![[ツールの選択] ダイアログのスクリーンショット。赤枠は [カタログ] タブ、Azure Speech MCP Server、[作成] ボタン、青枠は検索ボックス。](../Media/d3e05-05-tools-catalog-speech-mcp.png)

1. **[Azure Speech MCP Server ツールを接続する]** ダイアログで、次の構成を指定して **[接続]** を選択します。
    - **名前**（Name）: `azure-speech-tool-XX`（XX は自分の番号）
    - **リモート MCP サーバー エンドポイント**（Remote MCP Server endpoint）: `https://{foundry-resource-name}.cognitiveservices.azure.com/speech/mcp?api-version=...`（既定値のまま。次のパラメーターを入力すると、`{foundry-resource-name}` が自動で置き換わります）
    - **パラメーター**（Parameters）: foundry-resource-name: *自分の Foundry リソース名*
    - **認証**（Authentication）: キーベース（固定で表示されます）
    - **Authorization** の **Bearer**: *Foundry プロジェクトの API キー*
    - **X-Blob-Container-Url**: *ストレージ コンテナーの SAS URL*

    ![接続ダイアログのスクリーンショット。青枠は [名前]、パラメーターの値（Foundry リソース名）、Bearer と X-Blob-Container-Url の入力欄、赤枠はエンドポイントと [認証] のキーベース。画面は API キーと SAS URL を入力する前の状態。](../Media/d3e05-06-speech-mcp-connect-form.png)

    > **注意**: 画面のバージョンによっては、API キーの入力欄の名前が **Ocp-Apim-Subscription-Key** と表示される場合があります。どちらの場合も Foundry プロジェクトの API キーを入力します。

    > **注意**: `foundry-resource-name` には、プロジェクト名ではなく **Foundry リソース名**（プロジェクト エンドポイントのホスト名の先頭部分）を入力します。プロジェクト名を入力すると接続に失敗します。エンドポイントのドメインは `cognitiveservices.azure.com` で、プロジェクト エンドポイントの `services.ai.azure.com` とは異なります。`{foundry-resource-name}` の部分だけを自分のリソース名に置き換えてください。
    >
    > 例: Foundry リソース名が `ai103-lab01-20261119-01-resource` の場合、エンドポイントは `https://ai103-lab01-20261119-01-resource.cognitiveservices.azure.com/speech/mcp?api-version=2025-11-15-preview` になります。

    > **注意**: Azure サブスクリプションのポリシーによってキーベースの認証が無効になっている場合は、Entra ID 認証を使用して、エージェントを Azure Speech サービスに接続できます。

1. MCP ツールの接続が作成されるまで待ち、その詳細ページを表示します。

1. Azure Speech in Foundry Tools 接続の詳細ページで **[エージェントで使用する]**（Use in an agent）を選択し、先ほど作成した **speech-agent** エージェントを選択します。

    エージェントがプレイグラウンドで開き、Azure Speech in Foundry Tools ツールが接続された状態になるはずです。

## プレイグラウンドでの Azure Speech ツールのテスト

1. **speech-agent** エージェントのプレイグラウンドで、次のプロンプトを入力します。

    ```
    次の文を音声として生成してください: "吾輩は猫である。名前はまだ無い。"
    ```

1. 承認を求められたら、**[Always approve all Azure Speech MCP Server tools]** を選択して Azure Speech ツールの使用を承認します。

1. 応答を確認します。生成された音声ファイルへのリンクが含まれているはずです。リンクを選択して、合成された音声を聞きます。スピーカーが使えない場合は、リンク先のファイルが生成されていることを確認します。

    **出力例**（モデルの応答は実行のたびに変わります。リンクの SAS トークンは伏せています）:

    ```output
    音声を生成しました。再生・ダウンロードはこちらのURLから可能です（有効期限あり）:

    https://<ストレージ アカウント名>.blob.core.windows.net/files/tts/<日時>_<ID>.mp3?<SAS トークン>

    生成に使用した設定:
    - テキスト: 「吾輩は猫である。名前はまだ無い。」
    - 言語: ja-JP
    - 音声: ja-JP-NanamiNeural
    - 長さ: 約4.4秒
    ```

    > **ヒント**: 日本語の文を渡すと、エージェントは言語（`ja-JP`）と日本語の音声（出力例では `ja-JP-NanamiNeural`）を自動で選びます。

1. 生成された音声を日本語のまま文字起こしします。前の応答に表示されたリンク（SAS トークン付きの URL）を使って、次のプロンプトを入力します。

    ```
    次のファイルを文字起こししてください: <前の応答に表示された音声ファイルのリンク>
    ```

    > **注意**: リンクには有効期限があります。生成したあと、すぐに使用してください。

    **出力例**（モデルの応答は実行のたびに変わります）:

    ```output
    文字起こし結果です（音声長 約4.44秒）:

    我輩は猫である。名前はまだ無い。
    ```

    > **注意**: 文字起こしは、かな・漢字の表記が元の文と異なる場合があります（この例では「吾輩」が「我輩」になっています）。

1. 次に、上流の英語の音声ファイルを文字起こしします。次のプロンプトを入力します。

    ```
    次のファイルを文字起こししてください: https://microsoftlearning.github.io/mslearn-ai-language/Labfiles/05-speech-tool/speech_1.wav
    ```

1. 承認を求められた場合は、**[Always approve all Azure Speech MCP Server tools]** を選択して Azure Speech ツールの使用を承認します。

    > **注意**: ツールの呼び出し中に一時的なエラーが発生した場合は、ページを更新して、同じプロンプトをもう一度試してください。

    > **注意**: Foundry のガードレールによってやり取りがブロックされた、というメッセージが表示されることがあります。これは、`speech_1.wav` の文字起こし内容が Foundry の組み込みコンテンツ安全性チェックによって検出されるために発生します。その場合は、影響を受けない `speech_2.wav` を使用して、プロンプトをやり直してください。

1. 出力を確認します。音声ファイルの文字起こしが表示されるはずです。

    > **ヒント**: この音声ファイルは、`Labfiles/05-azure-speech-mcp` フォルダーにも配置されています（**speech_1.wav**、**speech_2.wav**）。ただし、MCP サーバーが読み取れるのは URL で指定したファイルのため、プロンプトには上の URL を指定します。

## クライアント アプリケーションの作成

### スターター コードを開く

1. Visual Studio Code を開きます。

1. **[ファイル] > [フォルダーを開く]** を選択し、配置済みの `Labfiles/05-azure-speech-mcp` フォルダーを開きます。

1. エクスプローラー ペインで **Python/speech-client** フォルダーを展開します。アプリケーション ファイルは次のとおりです。
    - **.env**（アプリケーションの構成ファイル）
    - **requirements.txt**（インストールが必要な Python パッケージの依存関係）
    - **speech-client.py**（アプリケーションのコード ファイル）

### アプリケーションの構成

1. **speech-client** フォルダーを右クリックし、**[統合ターミナルで開く]** を選択します。ターミナルが **speech-client** フォルダーで開いていることを確認します。

1. ターミナルで次のコマンドを入力して、演習用にあらかじめ構築済みの仮想環境 (`labenv`) を有効化します。

    ```
    .\labenv\Scripts\Activate.ps1
    ```

    > **注意**: 必要な Python パッケージ (Foundry SDK、Azure Identity など) は `labenv` に事前インストール済みです。`pip install` を再実行する必要はありません。

1. **.env** ファイルを開き、`your_project_endpoint` を Foundry プロジェクトの **エンドポイント**（Foundry ポータルのプロジェクト ホーム ページからコピーしたもの）に置き換えます。**AGENT_NAME** がエージェントの名前（**speech-agent**）になっていることを確認します。この名前は大文字と小文字が区別されます。

1. 構成ファイルを保存します（**Ctrl+S**）。

### アプリケーション コードの実装

1. **speech-client.py** ファイルを開き、既存のコードを確認します。エージェントにプロンプトを送信するコードを追加していきます。

1. ファイルの先頭の既存の参照の下にあるコメント **名前空間のインポート** を見つけて、必要な名前空間をインポートする以下のコードを追加します。

    ```python
    # 名前空間のインポート
    from azure.identity import DefaultAzureCredential
    from azure.ai.projects import AIProjectClient
    ```

1. **main** 関数では、構成ファイルからエンドポイントを読み込むコードがすでに用意されています。コメント **プロジェクト クライアントを取得** を見つけて、Foundry プロジェクトのクライアントを作成する以下のコードを追加します。

    ```python
    # プロジェクト クライアントを取得
    project_client = AIProjectClient(
        endpoint=foundry_endpoint,
        credential=DefaultAzureCredential(),
    )
    ```

1. コメント **OpenAI クライアントを取得** を見つけて、エージェントを呼び出すための OpenAI クライアントを取得する以下のコードを追加します。

    ```python
    # OpenAI クライアントを取得
    openai_client = project_client.get_openai_client()
    ```

1. コメント **エージェントを使用して応答を取得** を見つけて、ユーザー プロンプトをエージェントに送信して応答を表示する以下のコードを追加します（`else:` の下に 1 レベル深くインデントしてください）。

    > **ヒント**: `else:` の下にある `pass  # コードを追加したら、この行は削除してかまいません` の行は、`else:` ブロックが空にならないようにするための仮の行です。以下のコードを追加したら、この行は削除してかまいません。

    ```python
    # エージェントを使用して応答を取得
    response = openai_client.responses.create(
        input=[{"role": "user", "content": prompt}],
        extra_body={"agent_reference": {"name": agent_name, "type": "agent_reference"}},
    )

    print(f"{agent_name}: {response.output_text}")
    ```

1. コード ファイルに加えた変更を保存します。

## クライアント アプリケーションのテスト

1. ターミナル ペインで、次のコマンドを使用して Azure にサインインします。

    ```
    az login
    ```

1. メッセージに従って Azure にサインインします。

1. サインインしたら、次のコマンドを入力してアプリケーションを実行します。

    ```
    python speech-client.py
    ```

1. プロンプトが表示されたら、次のプロンプトを入力します。

    ```
    "雨にも負けず、風にも負けず。" を、音声 "ja-JP-KeitaNeural" を使用して音声合成してください。
    ```

1. 応答を確認します。生成された音声ファイルへのクリック可能なリンクが含まれているはずです。

    **出力例**（抜粋。モデルの応答は実行のたびに変わります。リンクの SAS トークンは伏せています）:

    ```output
    speech-agent: 音声を合成しました。以下のリンクからダウンロードして再生できます。
    https://<ストレージ アカウント名>.blob.core.windows.net/files/tts/<日時>_<ID>.mp3?<SAS トークン>
    - 音声: ja-JP-KeitaNeural
    - テキスト: 「雨にも負けず、風にも負けず。」
    - 長さ: 約 3.0 秒
    ```

    指定した音声名（`ja-JP-KeitaNeural`）が反映されていることを確認します。日本語の音声には、`ja-JP-NanamiNeural` などの音声名も指定できます。

1. 生成された音声ファイルを確認したら、そのリンクを使って、次のプロンプトを入力します。

    ```
    次のファイルを文字起こししてください: <前の応答に表示された音声ファイルのリンク>
    ```

    文字起こしの結果が、元の日本語の文と一致していることを確認します。

1. 次に、上流の英語の音声ファイルを文字起こしします。次のプロンプトを入力します。

    ```
    次のファイルを文字起こししてください: https://microsoftlearning.github.io/mslearn-ai-language/Labfiles/05-speech-tool/speech_2.wav
    ```

1. 応答を確認します。

1. プログラムを終了するには、「quit」と入力します（または Enter キーを押すだけでも終了します）。

## クリーンアップ

この演習で作成した **ストレージ アカウント、エージェント、Foundry プロジェクトは、まだ削除しないでください。** ストレージ アカウントを含むすべてのリソースの削除は、**4 日目の演習 06「ナレッジ マイニング ソリューションの作成」の「クリーンアップ」**で、1〜4 日目の分をまとめて行います。SAS 付きの URL を保存したテキスト ファイルも、最終クリーンアップのときに削除してください。
