import os
from dotenv import load_dotenv

# 参照の追加
# 参照の追加
import asyncio
from agent_framework import Message
from agent_framework_foundry import FoundryChatClient
from agent_framework.orchestrations import SequentialBuilder
from azure.identity import AzureCliCredential

async def main():
    load_dotenv()
    project_endpoint = os.getenv("PROJECT_ENDPOINT")
    model_deployment = os.getenv("MODEL_DEPLOYMENT_NAME")

    # エージェントの手順
    summarizer_instructions="""
    顧客のフィードバックを 1 文で要約してください。中立的かつ簡潔に保ってください。
    出力例:
    写真のアップロード中にアプリがクラッシュする。
    ユーザーがダーク モード機能を称賛している。
    """

    classifier_instructions="""
    フィードバックを次のいずれかに分類してください: Positive（肯定的）、Negative（否定的）、または Feature request（機能リクエスト）。
    """

    action_instructions="""
    要約と分類に基づいて、次のアクションを 1 文で提案してください。
    出力例:
    モバイル チームの高優先度バグとしてエスカレーション。
    デザインおよびマーケティング チームと共有するためのポジティブ フィードバックとして記録。
    製品バックログの機能拡張リクエストとして記録。
    """

    # チャット クライアントを作成
    # チャット クライアントを作成
    credential = AzureCliCredential()
    chat_client = FoundryChatClient(
        credential=credential,
        project_endpoint=project_endpoint,
        model=model_deployment,
    )

    # エージェントを作成
    # エージェントを作成
    summarizer = chat_client.as_agent(
        instructions=summarizer_instructions,
        name="summarizer",
    )

    classifier = chat_client.as_agent(
        instructions=classifier_instructions,
        name="classifier",
    )

    action = chat_client.as_agent(
        instructions=action_instructions,
        name="action",
    )

    # 現在のフィードバックを初期化
    # 現在のフィードバックを初期化
    feedback="""
    I use the dashboard every day to monitor metrics, and it works well overall.
    But when I'm working late at night, the bright screen is really harsh on my eyes.
    If you added a dark mode option, it would make the experience much more comfortable.
    """

    # シーケンシャル オーケストレーションを構築
    # シーケンシャル オーケストレーションを構築
    workflow = SequentialBuilder(participants=[summarizer, classifier, action], output_from="all").build()

    # 実行して出力を収集
    # 実行して出力を収集
    result = await workflow.run(f"Customer feedback: {feedback}")
    outputs: list[Message] = []
    for response in result.get_outputs():
        outputs.extend(response.messages)

    # 出力を表示
    # 出力を表示
    if outputs:
        for i, msg in enumerate(outputs, start=1):
            name = msg.author_name or ("assistant" if msg.role == "assistant" else "user")
            print(f"{'-' * 60}\n{i:02d} [{name}]\n{msg.text}")


if __name__ == "__main__":
    asyncio.run(main())
