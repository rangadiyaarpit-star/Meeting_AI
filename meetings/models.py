from django.db import models

class Meeting(models.Model):
    # અહીં null=True અને blank=True ઉમેર્યું છે જેથી ટેક્સ્ટ મોડમાં એરર ન આવે
    audio_file = models.FileField(
        upload_to='audio/', 
        null=True, 
        blank=True
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

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"Meeting {self.id}"