from rest_framework import serializers
from articles.models import Article
from users.api.serializers import UserSerializer
from publishers.api.serializers import PublisherSerializer


class ArticleSerializer(serializers.ModelSerializer):
    '''
    Serializer for Article model to expose id, title, content, author,
    publisher, approved and created_at fields.
    '''
    author = UserSerializer(read_only=True)
    publisher = PublisherSerializer(read_only=True)

    class Meta:
        model = Article
        fields = (
            'id', 'title', 'content', 'author', 'publisher', 'approved',
            'created_at'
        )
        read_only_fields = ('approved',)


class ArticleWriteSerializer(serializers.ModelSerializer):
    '''
    Serializer for creating and updating Article instances.
    '''
    class Meta:
        model = Article
        fields = ('title', 'content', 'publisher')
