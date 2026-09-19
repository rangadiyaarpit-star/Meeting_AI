from django.urls import path
from . import views

urlpatterns = [

    # Home page
    path(
        "",
        views.home,
        name="home"
    ),

    # Upload audio / text / microphone
    path(
        "upload/",
        views.upload_audio,
        name="upload_audio"
    ),

    # Meeting details
    path(
        "meeting/<int:meeting_id>/",
        views.meeting_detail,
        name="meeting_detail"
    ),

    # Generate AI notes
    path(
        "generate-notes/<int:meeting_id>/",
        views.generate_ai_notes,
        name="generate_notes"
    ),

    # Render health check
    path(
        "health/",
        views.health,
        name="health"
    ),
]