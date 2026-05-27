from django.urls import path
from .views import (
    profile_view,
    create_profile,
    search_players,
    player_detail,
    report_player,
    edit_profile,
    register_view,
    suspend_user
)

urlpatterns = [

    path('profile/', profile_view, name='profile'),

    path('create-profile/', create_profile, name='create_profile'),

    path('search/', search_players, name='search_players'),

    path('player/<int:profile_id>/', player_detail, name='player_detail'),

    path('report/<int:user_id>/', report_player, name='report_player'),

    path('edit-profile/', edit_profile, name='edit_profile'),

    path('register/', register_view, name='register'),

    path(
        'suspend/<int:user_id>/',
        suspend_user,
        name='suspend_user'
    ),
]