from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ''' Custom user model extending AbstractUser.
            Adds role-based functionality and subscription relationships.
            :role: Defines the user's role within the application.
            :subscribed_to_publisher: Many-to-many relationship to publishers
                the user is subscribed to.
            :subscribed_to_journalist: Many-to-many relationship to
                journalists the user is subscribed to.
    '''
    ROLE_CHOICES = (
        ('reader', 'Reader'),
        ("journalist", "Journalist"),
        ("editor", "Editor"),
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
    )

    subscribed_to_publisher = models.ManyToManyField(
        'publishers.Publisher',
        blank=True,
        related_name='subscribed_readers',
    )

    subscribed_to_journalist = models.ManyToManyField(
        'self',
        blank=True,
        symmetrical=False,
        related_name='journalist_subscribers',
    )
