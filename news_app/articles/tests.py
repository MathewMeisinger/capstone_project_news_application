from django.test import TestCase
from unittest.mock import patch
from articles.models import Article
from subscriptions.models import JournalistSubscription
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.test import APITestCase

User = get_user_model()


def get_jwt_for_user(user):
    '''
    Generate JWT tokens for a given user.
    '''
    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token)


class BaseAPITestCase(APITestCase):
    '''
    Docstring for BaseAPITestCase
    '''
    def create_user(self, username, role):
        return User.objects.create_user(
            username=username,
            password='testpassword123',
            role=role,
            )

    def authenticate(self, user):
        token = get_jwt_for_user(user)
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {token}'
            )


class ArticleSignalTests(TestCase):

    @patch("articles.signals.post_to_x")
    @patch("articles.signals.send_mail")
    def test_signal_fires_on_approval(
        self,
        mock_send_mail,
        mock_post_to_x
    ):
        reader = User.objects.create_user(
            username="reader",
            password="pass",
            role="reader"
        )
        journalist = User.objects.create_user(
            username="journalist",
            password="pass",
            role="journalist"
        )

        JournalistSubscription.objects.create(
            reader=reader,
            journalist=journalist
        )

        article = Article.objects.create(
            title="Draft",
            content="...",
            author=journalist,
            approved=False
        )

        # Trigger approval
        article.approved = True
        article.save()

        mock_send_mail.assert_called_once()
        mock_post_to_x.assert_called_once()


class ArticleAccessTests(BaseAPITestCase):
    '''
    Test article access permissions for different user roles.
    '''
    def setUp(self):
        self.reader = self.create_user('reader', 'reader')
        self.journalist = self.create_user('journalist', 'journalist')
        self.editor = self.create_user('editor', 'editor')

    def test_reader_can__view_articles(self):
        self.authenticate(self.reader)
        response = self.client.get('/api/articles/')
        self.assertEqual(response.status_code, 200)

    def test_reader_cannot_create_article(self):
        self.authenticate(self.reader)
        data = {
            'title': 'Unauthorized Article',
            'content': 'This should not be created.',
            'publisher': 1
        }
        response = self.client.post('/api/articles/', data)
        self.assertEqual(response.status_code, 403)


class JournalistArticleTests(BaseAPITestCase):
    '''
    Test journalist article creation.
    '''
    def setUp(self):
        self.journalist = self.create_user('journalist', 'journalist')
        self.authenticate(self.journalist)

    def test_journalist_can_create_article(self):
        response = self.client.post('/api/articles/', {
            'title': 'New Article',
            'content': 'Content of the new article.',
        })
        self.assertEqual(response.status_code, 201)
        self.assertFalse(Article.objects.first().approved)


class EditorArticleTests(BaseAPITestCase):
    '''
    Test editor article approval and deleting.
    '''
    def setUp(self):
        self.editor = self.create_user('editor', 'editor')
        self.journalist = self.create_user('journalist', 'journalist')
        self.article = Article.objects.create(
            title='Pending Article',
            content='Content awaiting approval.',
            author=self.journalist,
            approved=False
        )

    def test_editor_can_approve_article(self):
        self.authenticate(self.editor)
        self.article.approved = True
        self.article.save()
        self.article.refresh_from_db()
        self.assertTrue(self.article.approved)

    def test_editor_can_delete_article(self):
        self.authenticate(self.editor)
        response = self.client.delete(
            f'/api/articles/{self.article.id}/'
        )
        self.assertEqual(response.status_code, 204)


class SubscribedArticleTests(BaseAPITestCase):

    def setUp(self):
        self.reader = self.create_user("reader", "reader")
        self.journalist1 = self.create_user("j1", "journalist")
        self.journalist2 = self.create_user("j2", "journalist")

        self.article1 = Article.objects.create(
            title="A1",
            content="...",
            author=self.journalist1,
            approved=True,
        )

        self.article2 = Article.objects.create(
            title="A2",
            content="...",
            author=self.journalist2,
            approved=True,
        )

        JournalistSubscription.objects.create(
            reader=self.reader,
            journalist=self.journalist1,
        )

        self.authenticate(self.reader)

    def test_reader_gets_only_subscribed_articles(self):
        response = self.client.get("/api/articles/subscribed/")
        titles = [a["title"] for a in response.data]

        self.assertIn("A1", titles)
        self.assertNotIn("A2", titles)
