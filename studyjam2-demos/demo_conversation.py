"""
Demo 3: Multi-Turn Conversation - AI Remembers Context
Build with AI Kigali - Study Jam #2 (March 27, 2026)

Shows a 3-turn conversation within a single Live session where the AI
maintains context across turns. Each response is saved as audio and played.
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

CONVERSATION = [
    "My name is Timothy and I'm from Rwanda. I'm building a cloud platform called HostSpaceCloud.",
    "What kind of features would you suggest I add to my cloud platform?",
    "Can you remember my name and summarize what we've talked about so far?",
]


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
                "You are a friendly and knowledgeable AI assistant helping a developer. "
                "Remember everything the user tells you across the conversation. "
                "Keep responses to 2-3 sentences maximum."
            ))]
        ),
    )

    print("=" * 55)
    print("  Demo 3: Multi-Turn Conversation")
    print("  (AI remembers context across turns)")
    print("=" * 55)
    print("\n[*] Connecting to Gemini 3.1 Flash Live...")

    async with client.aio.live.connect(
        model="gemini-3.1-flash-live-preview", config=config
    ) as session:
        print("[+] Connected! Starting conversation...\n")

        wav_files = []

        for turn_num, message in enumerate(CONVERSATION, 1):
            print(f"  --- Turn {turn_num} of {len(CONVERSATION)} ---")
            print(f"  You: {message}\n")

            await session.send_realtime_input(text=message)

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
                wav_file = f"/tmp/gemini-live-demo/conversation_turn{turn_num}.wav"
                pcm_to_wav(pcm_data, wav_file)
                duration = len(pcm_data) / (SAMPLE_RATE * SAMPLE_WIDTH * CHANNELS)

                print(f"  AI: {transcript}")
                print(f"  [{duration:.1f}s audio]\n")

                wav_files.append((turn_num, wav_file))

                # Play the response immediately
                print(f"  [>] Playing response...\n")
                subprocess.run(["afplay", wav_file])
            else:
                print(f"  [!] No audio received for turn {turn_num}\n")

            # Brief pause between turns
            if turn_num < len(CONVERSATION):
                await asyncio.sleep(0.5)

    print("=" * 55)
    print("  Key takeaway: Single WebSocket session maintains")
    print("  full conversational context across all turns!")
    print("=" * 55)
    print("\n[+] Conversation complete!")


if __name__ == "__main__":
    asyncio.run(main())
