import whisper

print("Loading Whisper Model...")

model = whisper.load_model("small")

print("Whisper Loaded Successfully")


def transcribe_audio(audio_path):

    print(f"Audio Path: {audio_path}")

    result = model.transcribe(
        audio_path,
        fp16=False,
        language="en"
    )

    print("TRANSCRIPT RESULT:")
    print(result)

    return result["text"].strip()