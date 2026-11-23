"""
公開されているMCPサーバー（Streamable HTTP方式）のツール一覧を確認するスクリプト

対象: Microsoft Learn MCP Server など、リモートでホストされているMCPサーバー
     （ローカルで自作したstdio方式のサーバーではなく、URLで接続するタイプ）

前提: 演習02で使用した labenv 仮想環境には mcp パッケージが
     インストール済みのため、そのまま実行できます。
     もし別環境で実行する場合は事前に:
         pip install mcp --break-system-packages
"""
import asyncio
import json
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

# 調べたいMCPサーバーのURLをここに指定してください
MCP_SERVER_URL = "https://learn.microsoft.com/api/mcp"


async def main():
    # MCPサーバーへ接続（HTTPストリーミング）
    async with streamablehttp_client(MCP_SERVER_URL) as (read, write, get_session_id):
        # セッションを作成
        async with ClientSession(read, write) as session:
            # セッションを初期化（サーバーとのハンドシェイク）
            await session.initialize()

            # 利用可能なツール一覧を取得
            tools_result = await session.list_tools()

            print(f"接続先: {MCP_SERVER_URL}")
            print(f"利用可能なツール数: {len(tools_result.tools)}\n")

            for tool in tools_result.tools:
                # inputSchema は dict（JSON Schema形式）なので整形して出力
                schema_str = json.dumps(tool.inputSchema, indent=2, ensure_ascii=False)
                # 各行を字下げして見やすくする
                schema_indented = "\n".join(f"    {line}" for line in schema_str.splitlines())

                print(f"■ {tool.name}")
                print(f"  説明: {tool.description}")
                print(f"  パラメータ定義:")
                print(schema_indented)
                print()


if __name__ == "__main__":
    asyncio.run(main())