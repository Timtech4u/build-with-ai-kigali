"""
🎤 Gemini 3.1 Flash Live API - Interactive Chat Demo
Build with AI Kigali - Study Jam #2 (March 27, 2026)

This demo shows:
1. Connecting to Gemini 3.1 Flash Live via WebSocket
2. Sending text messages in real-time
3. Receiving audio + transcription responses
4. Multiple conversation turns

Requirements:
    pip install google-genai
    export GOOGLE_API_KEY=your-key
"""
import asyncio
import os
from google import genai
from google.genai import types

client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])

async def chat():
    # Step 1: Configure the Live session
    config = types.LiveConnectConfig(
        response_modalities=[types.Modality.AUDIO],
        system_instruction=types.Content(
            parts=[types.Part(text=(
                "You are a friendly AI assistant at a developer meetup in Kigali, Rwanda. "
                "Keep responses brief (1-2 sentences). Be encouraging about building with AI."
            ))]
        ),
        speech_config=types.SpeechConfig(
            voice_config=types.VoiceConfig(
                prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name="Puck")
            )
        ),
        output_audio_transcription=types.AudioTranscriptionConfig(),
    )

    print("=" * 50)
    print("🎤 Gemini 3.1 Flash Live - Chat Demo")
    print("=" * 50)
    print("Connecting...\n")

    async with client.aio.live.connect(
        model="gemini-3.1-flash-live-preview",
        config=config
    ) as session:
        print("✅ Connected!\n")

        # Step 2: Have a conversation
        messages = [
            "Hello! What can Gemini 3.1 Flash Live do?",
            "How would I build a voice assistant with it?",
            "What makes it different from a regular API call?",
        ]

        for i, msg in enumerate(messages, 1):
            print(f"👤 You: {msg}")

            # Send text
            await session.send_realtime_input(text=msg)

            # Receive response
            transcript = ""
            audio_size = 0

            async for response in session.receive():
                content = response.server_content
                if content:
                    if content.model_turn:
                        for part in content.model_turn.parts:
                            if part.inline_data:
                                audio_size += len(part.inline_data.data)
                    if content.output_transcription:
                        transcript += content.output_transcription.text
                    if content.turn_complete:
                        break

            print(f"🤖 Gemini: {transcript}")
            print(f"   📊 Audio: {audio_size:,} bytes\n")

            # Small pause between turns
            if i < len(messages):
                await asyncio.sleep(0.5)

    print("=" * 50)
    print("✅ Demo complete! Session closed.")
    print("=" * 50)

if __name__ == "__main__":
    asyncio.run(chat())
