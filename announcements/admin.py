from django.contrib import admin

from .models import (
    Announcement,
    AnnouncementReport
)

admin.site.register(Announcement)

admin.site.register(AnnouncementReport)