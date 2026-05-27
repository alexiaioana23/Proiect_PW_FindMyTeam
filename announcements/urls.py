from django.urls import path

from .views import (
    announcement_list,
    create_announcement,
    announcement_detail,
    report_announcement,
    reported_announcements,
    delete_reported_announcement
)

urlpatterns = [

    path(
        '',
        announcement_list,
        name='announcement_list'
    ),

    path(
        'create/',
        create_announcement,
        name='create_announcement'
    ),

    path(
        '<int:announcement_id>/',
        announcement_detail,
        name='announcement_detail'
    ),

    path(
        '<int:announcement_id>/report/',
        report_announcement,
        name='report_announcement'
    ),

    path(
        'reports/',
        reported_announcements,
        name='reported_announcements'
    ),



    path(
        'report/<int:announcement_id>/',
        report_announcement,
        name='report_announcement'
    ),

    path(
        'reports/',
        reported_announcements,
        name='reported_announcements'
    ),

    path(
        'delete-report/<int:report_id>/',
        delete_reported_announcement,
        name='delete_reported_announcement'
    ),

]

