from users.models import Profile
from teams.models import Team
from announcements.models import Announcement
from django.shortcuts import render


def home(request):

    total_players = Profile.objects.count()

    total_teams = Team.objects.count()

    total_announcements = Announcement.objects.count()

    return render(request, 'home.html', {

        'total_players': total_players,

        'total_teams': total_teams,

        'total_announcements': total_announcements,

    })