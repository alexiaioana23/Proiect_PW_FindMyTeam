from django.db import models
from django.contrib.auth.models import User


class Team(models.Model):

    name = models.CharField(
        max_length=100,
        unique=True
    )

    description = models.TextField()

    leader = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='led_teams'
    )

    members = models.ManyToManyField(
        User,
        related_name='teams'
    )

    max_members = models.IntegerField(
        default=5
    )

    def member_count(self):

        return self.members.count()

    def is_full(self):

        return self.member_count() >= self.max_members

    def __str__(self):

        return self.name