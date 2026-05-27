from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404
from messages_app.models import Conversation, Message
from .models import Announcement, AnnouncementReport

from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)

from django.contrib.auth.decorators import (
    login_required,
    user_passes_test
)

from django.contrib.auth.models import User

from .models import (
    Announcement,
    AnnouncementReport
)

from .forms import AnnouncementForm

from messages_app.models import (
    Conversation,
    Message
)


@login_required
def announcement_list(request):

    announcements = Announcement.objects.all().order_by(
        '-created_at'
    )

    return render(
        request,
        'announcement_list.html',
        {
            'announcements': announcements
        }
    )


@login_required
def create_announcement(request):

    if request.method == 'POST':

        form = AnnouncementForm(request.POST)

        if form.is_valid():

            announcement = form.save(
                commit=False
            )

            announcement.author = request.user

            announcement.save()

            return redirect(
                'announcement_list'
            )

    else:

        form = AnnouncementForm()

    return render(
        request,
        'create_announcement.html',
        {
            'form': form
        }
    )


@login_required
def announcement_detail(
    request,
    announcement_id
):

    announcement = get_object_or_404(
        Announcement,
        id=announcement_id
    )

    return render(
        request,
        'announcement_detail.html',
        {
            'announcement': announcement
        }
    )


@login_required
def report_announcement(
    request,
    announcement_id
):

    announcement = get_object_or_404(
        Announcement,
        id=announcement_id
    )

    if request.method == 'POST':

        reason = request.POST.get(
            'reason'
        )

        AnnouncementReport.objects.create(
            announcement=announcement,
            reported_by=request.user,
            reason=reason
        )

        return redirect(
            'announcement_list'
        )

    return render(
        request,
        'report_announcement.html',
        {
            'announcement': announcement
        }
    )


def is_admin(user):

    return user.is_superuser


@login_required
@user_passes_test(is_admin)
def admin_reports(request):

    reports = AnnouncementReport.objects.all().order_by(
        '-created_at'
    )

    return render(
        request,
        'admin_reports.html',
        {
            'reports': reports
        }
    )


@login_required
@user_passes_test(is_admin)
def delete_announcement(
    request,
    announcement_id
):

    announcement = get_object_or_404(
        Announcement,
        id=announcement_id
    )

    author = announcement.author

    if request.method == 'POST':

        conversation = Conversation.objects.create()

        conversation.participants.add(
            request.user,
            author
        )

        Message.objects.create(
            conversation=conversation,
            sender=request.user,
            content=
                f'Your announcement "{announcement.title}" '
                f'was removed by administrators.'
        )

        announcement.delete()

        return redirect(
            'admin_reports'
        )

    return render(
        request,
        'delete_announcement.html',
        {
            'announcement': announcement
        }
    )

@login_required
def report_announcement(request, announcement_id):

    announcement = get_object_or_404(
        Announcement,
        id=announcement_id
    )

    if request.method == 'POST':

        reason = request.POST.get('reason')

        AnnouncementReport.objects.create(
            announcement=announcement,
            reported_by=request.user,
            reason=reason
        )

        return redirect('announcement_list')

    return render(request, 'report_announcement.html', {
        'announcement': announcement
    })


@staff_member_required
def reported_announcements(request):

    reports = AnnouncementReport.objects.all().order_by('-created_at')

    return render(request, 'reported_announcements.html', {
        'reports': reports
    })


@staff_member_required
def delete_reported_announcement(request, report_id):

    report = get_object_or_404(
        AnnouncementReport,
        id=report_id
    )

    announcement = report.announcement
    author = announcement.author

    conversation = Conversation.objects.create()

    conversation.participants.add(
        request.user,
        author
    )

    Message.objects.create(
        conversation=conversation,
        sender=request.user,
        content=
            f'Anunțul "{announcement.title}" '
            f'a fost șters de administrator.'
    )

    announcement.delete()

    return redirect('reported_announcements')