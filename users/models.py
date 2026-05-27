from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):

    RANK_CHOICES = [
        ('Silver', 'Silver'),
        ('Gold Nova', 'Gold Nova'),
        ('Master Guardian', 'Master Guardian'),
        ('Legendary Eagle', 'Legendary Eagle'),
        ('Global Elite', 'Global Elite'),
    ]

    ROLE_CHOICES = [
        ('Entry Fragger', 'Entry Fragger'),
        ('AWPer', 'AWPer'),
        ('Support', 'Support'),
        ('IGL', 'IGL'),
        ('Lurker', 'Lurker'),
    ]

    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True
    )

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )

    is_banned = models.BooleanField(default=False)

    cs2_nickname = models.CharField(max_length=100)

    rank = models.CharField(
        max_length=50,
        choices=RANK_CHOICES
    )

    primary_role = models.CharField(
        max_length=50,
        choices=ROLE_CHOICES
    )

    secondary_role = models.CharField(
        max_length=50,
        choices=ROLE_CHOICES
    )

    suspended_until = models.DateTimeField(
        null=True,
        blank=True
    )

    suspension_reason = models.TextField(
        blank=True
    )

    languages = models.CharField(max_length=100)

    ban_reason = models.TextField(
        blank=True,
        null=True
    )

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):

        return self.user.username


class Report(models.Model):

    REASON_CHOICES = [
        ('Toxic Language', 'Toxic Language'),
        ('Fake Rank', 'Fake Rank'),
        ('Griefing', 'Griefing'),
        ('Spam', 'Spam'),
    ]

    reporter = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reports_made'
    )

    reported_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reports_received'
    )

    reason = models.CharField(
        max_length=50,
        choices=REASON_CHOICES
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):

        return f'{self.reporter} reported {self.reported_user}'