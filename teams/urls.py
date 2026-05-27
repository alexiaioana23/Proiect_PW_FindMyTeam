from django.urls import path
from .views import (
    create_team,
    team_list,
    team_detail,
    join_team,
    leave_team
)

urlpatterns = [

    path('', team_list, name='team_list'),

    path('create/', create_team, name='create_team'),

    path('<int:team_id>/', team_detail, name='team_detail'),

    path('<int:team_id>/join/', join_team, name='join_team'),

    path('<int:team_id>/leave/', leave_team, name='leave_team'),

]