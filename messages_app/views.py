from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .models import Conversation, Message


@login_required
def inbox(request):

    conversations = Conversation.objects.filter(
        participants=request.user
    ).order_by('-updated_at')

    for conversation in conversations:

        conversation.unread_messages = conversation.messages.filter(
            is_read=False
        ).exclude(
            sender=request.user
        ).count()

    return render(request, 'messages/inbox.html', {
        'conversations': conversations
    })

@login_required
def conversation_detail(request, conversation_id):

    conversation = get_object_or_404(
        Conversation,
        id=conversation_id,
        participants=request.user
    )

    messages = conversation.messages.all()

    messages.filter(
        is_read=False
    ).exclude(
        sender=request.user
    ).update(is_read=True)

    other_user = conversation.participants.exclude(
        id=request.user.id
    ).first()

    if request.method == 'POST':

        content = request.POST.get('content')

        if content:

            Message.objects.create(
                conversation=conversation,
                sender=request.user,
                content=content
            )

            conversation.save()

        return redirect(
            'conversation_detail',
            conversation_id=conversation.id
        )

    return render(request, 'messages/chat.html', {
        'conversation': conversation,
        'messages': messages,
        'other_user': other_user
    })


@login_required
def start_conversation(request, user_id):

    other_user = get_object_or_404(
        User,
        id=user_id
    )

    conversations = Conversation.objects.filter(
        participants=request.user
    ).filter(
        participants=other_user
    )

    if conversations.exists():

        conversation = conversations.first()

    else:

        conversation = Conversation.objects.create()

        conversation.participants.add(
            request.user,
            other_user
        )

    invite = request.GET.get('invite')

    if invite:

        Message.objects.create(
            conversation=conversation,
            sender=request.user,
            content=f'{request.user.username} te-a invitat să joci CS2.'
        )

    return redirect(
        'conversation_detail',
        conversation_id=conversation.id
    )