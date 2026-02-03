from django.db import models
from django.conf import settings


class Article(models.Model):
    '''
    Model representing a news article.
    fields:
    - title: The title of the article.
    - content: The main content/body of the article.
    - author: ForeignKey to the User model representing the author of the
        article.
    - publisher: ForeignKey to the Publisher model representing the publisher
        of the article.
    - approved: Boolean indicating whether the article has been approved for
        publication.
    - created_at: DateTime indicating when the article was created.
    '''
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='articles',
    )
    publisher = models.ForeignKey(
        'publishers.Publisher',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
