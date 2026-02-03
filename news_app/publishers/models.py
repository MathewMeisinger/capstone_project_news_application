from django.db import models
from django.conf import settings


User = settings.AUTH_USER_MODEL


class Publisher(models.Model):
    '''
    Model representing a news publisher.
    fields:
    - name: The name of the publisher.
    - editors: ManyToManyField to the User model representing the editors of
                the publisher.
    - journalists: ManyToManyField to the User model representing the
                    journalists of the publisher.
    '''
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)

    editors = models.ManyToManyField(
        User,
        related_name='publisher_as_editor',
        limit_choices_to={'role': 'editor'},
        blank=True,
    )
    journalists = models.ManyToManyField(
        User,
        related_name='publisher_as_journalist',
        limit_choices_to={'role': 'journalist'},
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
