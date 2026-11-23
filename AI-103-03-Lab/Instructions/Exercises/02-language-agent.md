---
lab:
    title: 'テキスト分析エージェントの開発'
    description: 'Foundry Tools の Azure Language を使用して、AI エージェントにテキスト分析機能を追加する。'
    level: 300
    duration: 30
    islab: true
    status: 'released'
---

# テキスト分析エージェントの開発

**Foundry Tools の Azure Language** は、言語の検出、エンティティの認識、PII の編集など、テキストの分析をサポートします。

このサービスは、REST API や各種言語向けの SDK を通じてアプリケーションから直接利用できます。また、**Foundry Tools の Azure Language MCP サーバー** を使用して、その機能を AI エージェントに統合することもできます。この演習では、後者を実際に行います。

この演習の所要時間は約 **30** 分です。

> **注意**: この演習で使用する一部のテクノロジーはプレビュー中または開発中のため、予期しない動作、警告、またはエラーが発生する場合があります。

## 前提条件

この演習を開始する前に、以下を準備してください。

- 1 日目の演習 01 の完了（1 日目で作成した Foundry プロジェクトを共用します）
- Foundry Agent Service の MCP ツールを使用できること（Enterprise ティア。詳細は [Foundry Agent Service の MCP ツール](https://learn.microsoft.com/azure/foundry/agents/how-to/tools/azure-ai-speech#prerequisites) を参照）
- Visual Studio Code、Python 3.13 以降、Azure CLI（演習環境にはインストール済みです）

> **注意**: **1 日目の演習 01** で作成した **East US 2** のプロジェクトをそのまま使用します。Agent Service の MCP ツールは **West US 3** 以外のリージョンで使用してください。

## 共用の Foundry プロジェクトを開く

1. Web ブラウザーで [Microsoft Foundry ポータル](https://ai.azure.com)（`https://ai.azure.com`）を開き、1 日目の演習 01 で作成したプロジェクト（例: **AI103-Lab01-YYYYMMDD-XX**）を開きます。ページ上部の **[新しい Foundry]**（New Foundry）トグルがオンになっていることを確認します。

1. プロジェクトのホーム ページで、**[API キー]**、**[プロジェクト エンドポイント]**、**[Azure OpenAI エンドポイント]** が表示されていることを確認します。

    > **ヒント**: プロジェクト キーをクリップボードにコピーしておいてください。あとの手順で必要になります。**Foundry リソース名** も控えておいてください。

    > **Foundry リソース名の確認方法**: **[プロジェクト エンドポイント]** は `https://<Foundry リソース名>.services.ai.azure.com/api/projects/<プロジェクト名>` の形式です。ホスト名の先頭部分が **Foundry リソース名**、`/projects/` の後ろが **プロジェクト名** です。リソース名とプロジェクト名は別の名前なので、混同しないでください。リソース名はプロジェクト名から推測できないため、必ずエンドポイントに表示された名前を、そのまま使用してください。
    >
    > 例: `https://ai103-lab01-20261119-01-resource.services.ai.azure.com/api/projects/AI103-Lab01-20261119-01` の場合、Foundry リソース名は `ai103-lab01-20261119-01-resource`、プロジェクト名は `AI103-Lab01-20261119-01` です。

## エージェントの作成

1. プロジェクトのホーム ページの **[エージェントの構築]** で **[エージェントの作成]**（Create agent）を選択します（または、左側のナビゲーション ペインで **[エージェント]**（Agents）を選択します）。**[エージェントの作成]** ダイアログで、**[エージェント名]** に `Text-Analysis-Agent` と入力し、**[対話モデル]** は既定の **[テキスト]** のままにして、**[作成]**（Create）を選択します。

    エージェントの準備ができると、エージェント プレイグラウンドが開きます。

    ![[エージェントの作成] ダイアログのスクリーンショット。青枠は [エージェント名]、赤枠は [対話モデル] の [テキスト] と作成ボタン。](../Media/d3e02-01-create-text-analysis-agent.png)

    > **注意**: エージェントの作成時に、モデルの選択は求められません。エージェントには既定で **gpt-5** が選ばれます。[対話モデル] は作成後に変更できません。

1. エージェント プレイグラウンドの **[モデル]** で、1 日目の演習 01 でデプロイした **gpt-5-mini**（TPM 10K）を選択します。

1. エージェントの **[手順]**（Instructions）欄に、次の指示を設定します。

    ```
    あなたは、ユーザーがテキストを分析するのを支援する AI エージェントです。
    ```

1. **[保存]**（Save）ボタンで変更を保存します。

    ![エージェント プレイグラウンドのスクリーンショット。赤枠は [モデル] の gpt-5-mini と [保存] ボタン、青枠は [手順] の入力欄。](../Media/d3e02-02-agent-model-instructions.png)

1. **[チャット]**（Chat）ペインに次のプロンプトを入力して、エージェントをテストします。

    ```
    あなたは何を手伝ってくれますか？
    ```

    エージェントが指示に基づいた適切な回答を返すはずです。

## Azure Language in Foundry Tools の接続の作成

Foundry には Azure Language in Foundry Tools の MCP サーバーが含まれており、これをプロジェクトに接続してエージェントで使用できます。

1. 左側のナビゲーション ペインで **[ツール]**（Tools）ページを選択します。

1. [ツール] ページ内の **[ツール]**（Tools）タブを選択します。

1. **[ツールを接続]** を選択し、**[ツールの選択]** ダイアログの **[カタログ]**（Catalog）タブで `Language` を検索して **Azure Language in Foundry Tools** を選択し、**[作成]** を選択します。

    ![[ツールの選択] ダイアログのスクリーンショット。赤枠は [カタログ] タブ、Azure Language in Foundry Tools、[作成] ボタン、青枠は検索ボックス。](../Media/d3e02-03-tool-catalog-azure-language.png)

1. **[Azure Language in Foundry Tools ツールを接続する]** ダイアログで、次の構成を指定して **[接続]** を選択します。
    - **名前**（Name）: `azure-language-tool-XX`（XX は自分の番号）
    - **リモート MCP サーバー エンドポイント**（Remote MCP Server endpoint）: `https://{foundry-resource-name}.cognitiveservices.azure.com/language/mcp?api-version=2025-11-15-preview`（次のパラメーターを入力すると、`{foundry-resource-name}` が自動で置き換わります）
    - **パラメーター**（Parameters）: foundry-resource-name: *自分の Foundry リソース名*
    - **認証**（Authentication）: キーベース（Key-based）
    - **Ocp-Apim-Subscription-Key**: *Foundry プロジェクトの API キー*

    ![接続ダイアログのスクリーンショット。青枠は [名前] とパラメーターの値（Foundry リソース名）、赤枠はエンドポイント、[認証]、[種類]、[接続] ボタン。画面は [認証] に Microsoft Entra を選んだ例。](../Media/d3e02-04-connect-language-tool.png)

    > **注意**: `foundry-resource-name` には、プロジェクト名ではなく **Foundry リソース名**（プロジェクト エンドポイントのホスト名の先頭部分）を入力します。プロジェクト名を入力すると接続に失敗します。エンドポイントのドメインは `cognitiveservices.azure.com` で、プロジェクト エンドポイントの `services.ai.azure.com` とは異なります。`{foundry-resource-name}` の部分だけを自分のリソース名に置き換えてください。
    >
    > 例: Foundry リソース名が `ai103-lab01-20261119-01-resource` の場合、エンドポイントは `https://ai103-lab01-20261119-01-resource.cognitiveservices.azure.com/language/mcp?api-version=2025-11-15-preview` になります。

    > **注意**: Azure サブスクリプションのポリシーによってキーベースの認証が無効になっている場合は、Entra ID 認証を使用して、エージェントを Azure Language サービスに接続できます。[認証] で **Microsoft Entra** を選ぶと、**[種類]**（既定: **プロジェクト マネージド ID**）と **[対象ユーザー]**（`https://cognitiveservices.azure.com/`）が表示されます。Microsoft Entra で接続した場合、プロジェクトのマネージド ID に Foundry リソースを使用する権限がないと、テストで「A user error occurred while executing a tool call.」と表示されることがあります。その場合は講師に確認してください。

1. MCP ツールの接続が作成されるまで待ち、その詳細ページを表示します。

1. Azure Language in Foundry Tools 接続の詳細ページで **[エージェントで使用する]**（Use in an agent）を選択し、先ほど作成した **Text-Analysis-Agent** エージェントを選択します。

    ![接続の詳細ページのスクリーンショット。赤枠は [認証]、[エージェントで使用する]、Text-Analysis-Agent。](../Media/d3e02-05-use-tool-in-agent.png)

    エージェントがプレイグラウンドで開き、Azure Language in Foundry Tools ツールが接続された状態になるはずです。

    ![エージェント プレイグラウンドのスクリーンショット。赤枠は [ツール] に追加された azure-language-tool-XX と、保存後のバージョン。](../Media/d3e02-06-agent-language-tool-added.png)

    > **注意**: MCP ツールがエージェントに自動的に追加されない場合があります。エージェントのツール一覧に **Azure Language in Foundry Tools** が表示されていることを確認してください。表示されていない場合は、エージェントで使用可能なツールから手動で追加します。

## プレイグラウンドでの Azure Language ツールのテスト

1. **Text-Analysis-Agent** エージェントのプレイグラウンドで、指示を次のように変更します。

    ```
    あなたは、ユーザーがテキストを分析するのを支援する AI エージェントです。テキスト分析のタスクを実行するには、Azure Language ツールを使用してください。
    ```

1. **[保存]** ボタンで変更を保存します。

1. **[チャット]** ペインに次のプロンプトを入力して、エージェントをテストします。

    ```
    この記事に含まれる PII エンティティを特定し、編集済みのバージョンを生成してください:

    株式会社みらいテックは、2015年4月1日に、大学時代の友人である佐藤健一（当時28歳）と鈴木美咲（当時27歳）によって、北海道札幌市で創業されました。2人は、農家向けに天候データを分析するソフトウェアを作りたいという思いから、札幌市中央区の小さなオフィスで最初の製品を開発し、地元の農業協同組合に導入してもらうことに成功しました。

    2018年には本社を福岡市に移転し、九州各地の企業にクラウド サービスを提供して事業を拡大しました。2022年には大阪市の企業と業務提携を結び、全国に営業拠点を開設しました。佐藤は最高経営責任者（CEO）として会社の長期的な戦略を導き、鈴木は最高技術責任者（CTO）として製品開発を率い、同社が国内のソフトウェア業界で存在感を高める原動力となりました。
    ```

1. 承認を求められたら、**[Always approve all Azure Language in Foundry Tools tools]** を選択して Azure Language ツールの使用を承認します（承認を 2 回求められる場合があります）。

    > **注意**: 環境によっては、ツールの承認後に 403、502、その他の一時的なエラーが発生することがあります。これらのエラーは通常、処理を妨げるものではありません。ページを更新して、同じプロンプトをもう一度試してください。

1. 応答を確認します。記事の中の個人を特定できる情報が識別され、その情報を編集した記事のバージョンが作成されるはずです。

    > **注意**: 記事に登場する会社名と人物は架空です。

    **出力例**（抜粋。モデルの応答は実行のたびに変わります）:

    ```output
    以下を検出しました（PII＝個人を特定しうる情報）:
    - 人名: 佐藤健一, 鈴木美咲
    - 年齢: 28歳, 27歳

    編集済み本文:
    株式会社みらいテックは、2015年4月1日に、大学時代の友人である[氏名A]（当時[年齢A]）と[氏名B]（当時[年齢B]）によって、北海道札幌市で創業されました。…
    ```

1. チャットの **[ログ]**（Logs）を確認し、エージェントがプロンプトの処理に Azure Language ツールを使用したことを確認します。

    > **ヒント**: エージェントがツールを使うかどうかは、実行のたびに変わる場合があります。ログにツールの呼び出しが表示されない場合は、プロンプトの先頭に `Azure Language ツールを使用して、` を付けて、もう一度試します。

## ツールの承認の構成

1. プレイグラウンドの **指示** の下にある **ツール**（Tools）の一覧で、追加した Azure Language ツールのメニューから **[構成]**（Configure）を選択します。

1. **[この MCP サーバーのツールに対するこのエージェントの承認設定]**（Approval setting for tools in this MCP server for this agent）が **[すべてのツールを常に自動承認]**（Always auto-approve all tools）になっていることを確認します（なっていない場合は変更して追加します）。

    > **重要**: プレイグラウンドで承認したツールだけが自動承認の対象になる場合があります。クライアント アプリケーションには承認ボタンがないため、ここで **[すべてのツールを常に自動承認]** を選択することをお勧めします。個別のツールだけが自動承認の状態では、承認待ちで処理が止まり、アプリケーションの応答が空になります。

1. エージェントへの変更を保存します。**[保存]** を忘れると、設定がクライアント アプリケーションから使われるエージェントに反映されません。

## クライアント アプリケーションの作成

### スターター コードを開く

1. Visual Studio Code を開きます。

1. **[ファイル] > [フォルダーを開く]** を選択し、配置済みの `Labfiles/02-language-agent` フォルダーを開きます。

1. エクスプローラー ペインで **Python/text-agent** フォルダーを展開します。アプリケーション ファイルは次のとおりです。
    - **.env**（アプリケーションの構成ファイル）
    - **requirements.txt**（インストールが必要な Python パッケージの依存関係）
    - **text-agent.py**（アプリケーションのコード ファイル）

### アプリケーションの構成

1. **text-agent** フォルダーを右クリックし、**[統合ターミナルで開く]** を選択します。ターミナルが **text-agent** フォルダーで開いていることを確認します。

1. ターミナルで次のコマンドを入力して、演習用にあらかじめ構築済みの仮想環境 (`labenv`) を有効化します。

    ```
    .\labenv\Scripts\Activate.ps1
    ```

    > **注意**: 必要な Python パッケージ (Foundry SDK、Azure Identity など) は `labenv` に事前インストール済みです。`pip install` を再実行する必要はありません。

1. **.env** ファイルを開き、`your_project_endpoint` を Foundry プロジェクトの **エンドポイント**（Foundry ポータルのプロジェクト ホーム ページからコピーしたもの）に置き換えます。**AGENT_NAME** がエージェントの名前（**Text-Analysis-Agent**）になっていることを確認します。この名前は大文字と小文字が区別されます。

    > **注意**: この演習の `FOUNDRY_ENDPOINT` には、演習 01 とは異なり、**プロジェクト エンドポイント**（末尾の `/api/projects/{プロジェクト名}` を含む URL）をそのまま設定します。

1. 構成ファイルを保存します（**Ctrl+S**）。

### アプリケーション コードの実装

1. **text-agent.py** ファイルを開き、既存のコードを確認します。エージェントにプロンプトを送信するコードを追加していきます。

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

1. コメント **エージェントを使用して応答を取得** を見つけて、ユーザー プロンプトをエージェントに送信して応答を表示する以下のコードを追加します。

    ```python
    # エージェントを使用して応答を取得
    prompt = input("ユーザー プロンプト: ")
    response = openai_client.responses.create(
        input=[{"role": "user", "content": prompt}],
        extra_body={"agent_reference": {"name": agent_name, "type": "agent_reference"}},
    )

    print(f"{agent_name}: {response.output_text}")
    ```

    エージェントの指示とツールの定義は Foundry 側にあり、コードには含まれていません。

1. ツールの承認が自動になっていない場合、応答は `mcp_approval_request`（ツールの承認待ち）で止まり、`response.output_text` が空になります。*print(f"{agent_name}: {response.output_text}")* 行の **前** に、承認待ちの要求へ承認の応答を返して処理を続ける、以下のコードを追加します。

    ```python
    # ツールの承認待ち (mcp_approval_request) の場合は、承認の応答を返して続行
    for _ in range(5):
        approval_requests = [item for item in response.output if item.type == "mcp_approval_request"]
        if not approval_requests:
            break
        response = openai_client.responses.create(
            previous_response_id=response.id,
            input=[{"type": "mcp_approval_response", "approval_request_id": request.id, "approve": True} for request in approval_requests],
            extra_body={"agent_reference": {"name": agent_name, "type": "agent_reference"}},
        )
    ```

    > **注意**: このコードは、承認待ちのツールの呼び出しを、内容を確認せずにすべて承認します。実際のアプリケーションでは、承認する前に、呼び出されるツールの名前（`request.name`）と引数（`request.arguments`）を確認します。

1. コード ファイルに加えた変更を保存します。

## クライアント アプリケーションのテスト

1. Visual Studio Code のターミナルで、次のコマンドを入力して Azure にサインインします。

    ```
    az login
    ```

1. メッセージに従って Azure にサインインします。

1. サインインしたら、次のコマンドを入力してアプリケーションを実行します。

    ```
    python text-agent.py
    ```

1. プロンプトが表示されたら、次のプロンプトを入力します。

    ```
    次のテキストから名前付きエンティティを抽出してください: "田中さんと私は7月14日に京都へ行きました。"
    ```

1. 応答を確認します。人物、場所、日付が識別されるはずです。

    **出力例**（モデルの応答は実行のたびに変わります）:

    ```output
    Text-Analysis-Agent: 抽出された名前付きエンティティ:
    - 人名: 田中
    - 日付: 7月14日
    - 場所: 京都
    ```

    > **トラブルシューティング**: エージェントの応答が空になる場合は、応答の `output` に `mcp_approval_request` が含まれていないか確認してください。含まれていれば、ツールが承認待ちです。承認の応答を返すコード（`mcp_approval_response`）が追加されていることを確認します。
    >
    > 原因の確認には、次の「ツールの詳細の確認」で追加する `response.model_dump_json(indent=2)` の出力（`output` と `tools`）が役立ちます。

## ツールの詳細の確認

Azure Language in Foundry Tools ツールは幅広い機能を提供しており、エージェントは呼び出す適切な機能を選択する必要があります。エージェントの応答から、そのオプションを確認できます。

1. **text-agent.py** コード ファイルで、先ほど追加した *print(f"{agent_name}: {response.output_text}")* 行の直後（*except Exception as ex:* 行の前）に、次の行を追加します。

    <!-- verify:skip -->
    ```python
    print(f"\n応答の詳細: {response.model_dump_json(indent=2)}")
    ```

1. コード ファイルに加えた変更を保存します。

1. ターミナルで、アプリケーションを実行するコマンド（`python text-agent.py`）をもう一度入力します。

1. プロンプトが表示されたら、次のプロンプトを入力します。

    ```
    このレビューに記載されているエンティティと日付を教えてください。また、肯定的か否定的かも判定してください: "7月に沖縄行きの航空券をさくらトラベルで予約しましたが、最高でした!"
    ```

1. 応答を確認します（かなり上にスクロールする必要がある場合があります）。エンティティと日付が識別され、テキストの感情（センチメント）が判定されるはずです。

    **出力例**（応答の最初の部分。モデルの応答は実行のたびに変わります）:

    ```output
    Text-Analysis-Agent: 抽出結果:
    - エンティティ: 
      - 沖縄（場所）
      - 航空券（製品）
      - さくらトラベル（組織）
    - 日付: 7月（年は特定不可）

    感情分析: 肯定的（スコア約0.98）
    ```

1. JSON の応答の詳細を確認します。エージェントが利用できる各ツールが示されています。この場合、Azure Language in Foundry Tools の **extract_named_entities_from_text** ツールと **detect_sentiment_from_text** ツールが使用されているはずです。

    > **ヒント**: 呼び出されるツールは、プロンプトによって変わる場合があります。

## クリーンアップ

この演習で使用した **Foundry プロジェクトとエージェントは、後続の演習（03〜07）でも使用します。まだ削除しないでください。** リソースの削除は、**4 日目の演習 06「ナレッジ マイニング ソリューションの作成」の「クリーンアップ」**で、1〜4 日目の分をまとめて行います。
