from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)

from django.contrib import messages
from django.db import models

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .models import Profile, Report

from .forms import (
    ProfileForm,
    ReportForm,
    RegisterForm
)

from datetime import timedelta
from django.utils import timezone
from django.contrib.auth import logout

@login_required
def create_profile(request):

    if Profile.objects.filter(user=request.user).exists():

        return redirect('profile')

    if request.method == 'POST':

        form = ProfileForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            profile = form.save(commit=False)

            profile.user = request.user

            profile.save()

            return redirect('profile')

    else:

        form = ProfileForm()

    return render(
        request,
        'create_profile.html',
        {
            'form': form,
            'has_profile': False
        }
    )


@login_required
def edit_profile(request):

    profile = Profile.objects.get(
        user=request.user
    )

    if request.method == 'POST':

        form = ProfileForm(
            request.POST,
            request.FILES,
            instance=profile
        )

        if form.is_valid():

            try:

                form.save()

                messages.success(
                    request,
                    'Rank-ul a fost actualizat.'
                )

                return redirect('profile')

            except:

                messages.error(
                    request,
                    'Eroare la salvare. '
                    'Te rugăm să încerci mai târziu.'
                )

    else:

        form = ProfileForm(
            instance=profile
        )

    return render(
        request,
        'edit_profile.html',
        {
            'form': form,
            'has_profile': True
        }
    )


def register_view(request):

    if request.method == 'POST':

        form = RegisterForm(request.POST)

        if form.is_valid():

            from django.contrib.auth import login

            user = form.save()

            login(
                request,
                user,
                backend='django.contrib.auth.backends.ModelBackend'
            )

            return redirect('create_profile')

    else:

        form = RegisterForm()

    return render(
        request,
        'register.html',
        {
            'form': form
        }
    )


@login_required
def profile_view(request):

    profile = Profile.objects.get(
        user=request.user
    )

    return render(
        request,
        'profile.html',
        {
            'profile': profile,
            'has_profile': True
        }
    )

@login_required
def search_players(request):

    profiles = Profile.objects.all()

    rank = request.GET.get('rank')

    role = request.GET.get('role')

    if rank:

        profiles = profiles.filter(rank=rank)

    if role:

        profiles = profiles.filter(
            models.Q(primary_role=role) |
            models.Q(secondary_role=role)
        )

    no_results = False

    if role and not profiles.exists():

        no_results = True

    return render(request, 'search_players.html', {

        'profiles': profiles,

        'ranks': Profile.RANK_CHOICES,

        'roles': Profile.ROLE_CHOICES,

        'selected_rank': rank,

        'selected_role': role,

        'no_results': no_results
    })


@login_required
def player_detail(request, profile_id):

    profile = Profile.objects.get(
        id=profile_id
    )

    return render(
        request,
        'player_detail.html',
        {
            'profile': profile,
            'has_profile': True
        }
    )


@login_required
def report_player(request, user_id):

    reported_user = get_object_or_404(
        User,
        id=user_id
    )

    if request.method == 'POST':

        reason = request.POST.get('reason')

        Report.objects.create(
            reporter=request.user,
            reported_user=reported_user,
            reason=reason
        )

        return redirect('search_players')

    return render(
        request,
        'report_player.html',
        {
            'reported_user': reported_user,
            'has_profile': True
        }
    )

from django.contrib.admin.views.decorators import (
    staff_member_required
)

from django.contrib.auth.models import User


@staff_member_required
def suspend_user(request, user_id):

    user = get_object_or_404(
        User,
        id=user_id
    )

    profile = user.profile

    already_suspended = not user.is_active

    if request.method == 'POST':

        action = request.POST.get('action')

        if action == 'unsuspend':

            user.is_active = True
            user.save()

            profile.suspended_until = None
            profile.suspension_reason = ''
            profile.save()

            return redirect('/admin/users/report/')

        duration = int(
            request.POST.get('duration')
        )

        reason = request.POST.get(
            'reason'
        )

        suspended_until = (
            timezone.now() +
            timedelta(days=duration)
        )

        user.is_active = False
        user.save()

        profile.suspended_until = suspended_until
        profile.suspension_reason = reason
        profile.save()

        logout(request)

        return redirect('/admin/users/report/')

    return render(
        request,
        'suspend_user.html',
        {
            'suspended_user': user,
            'already_suspended': already_suspended
        }
    )