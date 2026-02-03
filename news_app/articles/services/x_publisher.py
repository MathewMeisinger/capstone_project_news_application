import requests
from django.conf import settings
import logging

logger = logging.getLogger('news.twitter')


def post_to_x(article):
    '''
    Publish an article announcement to X (formerly Twitter).
    Logs failure but does not block the approval workflow.
    '''

    if not settings.X_BEARER_TOKEN:
        logger.error(
            'X Post aborted: No bearer token configured.'
            '(article id=%s)', article.pk
        )
        return

    url = f'{settings.X_API_BASE_URL}tweets'

    headers = {
        'authorization': f'Bearer {settings.X_BEARER_TOKEN}',
        'Content-Type': 'application/json',
    }

    payload = {
        'text': (
            f"New Article Published\n\n"
            f"{article.title}\n\n"
            f"By {article.author.username}\n\n"
            f'Read more at: http://example.com/articles/{article.pk}'
        )
    }

    try:
        response = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=5,
        )
        response.raise_for_status()
    except requests.RequestException as exc:
        logger.error(
            "Failed to post article to X "
            "(article_id=%s, status_code=%s, response=%s)",
            article.pk,
            getattr(exc.response, 'status_code', 'N/A'),
            getattr(exc.response, 'text', 'N/A'),
            exc_info=True,  # prints stack trace
        )
