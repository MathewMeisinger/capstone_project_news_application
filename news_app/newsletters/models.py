from django.db import models
from django.conf import settings


class Newsletter(models.Model):
    ''' Model representing a newsletter.

        -title: The title of the newsletter.
        -description: A brief description of the newsletter.
        -author: The user who created the newsletter.
        -articles: Many-to-many relationship with articles included in the
            newsletter.
        -created_at: Timestamp when the newsletter was created.
    '''
    title = models.CharField(max_length=255)
    description = models.TextField()
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='newsletters',
    )
    articles = models.ManyToManyField('articles.Article')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
