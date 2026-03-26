"""
Demo 1: Hello Kigali! - Simplest Gemini 3.1 Flash Live Demo
Build with AI Kigali - Study Jam #2 (March 27, 2026)

Sends a greeting, receives audio, saves to WAV, and plays it through speakers.
This is the "Hello World" of real-time AI voice -- under 60 lines of code.
"""
import asyncio
import os
import struct
import subprocess
import tempfile
from google import genai
from google.genai import types

client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])

SAMPLE_RATE = 24000
SAMPLE_WIDTH = 2  # 16-bit
CHANNELS = 1


def pcm_to_wav(pcm_data: bytes, filename: str) -> str:
    """Convert raw PCM (24kHz, 16-bit, mono) to a WAV file."""
    data_size = len(pcm_data)
    with open(filename, "wb") as f:
        # WAV header
        f.write(b"RIFF")
        f.write(struct.pack("<I", 36 + data_size))
        f.write(b"WAVE")
        f.write(b"fmt ")
        f.write(struct.pack("<I", 16))  # chunk size
        f.write(struct.pack("<H", 1))   # PCM format
        f.write(struct.pack("<H", CHANNELS))
        f.write(struct.pack("<I", SAMPLE_RATE))
        f.write(struct.pack("<I", SAMPLE_RATE * CHANNELS * SAMPLE_WIDTH))  # byte rate
        f.write(struct.pack("<H", CHANNELS * SAMPLE_WIDTH))  # block align
        f.write(struct.pack("<H", SAMPLE_WIDTH * 8))  # bits per sample
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
            parts=[types.Part(text="You are an enthusiastic AI at a developer meetup. Keep responses to 1-2 sentences.")]
        ),
    )

    print("=" * 55)
    print("  Demo 1: Hello Kigali! (Gemini 3.1 Flash Live)")
    print("=" * 55)
    print("\n[*] Connecting to Gemini 3.1 Flash Live...")

    async with client.aio.live.connect(
        model="gemini-3.1-flash-live-preview", config=config
    ) as session:
        print("[+] Connected! Sending greeting...\n")

        await session.send_realtime_input(text="Hello Kigali! Greet the developers at Build with AI Kigali!")

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

        if not audio_chunks:
            print("[!] No audio received.")
            return

        # Combine all audio chunks
        pcm_data = b"".join(audio_chunks)
        wav_file = "/tmp/gemini-live-demo/hello_kigali.wav"
        pcm_to_wav(pcm_data, wav_file)

        duration = len(pcm_data) / (SAMPLE_RATE * SAMPLE_WIDTH * CHANNELS)
        print(f"    Transcript: {transcript}")
        print(f"    Audio: {len(pcm_data):,} bytes ({duration:.1f}s)")
        print(f"    Saved: {wav_file}")
        print(f"\n[>] Playing audio...\n")

        # Play the WAV file (macOS)
        subprocess.run(["afplay", wav_file])

        print("\n[+] Done!")


if __name__ == "__main__":
    asyncio.run(main())
