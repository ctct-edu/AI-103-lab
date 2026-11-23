import os
import asyncio
import base64
import queue
from dotenv import load_dotenv
import pyaudio

# 名前空間のインポート



def main():
    """メイン エントリ ポイント。"""

    try:
        # コンソールをクリア
        os.system('cls' if os.name == 'nt' else 'clear')

        # 環境変数から必要な構成を取得
        load_dotenv()
        endpoint = os.environ.get("AZURE_VOICELIVE_ENDPOINT")
        agent_name = os.environ.get("AZURE_VOICELIVE_AGENT_ID")
        project_name = os.environ.get("AZURE_VOICELIVE_PROJECT_NAME")
        agent_config = AgentConfig({ "agent_name": agent_name, "project_name": project_name })


        # 認証用の資格情報を作成
        credential = AzureCliCredential()

        # 音声アシスタントを作成して開始
        assistant = VoiceAssistant(
            endpoint=endpoint,
            credential=credential,
            agent_config = agent_config
        )

        # アシスタントを実行
        try:
            asyncio.run(assistant.start())
        except KeyboardInterrupt:
            # ユーザーが CTRL+C を押したら終了
            print("\n👋 さようなら!")


    except Exception as e:
        print(f"❌ エラーが発生しました: {e}")


# VoiceAssistant クラス - 音声エージェントの中心となるクラス
class VoiceAssistant:
    """
    会話の流れを調整するメインの音声アシスタント。

    このクラスは Azure VoiceLive の基本パターンを示します。
    1. サービスに接続する
    2. セッションを構成する
    3. 音声の入出力 (キャプチャ/再生) を開始する
    4. サービスからのイベントを処理する
    """

    def __init__(self, endpoint, credential, agent_config):
        self.endpoint = endpoint
        self.credential = credential
        self.agent_config = agent_config
    async def start(self):
        """音声アシスタントを開始します。"""
        print("\n" + "=" * 60)
        print("🎙️  AZURE VOICELIVE 音声エージェント")
        print("=" * 60)

        # この try ブロックにコードを追加します!
        try:
            pass  # コードを追加したら、この行は削除してかまいません
            # ステップ 1: Azure VoiceLive をエージェントに接続


                # ステップ 2: オーディオ プロセッサを初期化


                # ステップ 3: セッションを構成


                # ステップ 4: オーディオ システムを開始


                # ステップ 5: イベントを処理



        finally:
            if hasattr(self, 'audio_processor'):
                self.audio_processor.shutdown()

    async def setup_session(self):
        """音声設定でセッションを構成します。"""

        session_config = RequestSession(
            # テキストと音声の両方を有効にする
            modalities=[Modality.TEXT, Modality.AUDIO],

            # 日本語を話す音声を指定する (エージェントに設定された音声を上書き)
            voice=AzureStandardVoice(name="ja-JP-Nanami:DragonHDLatestNeural"),

            # 音声形式 (24kHz、16 ビット PCM)
            input_audio_format=InputAudioFormat.PCM16,
            output_audio_format=OutputAudioFormat.PCM16,

            # 音声アクティビティ検出 (発話を検出するタイミング)
            turn_detection=AzureSemanticVadMultilingual(),

            # スピーカーからのエコーを防止
            input_audio_echo_cancellation=AudioEchoCancellation(),

            # 背景ノイズを低減
            input_audio_noise_reduction=AudioNoiseReduction(type="azure_deep_noise_suppression")
        )

        await self.connection.session.update(session=session_config)
        print("⚙️  セッションを構成しました")

    async def process_events(self):
        """VoiceLive サービスからのイベントを処理します。"""

        # サービスからのイベントを待ち受ける
        async for event in self.connection:
            await self.handle_event(event)

    async def handle_event(self, event):
        """サービスからのさまざまな種類のイベントを処理します。"""

        # セッションの準備ができた - 音声のキャプチャを開始
        if event.type == ServerEventType.SESSION_UPDATED:
            print(f"📡 エージェントに接続しました: {event.session.agent.name}")
            self.audio_processor.start_capture()

        # ユーザーの音声が文字起こしされた
        elif event.type == ServerEventType.CONVERSATION_ITEM_INPUT_AUDIO_TRANSCRIPTION_COMPLETED:
            print(f'👤 あなた: {event.get("transcript", "")}')

        # エージェントが音声の文字起こしとともに応答している
        elif event.type == ServerEventType.RESPONSE_AUDIO_TRANSCRIPT_DONE:
            print(f'🤖 エージェント: {event.get("transcript", "")}')

        # ユーザーが話し始めた (再生中の音声を中断)
        elif event.type == ServerEventType.INPUT_AUDIO_BUFFER_SPEECH_STARTED:
            self.audio_processor.clear_playback_queue()
            print("🎤 聞いています...")

        # ユーザーが話し終えた
        elif event.type == ServerEventType.INPUT_AUDIO_BUFFER_SPEECH_STOPPED:
            print("🤔 考えています...")

        # 音声応答のチャンクを受信
        elif event.type == ServerEventType.RESPONSE_AUDIO_DELTA:
            self.audio_processor.queue_audio(event.delta)

        # 音声応答が完了
        elif event.type == ServerEventType.RESPONSE_AUDIO_DONE:
            print("✓ 応答が完了しました\n")

        # エラーを処理
        elif event.type == ServerEventType.ERROR:
            print(f"❌ エラー: {event.error.message}")


# AudioProcessor クラス - PyAudio を使用してマイク入力とスピーカー出力を処理
class AudioProcessor:
    """
    音声入力 (マイク) と音声出力 (スピーカー) を処理します。

    主な役割:
    - マイクから音声をキャプチャして VoiceLive に送信する
    - VoiceLive から音声を受信してスピーカーで再生する
    """

    def __init__(self, connection):
        self.connection = connection
        self.audio = pyaudio.PyAudio()

        # 音声設定: 24kHz、16 ビット PCM、モノラル
        self.format = pyaudio.paInt16
        self.channels = 1
        self.rate = 24000
        self.chunk_size = 1200  # 50ms のチャンク

        # 入力と出力のストリーム
        self.input_stream = None
        self.output_stream = None
        self.playback_queue = queue.Queue()

    def start_capture(self):
        """マイクからの音声キャプチャを開始します。"""

        def capture_callback(in_data, frame_count, time_info, status):
            # 音声を base64 に変換して VoiceLive に送信
            audio_base64 = base64.b64encode(in_data).decode("utf-8")
            asyncio.run_coroutine_threadsafe(
                self.connection.input_audio_buffer.append(audio=audio_base64),
                self.loop
            )
            return (None, pyaudio.paContinue)

        # コールバック スレッドで使用するためにイベント ループを保存
        self.loop = asyncio.get_event_loop()

        self.input_stream = self.audio.open(
            format=self.format,
            channels=self.channels,
            rate=self.rate,
            input=True,
            frames_per_buffer=self.chunk_size,
            stream_callback=capture_callback
        )
        print("🎤 マイクを開始しました")

    def start_playback(self):
        """音声再生システムを開始します。"""

        remaining = bytes()

        def playback_callback(in_data, frame_count, time_info, status):
            nonlocal remaining

            # 必要なバイト数を計算
            bytes_needed = frame_count * pyaudio.get_sample_size(pyaudio.paInt16)
            output = remaining[:bytes_needed]
            remaining = remaining[bytes_needed:]

            # 必要に応じてキューからさらに音声を取得
            while len(output) < bytes_needed:
                try:
                    audio_data = self.playback_queue.get_nowait()
                    if audio_data is None:  # 終了シグナル
                        break
                    output += audio_data
                except queue.Empty:
                    # 利用可能な音声がない場合は無音で埋める
                    output += bytes(bytes_needed - len(output))
                    break

            # 余った分は次のコールバックのために保持
            if len(output) > bytes_needed:
                remaining = output[bytes_needed:]
                output = output[:bytes_needed]

            return (output, pyaudio.paContinue)

        self.output_stream = self.audio.open(
            format=self.format,
            channels=self.channels,
            rate=self.rate,
            output=True,
            frames_per_buffer=self.chunk_size,
            stream_callback=playback_callback
        )
        print("🔊 スピーカーの準備ができました")

    def queue_audio(self, audio_data):
        """音声データを再生キューに追加します。"""
        self.playback_queue.put(audio_data)

    def clear_playback_queue(self):
        """保留中の音声をクリアします (ユーザーが割り込んだときに使用)。"""
        while not self.playback_queue.empty():
            try:
                self.playback_queue.get_nowait()
            except queue.Empty:
                break

    def shutdown(self):
        """音声リソースをクリーンアップします。"""
        if self.input_stream:
            self.input_stream.stop_stream()
            self.input_stream.close()

        if self.output_stream:
            self.playback_queue.put(None)  # 終了シグナル
            self.output_stream.stop_stream()
            self.output_stream.close()

        self.audio.terminate()
        print("🔇 音声を停止しました")





if __name__ == "__main__":
    main()
