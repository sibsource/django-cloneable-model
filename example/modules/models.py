import uuid

from django.db import models
from django.utils import timezone

from cloneable_model.models import CloneableModelMixin
from mptt.models import MPTTModel, TreeForeignKey

from conferences.models import Conference


class Module(models.Model):
    title = models.CharField(max_length=255)
    conference = models.ForeignKey(Conference)
    created = models.DateTimeField(default=timezone.now, editable=False)

    def __str__(self):
        return '{title} {id}'.format(id=self.id, title=self.title)


class ScheduleModule(Module):
    def __str__(self):
        return '{title} {id} {conference_id}'.format(
            title=self.title,
            id=self.id,
            conference_id=self.conference_id
        )


class Event(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    name = models.CharField(max_length=255)
    schedule = models.ForeignKey(ScheduleModule, related_name='events')
    event = models.ForeignKey(
        'self',
        blank=True,
        null=True,
        related_name='parent'
    )
    owners = models.ManyToManyField(
        'conferences.ConferenceAttendee',
        blank=True
    )
    attendees = models.ManyToManyField(
        'conferences.ConferenceAttendee',
        through='EventAttendee',
        related_name='events',
        blank=True
    )
    documents = models.ManyToManyField(
        'Document',
        through='EventDocument',
        blank=True
    )
    presenters = models.ManyToManyField(
        'Presenter',
        through='EventPresenter',
        blank=True
    )
    created = models.DateTimeField(default=timezone.now, editable=False)

    def __str__(self):
        return '{name} {id}'.format(
            name=self.name,
            id=self.id
        )


class EventAttendee(models.Model):
    event = models.ForeignKey(Event)
    attendee = models.ForeignKey('conferences.ConferenceAttendee')


class EventDocument(models.Model):
    event = models.ForeignKey(Event)
    document = models.ForeignKey('Document')


class EventPresenter(models.Model):
    event = models.ForeignKey(Event)
    presenter = models.ForeignKey('Presenter')

    def __str__(self):
        return '{event} {id}'.format(event=self.event.name, id=self.id)

class DocumentsModule(Module):
    pass


class Category(CloneableModelMixin, MPTTModel, models.Model):
    CLONE_SETTINGS = {}

    module = models.ForeignKey(DocumentsModule)
    parent = TreeForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='children',
        db_index=True
    )
    name = models.CharField(max_length=255)

    class MPTTMeta:
        order_insertion_by = ('name',)

    def __str__(self):
        return '{name} {id}'.format(name=self.name, id=self.id)


class Document(models.Model):
    module = models.ForeignKey(DocumentsModule)
    category = models.ForeignKey(Category)
    name = models.CharField(max_length=255, blank=True)
    file = models.FileField(upload_to='media')
    created = models.DateTimeField(default=timezone.now, editable=False)

    def __str__(self):
        return '{name} {id}'.format(name=self.name, id=self.id)


class PresentersModule(Module):
    pass


class Presenter(models.Model):
    module = models.ForeignKey(PresentersModule)
    name = models.CharField(max_length=255)
    created = models.DateTimeField(default=timezone.now, editable=False)

    def __str__(self):
        return '{name} {id}'.format(name=self.name, id=self.id)
