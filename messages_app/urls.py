from django.urls import path

from .views import (
    inbox,
    conversation_detail,
    start_conversation
)

urlpatterns = [

    path(
        '',
        inbox,
        name='inbox'
    ),

    path(
        'conversation/<int:conversation_id>/',
        conversation_detail,
        name='conversation_detail'
    ),

    path(
        'start/<int:user_id>/',
        start_conversation,
        name='start_conversation'
    ),
]