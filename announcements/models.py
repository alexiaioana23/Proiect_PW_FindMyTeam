from django.db import models
from django.contrib.auth.models import User


class Announcement(models.Model):

    CATEGORY_CHOICES = [
        ('LFT', 'Looking For Team'),
        ('LFP', 'Looking For Players'),
    ]

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    title = models.CharField(
        max_length=200
    )

    content = models.TextField()

    category = models.CharField(
        max_length=10,
        choices=CATEGORY_CHOICES
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return self.title


class AnnouncementReport(models.Model):

    announcement = models.ForeignKey(
        Announcement,
        on_delete=models.CASCADE,
        related_name='reports'
    )

    reported_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    reason = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return f"Report for {self.announcement.title}"