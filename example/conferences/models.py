import random

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from cloneable_model.models import CloneableModelMixin


class Conference(CloneableModelMixin, models.Model):
    CLONE_SETTINGS = {
        'attendee_set': {},
        'module_set': {
            'moduleattendee_set': {}
        }
    }

    client = models.ForeignKey('clients.Client')
    attendees = models.ManyToManyField(
        User,
        through='ConferenceAttendee',
        related_name='conferences'
    )
    settings = models.ManyToManyField('Settings', blank=True)
    title = models.CharField(max_length=255)
    code = models.CharField(max_length=6, unique=True)
    created = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = 'Conference'
        verbose_name_plural = 'Conferences'

    def save(self, *args, **kwargs):
        if not self.pk:
            self.created = timezone.now()
            self.code = random.randint(100000, 999999)
        super().save(*args, **kwargs)

    def __str__(self):
        return '{title} {id}'.format(title=self.title, id=self.id)


class ConferenceAttendee(models.Model):
    conference = models.ForeignKey(
        Conference
    )
    user = models.ForeignKey(User)

    def __str__(self):
        return '{user} {id}'.format(
            user=self.user,
            id=self.id
        )


class Settings(models.Model):
    is_active = models.BooleanField(default=True)
    is_private = models.BooleanField(default=False)

    def __str__(self):
        return '{id} {is_active} {is_private}'.format(
            id=self.pk,
            is_active=self.is_active,
            is_private=self.is_private
        )


class Uroboros(CloneableModelMixin, models.Model):
    title = models.CharField(max_length=255)
    uroboros = models.ForeignKey(
        'self',
        blank=True,
        null=True,
        related_name='children'
    )

    def __str__(self):
        return '{title} {id}'.format(title=self.title, id=self.id)
