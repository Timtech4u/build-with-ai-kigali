"""
Demo 5: Voice Agent with Function Calling
Build with AI Kigali - Study Jam #2 (March 27, 2026)

A voice AI agent that can call tools (get_weather, convert_currency) and
speak the results. Shows how Gemini Live can be a real voice assistant
that takes actions, not just chats.
"""
import asyncio
import json
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


# ---- Tool Implementations ----

def get_weather(city: str) -> dict:
    """Simulate a weather API call."""
    weather_data = {
        "Kigali": {"temp_c": 24, "condition": "Partly cloudy", "humidity": 65},
        "Nairobi": {"temp_c": 22, "condition": "Sunny", "humidity": 55},
        "Lagos": {"temp_c": 31, "condition": "Humid and warm", "humidity": 80},
        "San Francisco": {"temp_c": 16, "condition": "Foggy", "humidity": 75},
        "Tokyo": {"temp_c": 18, "condition": "Clear skies", "humidity": 50},
    }
    # Case-insensitive lookup with fallback
    for known_city, data in weather_data.items():
        if known_city.lower() == city.lower():
            return {"city": known_city, **data}
    return {"city": city, "temp_c": 25, "condition": "Clear", "humidity": 60}


def convert_currency(amount: float, from_currency: str, to_currency: str) -> dict:
    """Simulate a currency conversion."""
    # Approximate rates relative to USD
    rates_to_usd = {
        "USD": 1.0, "RWF": 0.00076, "KES": 0.0077, "NGN": 0.00065,
        "EUR": 1.08, "GBP": 1.27, "JPY": 0.0067, "INR": 0.012,
    }
    from_c = from_currency.upper()
    to_c = to_currency.upper()
    if from_c not in rates_to_usd or to_c not in rates_to_usd:
        return {"error": f"Unknown currency: {from_c} or {to_c}"}
    usd_amount = amount * rates_to_usd[from_c]
    converted = usd_amount / rates_to_usd[to_c]
    return {
        "amount": amount,
        "from": from_c,
        "to": to_c,
        "converted_amount": round(converted, 2),
        "rate": round(rates_to_usd[from_c] / rates_to_usd[to_c], 6),
    }


TOOL_HANDLERS = {
    "get_weather": get_weather,
    "convert_currency": convert_currency,
}

# ---- Tool Declarations for Gemini ----

tools = [
    types.Tool(
        function_declarations=[
            types.FunctionDeclaration(
                name="get_weather",
                description="Get the current weather for a city.",
                parameters=types.Schema(
                    type=types.Type.OBJECT,
                    properties={
                        "city": types.Schema(
                            type=types.Type.STRING,
                            description="The city name, e.g. 'Kigali'",
                        ),
                    },
                    required=["city"],
                ),
            ),
            types.FunctionDeclaration(
                name="convert_currency",
                description="Convert an amount from one currency to another.",
                parameters=types.Schema(
                    type=types.Type.OBJECT,
                    properties={
                        "amount": types.Schema(
                            type=types.Type.NUMBER,
                            description="The amount to convert",
                        ),
                        "from_currency": types.Schema(
                            type=types.Type.STRING,
                            description="Source currency code (e.g. 'USD', 'RWF', 'KES')",
                        ),
                        "to_currency": types.Schema(
                            type=types.Type.STRING,
                            description="Target currency code (e.g. 'USD', 'RWF', 'EUR')",
                        ),
                    },
                    required=["amount", "from_currency", "to_currency"],
                ),
            ),
        ]
    )
]


async def run_query(session, query: str, turn_num: int) -> None:
    """Send a query, handle any tool calls, collect and play the final audio response."""
    print(f"  You: {query}")
    print(f"  [*] Sending...", end="", flush=True)

    await session.send_realtime_input(text=query)

    audio_chunks = []
    transcript = ""

    async for response in session.receive():
        # Check for tool call
        if response.tool_call:
            tool_call = response.tool_call
            print(f" tool call received!")

            function_responses = []
            for fc in tool_call.function_calls:
                func_name = fc.name
                func_args = fc.args if fc.args else {}
                print(f"    -> Calling {func_name}({json.dumps(func_args)})")

                # Execute the tool
                handler = TOOL_HANDLERS.get(func_name)
                if handler:
                    result = handler(**func_args)
                else:
                    result = {"error": f"Unknown function: {func_name}"}

                print(f"    <- Result: {json.dumps(result)}")

                function_responses.append(
                    types.FunctionResponse(
                        name=func_name,
                        response=result,
                        id=fc.id,
                    )
                )

            # Send tool response back
            print(f"  [*] Sending tool result, waiting for voice response...", end="", flush=True)
            await session.send_tool_response(function_responses=function_responses)
            continue

        # Check for server content (the spoken response after tool use)
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
        wav_file = f"/tmp/gemini-live-demo/function_turn{turn_num}.wav"
        pcm_to_wav(pcm_data, wav_file)
        duration = len(pcm_data) / (SAMPLE_RATE * SAMPLE_WIDTH * CHANNELS)
        print(f" done ({duration:.1f}s)")
        print(f"  AI: {transcript}")
        print(f"  [>] Playing...\n")
        subprocess.run(["afplay", wav_file])
    else:
        print(f" no audio.")


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
                "You are a helpful voice assistant with access to weather and currency tools. "
                "When asked about weather or currency, ALWAYS use the provided tools. "
                "After getting the tool result, give a natural spoken summary. "
                "Keep responses concise (1-2 sentences)."
            ))]
        ),
        tools=tools,
    )

    print("=" * 55)
    print("  Demo 5: Voice Agent with Function Calling")
    print("  (Weather + Currency tools)")
    print("=" * 55)
    print("\n[*] Connecting to Gemini 3.1 Flash Live...")

    async with client.aio.live.connect(
        model="gemini-3.1-flash-live-preview", config=config
    ) as session:
        print("[+] Connected! Running tool queries...\n")

        queries = [
            "What's the weather like in Kigali right now?",
            "Convert 100 US dollars to Rwandan francs.",
            "Compare the weather in Kigali and Lagos, and tell me which is hotter.",
        ]

        for i, query in enumerate(queries, 1):
            print(f"  --- Query {i} of {len(queries)} ---")
            await run_query(session, query, i)
            if i < len(queries):
                await asyncio.sleep(0.5)

    print("=" * 55)
    print("  Key takeaway: Gemini Live can call your tools")
    print("  and speak the results in real-time!")
    print("=" * 55)
    print("\n[+] Function calling demo complete!")


if __name__ == "__main__":
    asyncio.run(main())
