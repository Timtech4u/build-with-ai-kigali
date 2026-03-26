"""
Demo 2: Voice Showcase - Hear 4 Different AI Voices
Build with AI Kigali - Study Jam #2 (March 27, 2026)

Generates the same phrase with 4 different voices (Puck, Charon, Kore, Aoede)
and plays them back-to-back so the audience can hear the differences.
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

VOICES = ["Puck", "Charon", "Kore", "Aoede"]
PROMPT = "Hello! I'm speaking at Build with AI in Kigali, Rwanda. Let's build something amazing together!"


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


async def generate_with_voice(voice_name: str) -> tuple[bytes, str]:
    """Connect to Gemini Live with a specific voice and return (pcm_audio, transcript)."""
    config = types.LiveConnectConfig(
        response_modalities=[types.Modality.AUDIO],
        speech_config=types.SpeechConfig(
            voice_config=types.VoiceConfig(
                prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name=voice_name)
            )
        ),
        output_audio_transcription=types.AudioTranscriptionConfig(),
        system_instruction=types.Content(
            parts=[types.Part(text=(
                "You are an AI assistant introducing yourself at a developer meetup. "
                "Say the user's message naturally and with personality. Keep it to 1-2 sentences."
            ))]
        ),
    )

    async with client.aio.live.connect(
        model="gemini-3.1-flash-live-preview", config=config
    ) as session:
        await session.send_realtime_input(text=PROMPT)

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

    return b"".join(audio_chunks), transcript


async def main():
    print("=" * 55)
    print("  Demo 2: Voice Showcase (4 AI Voices)")
    print("=" * 55)
    print(f"\n  Prompt: \"{PROMPT}\"\n")

    wav_files = []

    for voice in VOICES:
        print(f"[*] Generating with voice: {voice}...")
        try:
            pcm_data, transcript = await generate_with_voice(voice)
            if not pcm_data:
                print(f"    [!] No audio received for {voice}, skipping.")
                continue

            wav_file = f"/tmp/gemini-live-demo/voice_{voice.lower()}.wav"
            pcm_to_wav(pcm_data, wav_file)
            duration = len(pcm_data) / (SAMPLE_RATE * SAMPLE_WIDTH * CHANNELS)

            print(f"    Transcript: {transcript}")
            print(f"    Audio: {duration:.1f}s | Saved: {wav_file}")
            wav_files.append((voice, wav_file))
        except Exception as e:
            print(f"    [!] Error with {voice}: {e}")

    if not wav_files:
        print("\n[!] No audio generated.")
        return

    # Playback phase
    print(f"\n{'=' * 55}")
    print("  Playing all voices back-to-back...")
    print(f"{'=' * 55}\n")

    for voice, wav_file in wav_files:
        print(f"[>] Now playing: {voice}")
        subprocess.run(["afplay", wav_file])
        print()

    print("[+] Voice showcase complete!")


if __name__ == "__main__":
    asyncio.run(main())
