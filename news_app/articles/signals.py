from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Article
from subscriptions.models import (
    JournalistSubscription,
    NewsletterSubscription
)
import requests
from articles.services.x_publisher import post_to_x


@receiver(pre_save, sender=Article)
def article_pre_save(sender, instance, **kwargs):
    '''
    Store the previous approved status before saving.
    '''
    if not instance.pk:
        instance.previous_approved = False
        return

    try:
        previous = Article.objects.get(pk=instance.pk)
        instance.previous_approved = previous.approved
    except Article.DoesNotExist:
        instance.previous_approved = False


@receiver(post_save, sender=Article)
def notify_subscribers_on_approval(sender, instance, created, **kwargs):
    '''
    Send notification emails to subscribers only when an article 
    goes from unapproved to approved status for the first time.
    '''
    # only proceed if the article is being updated, not created
    if created:
        return

    if not instance.approved:
        return

    if getattr(instance, 'previous_approved', True):
        return

    # fetch journalist and newsletter subscribers
    journalist_subscribers = JournalistSubscription.objects.filter(
        journalist=instance.author
    ).select_related('reader')

    newsletter_subscribers = NewsletterSubscription.objects.filter(
        newsletter__articles=instance
    ).select_related('reader')

    # compile unique recipient emails
    recipients = set()

    for sub in journalist_subscribers:
        recipients.add(sub.reader.email)

    for sub in newsletter_subscribers:
        recipients.add(sub.reader.email)

    # Remove any 'None' emails if present
    recipients.discard(None)

    if not recipients:
        return

    # send notification emails
    subject = f'New Article Published: {instance.title}'
    message = (
        f"{instance.title}\n\n"
        f"By {instance.author.username}\n\n"
        f'{instance.content[:200]}...\n\n'
        f'Read more at: http://example.com/articles/{instance.pk}'
    )

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=list(recipients),
        fail_silently=False,
    )

    # Post to X (Twitter)
    post_to_x(instance)
