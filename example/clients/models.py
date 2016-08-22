from django.db import models

from cloneable_model.models import CloneableModelMixin


class Client(CloneableModelMixin, models.Model):
    title = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'

    def __str__(self):
        return '{title} {id}'.format(title=self.title, id=self.id)
