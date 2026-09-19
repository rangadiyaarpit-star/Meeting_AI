from django.db import models


class Meeting(models.Model):

    title = models.CharField(
        max_length=255,
        blank=True
    )

    audio_file = models.FileField(
        upload_to='audio/'
    )

    transcript = models.TextField(
        blank=True
    )

    summary = models.TextField(
        blank=True
    )

    action_items = models.TextField(
        blank=True
    )

    notes_version = models.IntegerField(
        default=1
    )

    duration = models.CharField(
        max_length=50,
        blank=True
    )

    sentiment = models.CharField(
        max_length=50,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):

        if self.title:
            return self.title

        return f"Meeting {self.id}"