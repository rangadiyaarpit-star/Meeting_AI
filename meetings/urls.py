from django.urls import path

from . import views



urlpatterns = [



    path(

        '',

        views.home,

        name='home'

    ),



    path(

        'upload/',

        views.upload_audio,

        name='upload_audio'

    ),



    path(

        'meeting/<int:meeting_id>/',

        views.meeting_detail,

        name='meeting_detail'

    ),



    path(

        'generate-notes/<int:meeting_id>/',

        views.generate_ai_notes,

        name='generate_notes'

    ),



]