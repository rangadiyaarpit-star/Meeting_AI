from faster_whisper import WhisperModel

_model = None


def get_model():
    global _model

    if _model is None:
        print("Loading Multilingual Whisper model...")

        _model = WhisperModel(
            "tiny",
            device="cpu",
            compute_type="int8",
            cpu_threads=2,
        )

        print("Multilingual Whisper loaded successfully")

    return _model


def transcribe_audio(audio_path):
    print(f"Audio Path: {audio_path}")

    model = get_model()

    # language=None = automatic language detection
    segments, info = model.transcribe(
        audio_path,
        language=None,
        task="transcribe",
        beam_size=1,
    )

    transcript = " ".join(
        segment.text for segment in segments
    ).strip()

    print(f"Detected language: {info.language}")
    print(f"Language probability: {info.language_probability}")
    print("TRANSCRIPT RESULT:")
    print(transcript)

    return transcript