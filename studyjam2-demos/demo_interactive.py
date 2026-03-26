"""
Demo 4: Interactive Voice Chat - Audience Participation!
Build with AI Kigali - Study Jam #2 (March 27, 2026)

The presenter types whatever the audience suggests, and the AI responds
with spoken audio played through the speakers. Type 'quit' to exit.
"""
import asyncio
import os
import struct
import subprocess
from google import genai
from google.genai import types

client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])

SAMPLE_RATE = 24000
SAMPLE_WIDTH = 2
CHANNELS = 1


def pcm_to_wav(pcm_data: bytes, filename: str) -> str:
    """Convert raw PCM (24kHz, 16-bit, mono) to a WAV file."""
    data_size = len(pcm_data)
    with open(filename, "wb") as f:
        f.write(b"RIFF")
        f.write(struct.pack("<I", 36 + data_size))
        f.write(b"WAVE")
        f.write(b"fmt ")
        f.write(struct.pack("<I", 16))
        f.write(struct.pack("<H", 1))
        f.write(struct.pack("<H", CHANNELS))
        f.write(struct.pack("<I", SAMPLE_RATE))
        f.write(struct.pack("<I", SAMPLE_RATE * CHANNELS * SAMPLE_WIDTH))
        f.write(struct.pack("<H", CHANNELS * SAMPLE_WIDTH))
        f.write(struct.pack("<H", SAMPLE_WIDTH * 8))
        f.write(b"data")
        f.write(struct.pack("<I", data_size))
        f.write(pcm_data)
    return filename


async def main():
    config = types.LiveConnectConfig(
        response_modalities=[types.Modality.AUDIO],
        speech_config=types.SpeechConfig(
            voice_config=types.VoiceConfig(
                prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name="Puck")
            )
        ),
        output_audio_transcription=types.AudioTranscriptionConfig(),
        system_instruction=types.Content(
            parts=[types.Part(text=(
                "You are a witty, knowledgeable AI assistant at a developer meetup in Kigali, Rwanda. "
                "The audience is asking you questions live. Be engaging, concise (2-3 sentences max), "
                "and occasionally add humor. You love talking about AI, coding, and Africa's tech scene."
            ))]
        ),
    )

    print("=" * 55)
    print("  Demo 4: Interactive Voice Chat")
    print("  Type anything, hear the AI respond!")
    print("  Type 'quit' to exit")
    print("=" * 55)
    print("\n[*] Connecting to Gemini 3.1 Flash Live...")

    async with client.aio.live.connect(
        model="gemini-3.1-flash-live-preview", config=config
    ) as session:
        print("[+] Connected! Ready for audience questions.\n")

        turn = 0
        while True:
            try:
                user_input = await asyncio.get_event_loop().run_in_executor(
                    None, lambda: input("  You > ")
                )
            except (EOFError, KeyboardInterrupt):
                print("\n\n[*] Exiting...")
                break

            user_input = user_input.strip()
            if not user_input:
                continue
            if user_input.lower() in ("quit", "exit", "q"):
                print("\n[*] Goodbye!")
                break

            turn += 1
            print(f"  [*] Thinking...", end="", flush=True)

            await session.send_realtime_input(text=user_input)

            audio_chunks = []
            transcript = ""

            async for response in session.receive():
                content = response.server_content
                if content:
                    if content.model_turn:
                        for part in content.model_turn.parts:
                            if part.inline_data:
                                audio_chunks.append(part.inline_data.data)
                    if content.output_transcription:
                        transcript += content.output_transcription.text
                    if content.turn_complete:
                        break

            if audio_chunks:
                pcm_data = b"".join(audio_chunks)
                wav_file = f"/tmp/gemini-live-demo/interactive_turn{turn}.wav"
                pcm_to_wav(pcm_data, wav_file)
                duration = len(pcm_data) / (SAMPLE_RATE * SAMPLE_WIDTH * CHANNELS)

                print(f" done ({duration:.1f}s)")
                print(f"  AI: {transcript}")
                print(f"  [>] Playing...\n")
                subprocess.run(["afplay", wav_file])
            else:
                print(" no audio received.")

    print("\n[+] Session ended. All audio saved to /tmp/gemini-live-demo/")


if __name__ == "__main__":
    asyncio.run(main())
