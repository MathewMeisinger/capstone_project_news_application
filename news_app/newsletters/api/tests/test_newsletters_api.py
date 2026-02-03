from newsletters.models import Newsletter
from articles.models import Article
from tests.base import BaseAPITestCase


class NewsletterTests(BaseAPITestCase):

    def setUp(self):
        self.reader = self.create_user("reader", "reader")
        self.journalist = self.create_user("journalist", "journalist")

        self.article = Article.objects.create(
            title="Approved",
            content="...",
            author=self.journalist,
            approved=True,
        )

        self.newsletter = Newsletter.objects.create(
            title="Weekly",
            description="Desc",
            author=self.journalist,
        )

        self.newsletter.articles.add(self.article)
        self.authenticate(self.reader)

    def test_newsletter_articles_visible(self):
        response = self.client.get(
            f"/api/newsletters/{self.newsletter.id}/"
        )
        self.assertEqual(response.status_code, 200)
