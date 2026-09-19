from faster_whisper import WhisperModel

_model = None


def get_model():
    global _model

    if _model is None:
        print("Loading Faster Whisper model...")

        _model = WhisperModel(
            "tiny.en",
            device="cpu",
            compute_type="int8",
            cpu_threads=2,
        )

        print("Faster Whisper loaded successfully")

    return _model


def transcribe_audio(audio_path):
    print(f"Audio Path: {audio_path}")

    model = get_model()

    segments, info = model.transcribe(
        audio_path,
        language="en",
        beam_size=1,
    )

    transcript = " ".join(
        segment.text for segment in segments
    ).strip()

    print("TRANSCRIPT RESULT:")
    print(transcript)

    return transcript