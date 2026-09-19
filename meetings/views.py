from django.shortcuts import render, redirect, get_object_or_404
from .forms import MeetingForm
from .models import Meeting
from .utils.ai_notes import generate_notes

try:
    from .utils.transcribe import transcribe_audio
except:
    transcribe_audio = None
    


def home(request):
    form = MeetingForm()
    meetings = Meeting.objects.all().order_by('-created_at')
    
    return render(
        request,
        'home.html',
        {
            'form': form, 
            'meetings': meetings
        }
    )


def upload_audio(request):
    if request.method == "POST":
        input_mode = request.POST.get("input_mode", "file")
        transcript = ""
        meeting = None

        # ૧. જો યુઝરે TEXT INPUT પસંદ કર્યું હોય
        if input_mode == "text":
            text_input = request.POST.get("text_input", "").strip()
            if text_input:
                meeting = Meeting.objects.create(transcript=text_input)
                transcript = text_input
            else:
                return redirect("/")

        # ૨. જો યુઝરે MICROPHONE (MIC) પસંદ કર્યું હોય
        elif input_mode == "mic":
            if 'recorded_audio' in request.FILES:
                meeting = Meeting(audio_file=request.FILES['recorded_audio'])
                meeting.save()
                
                try:
                    if transcribe_audio:
                        transcript = transcribe_audio(meeting.audio_file.path)
                    else:
                        transcript = "Microphone transcription module not found."
                except Exception as e:
                    transcript = f"Mic Transcription Error: {str(e)}"
            else:
                return redirect("/")

        # ૩. જો યુઝરે નોર્મલ FILE UPLOAD (MP3/WAV) પસંદ કર્યું હોય
        else:
            form = MeetingForm(request.POST, request.FILES)
            if form.is_valid():
                meeting = form.save()
                try:
                    if transcribe_audio:
                        transcript = transcribe_audio(meeting.audio_file.path)
                    else:
                        transcript = "Transcription module not found."
                except Exception as e:
                    transcript = f"File Transcription Error: {str(e)}"
            else:
                return redirect("/")

        # --- ઓટોમેટિક AI SUMMARY & ACTION ITEMS જનરેશન ---
        if meeting and transcript and not transcript.startswith("Error:"):
            meeting.transcript = transcript
            try:
                # generate_notes() માંથી આવતી સમરી સેટ કરવી
                # (જો તમારું આ ફંક્શન અલગથી action_items આપતું હોય તો તે મુજબ સેટ કરી શકો છો, 
                # અહીં આપણે અત્યારે સિંગલ AI આઉટપુટ તરીકે હેન્ડલ કર્યું છે)
                meeting.summary = generate_notes(transcript)
                meeting.action_items = "Generated automatically via AI Notes dashboard."
            except Exception as e:
                meeting.summary = f"AI Notes Generation Error: {str(e)}"
            meeting.save()

        if not meeting:
            return redirect("/")

        return render(
            request,
            "success.html",
            {
                "meeting": meeting,
                "transcript": transcript
            }
        )

    return redirect("/")


def meeting_detail(request, meeting_id):
    meeting = get_object_or_400(Meeting, id=meeting_id)
    return render(
        request,
        "meeting_detail.html",
        {
            "meeting": meeting
        }
    )


def delete_meeting(request, meeting_id):
    meeting = get_object_or_404(Meeting, id=meeting_id)
    meeting.delete()
    return redirect("/")


def generate_ai_notes(request, meeting_id):
    meeting = get_object_or_400(Meeting, id=meeting_id)

    if meeting.transcript:
        try:
            meeting.summary = generate_notes(meeting.transcript)
            meeting.save()
        except Exception as e:
            meeting.summary = str(e)
            meeting.save()

    return render(
        request,
        "success.html",
        {
            "meeting": meeting,
            "transcript": meeting.transcript
        }
    )