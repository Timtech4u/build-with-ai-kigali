"""
Gemini 3.1 Flash Live API - Basic Demo
Build with AI Kigali - Study Jam #2 (March 27, 2026)

Connects via WebSocket and exchanges a text message.
"""
import asyncio
import os
from google import genai
from google.genai import types

client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])

async def main():
    config = types.LiveConnectConfig(
        response_modalities=[types.Modality.AUDIO],
        system_instruction=types.Content(
            parts=[types.Part(text="You are a friendly assistant. Keep responses brief and under 2 sentences.")]
        ),
        speech_config=types.SpeechConfig(
            voice_config=types.VoiceConfig(
                prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name="Puck")
            )
        ),
    )

    print("🔌 Connecting to Gemini 3.1 Flash Live...")

    async with client.aio.live.connect(
        model="gemini-3.1-flash-live-preview",
        config=config
    ) as session:
        print("✅ Connected to Gemini 3.1 Flash Live!\n")

        # Send text input
        await session.send_realtime_input(text="Say hello to the developers at Build with AI Kigali!")

        # Receive response
        audio_chunks = 0
        transcript = ""

        async for response in session.receive():
            content = response.server_content
            if content:
                if content.model_turn:
                    for part in content.model_turn.parts:
                        if part.inline_data:
                            audio_chunks += 1
                        if part.text:
                            transcript += part.text

                if content.output_transcription:
                    transcript += content.output_transcription.text

                if content.turn_complete:
                    break

        print(f"📊 Received {audio_chunks} audio chunks")
        if transcript:
            print(f"📝 Transcript: {transcript}")
        else:
            print("📝 (Audio response received - enable transcription to see text)")
        print("\n✅ Session complete!")

    print("🔌 Disconnected.")

if __name__ == "__main__":
    asyncio.run(main())
