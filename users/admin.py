from django.contrib import admin
from django.utils.html import format_html

from .models import Profile, Report

from django.utils.html import format_html

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user']


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):

    list_display = [
        'reporter',
        'reported_user',
        'reason',
        'suspend_button'
    ]

    def suspend_button(self, obj):

        return format_html(
            '<a class="button" href="/users/suspend/{}/">Suspend User</a>',
            obj.reported_user.id
        )

    suspend_button.short_description = 'Actions'

