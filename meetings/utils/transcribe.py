import whisper

_model = None


def get_model():
    global _model

    if _model is None:
        print("Loading Whisper Model...")

        _model = whisper.load_model(
            "tiny",
            device="cpu"
        )

        print("Whisper Loaded Successfully")

    return _model


def transcribe_audio(audio_path):
    print(f"Audio Path: {audio_path}")

    model = get_model()

    result = model.transcribe(
        audio_path,
        fp16=False,
        language="en"
    )

    print("TRANSCRIPT RESULT:")
    print(result)

    return result["text"].strip()