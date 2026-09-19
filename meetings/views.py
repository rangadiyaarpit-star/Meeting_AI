from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse

from .forms import MeetingForm
from .models import Meeting


def health(request):
    return JsonResponse({"status": "ok"})


def home(request):
    form = MeetingForm()
    meetings = Meeting.objects.all().order_by("-created_at")

    return render(
        request,
        "home.html",
        {
            "form": form,
            "meetings": meetings,
        },
    )


def upload_audio(request):
    if request.method != "POST":
        return redirect("/")

    input_mode = request.POST.get("input_mode", "file")
    transcript = ""
    meeting = None

    # =========================================================
    # 1. TEXT INPUT
    # =========================================================
    if input_mode == "text":
        text_input = request.POST.get("text_input", "").strip()

        if not text_input:
            return redirect("/")

        meeting = Meeting.objects.create(
            transcript=text_input
        )
        transcript = text_input

    # =========================================================
    # 2. MICROPHONE
    # =========================================================
    elif input_mode == "mic":
        if "recorded_audio" not in request.FILES:
            return redirect("/")

        meeting = Meeting(
            audio_file=request.FILES["recorded_audio"]
        )
        meeting.save()

        try:
            # IMPORTANT:
            # Whisper/Torch module only loads when actually needed
            from .utils.transcribe import transcribe_audio

            transcript = transcribe_audio(
                meeting.audio_file.path
            )

        except Exception as e:
            transcript = f"Mic Transcription Error: {str(e)}"

    # =========================================================
    # 3. NORMAL FILE UPLOAD
    # =========================================================
    else:
        form = MeetingForm(
            request.POST,
            request.FILES
        )

        if not form.is_valid():
            return redirect("/")

        meeting = form.save()

        try:
            # IMPORTANT:
            # Do not import Whisper at server startup
            from .utils.transcribe import transcribe_audio

            transcript = transcribe_audio(
                meeting.audio_file.path
            )

        except Exception as e:
            transcript = f"File Transcription Error: {str(e)}"

    # =========================================================
    # SAVE TRANSCRIPT + AI NOTES
    # =========================================================
    if meeting and transcript and not transcript.startswith("Error:"):

        meeting.transcript = transcript

        try:
            # Lazy import AI notes too
            from .utils.ai_notes import generate_notes

            meeting.summary = generate_notes(transcript)
            meeting.action_items = (
                "Generated automatically via AI Notes dashboard."
            )

        except Exception as e:
            meeting.summary = (
                f"AI Notes Generation Error: {str(e)}"
            )

        meeting.save()

    if not meeting:
        return redirect("/")

    return render(
        request,
        "success.html",
        {
            "meeting": meeting,
            "transcript": transcript,
        },
    )


def meeting_detail(request, meeting_id):
    # FIXED: get_object_or_400 -> get_object_or_404
    meeting = get_object_or_404(
        Meeting,
        id=meeting_id
    )

    return render(
        request,
        "meeting_detail.html",
        {
            "meeting": meeting
        },
    )


def delete_meeting(request, meeting_id):
    meeting = get_object_or_404(
        Meeting,
        id=meeting_id
    )

    meeting.delete()

    return redirect("/")


def generate_ai_notes(request, meeting_id):
    # FIXED: get_object_or_400 -> get_object_or_404
    meeting = get_object_or_404(
        Meeting,
        id=meeting_id
    )

    if meeting.transcript:
        try:
            # Lazy import
            from .utils.ai_notes import generate_notes

            meeting.summary = generate_notes(
                meeting.transcript
            )

        except Exception as e:
            meeting.summary = str(e)

        meeting.save()

    return render(
        request,
        "success.html",
        {
            "meeting": meeting,
            "transcript": meeting.transcript,
        },
    )