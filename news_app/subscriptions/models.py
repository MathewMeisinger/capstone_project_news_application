from django.db import models
from django.conf import settings
from newsletters.models import Newsletter

User = settings.AUTH_USER_MODEL


class JournalistSubscription(models.Model):
    '''A model representing a subscription where a reader subscribes to a
        journalist.

        :reader: ForeignKey to the User model representing the reader.
        :journalist: ForeignKey to the User model representing the journalist.
        :created_at: DateTimeField recording when the subscription was created.
    '''
    reader = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='journalist_subscriptions'
    )
    journalist = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscribed_readers'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('reader', 'journalist')

    def __str__(self):
        return f'{self.reader} subscribed to {self.journalist}'


class NewsletterSubscription(models.Model):
    ''' A model representing a subscription where a reader subscribes to a
        newsletter.

        :reader: ForeignKey to the User model representing the reader.
        :newsletter: ForeignKey to the Newsletter model.
        :created_at: DateTimeField recording when the subscription was created.
    '''
    reader = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='newsletter_subscriptions'
    )
    newsletter = models.ForeignKey(
        Newsletter,
        on_delete=models.CASCADE,
        related_name='subscribed_readers'

    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('reader', 'newsletter')

    def __str__(self):
        return f'{self.reader} subscribed to {self.newsletter}'
