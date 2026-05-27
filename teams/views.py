from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Team
from .forms import TeamForm
from django.contrib import messages


@login_required
def create_team(request):

    if request.method == 'POST':

        form = TeamForm(request.POST)

        if form.is_valid():

            team = form.save(commit=False)

            team.leader = request.user

            team.save()

            if request.user not in team.members.all():
                team.members.add(request.user)

            return redirect('team_list')

    else:
        form = TeamForm()

    return render(request, 'create_team.html', {
        'form': form
    })


@login_required
def team_list(request):

    teams = Team.objects.all()

    query = request.GET.get('q')

    if query:
        teams = teams.filter(name__icontains=query)

    return render(request, 'team_list.html', {
        'teams': teams
    })


@login_required
def team_detail(request, team_id):

    team = Team.objects.get(id=team_id)

    return render(request, 'team_detail.html', {
        'team': team
    })


@login_required
def join_team(request, team_id):

    team = get_object_or_404(
        Team,
        id=team_id
    )

    if request.user in team.members.all():

        messages.warning(
            request,
            'Ești deja în echipă.'
        )

        return redirect(
            'team_detail',
            team_id=team.id
        )

    if team.is_full():

        messages.error(
            request,
            f'Momentan, echipa {team.name} nu are locuri disponibile.'
        )

        return redirect(
            'team_detail',
            team_id=team.id
        )

    team.members.add(request.user)

    messages.success(
        request,
        'Te-ai alăturat echipei.'
    )

    return redirect(
        'team_detail',
        team_id=team.id
    )

@login_required
def leave_team(request, team_id):

    team = get_object_or_404(
        Team,
        id=team_id
    )

    if request.user == team.leader:

        messages.error(
            request,
            'Team leader cannot leave the team.'
        )

        return redirect(
            'team_detail',
            team_id=team.id
        )

    if request.user in team.members.all():

        team.members.remove(request.user)

        messages.success(
            request,
            'Ai părăsit echipa.'
        )

    return redirect(
        'team_detail',
        team_id=team.id
    )