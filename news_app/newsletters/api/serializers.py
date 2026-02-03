from rest_framework import serializers
from newsletters.models import Newsletter


class NewsletterSerializer(serializers.ModelSerializer):
    '''
    Serializer for Newsletter model to expose id, title, description and
    created_at.
    '''
    class Meta:
        model = Newsletter
        fields = ['id', 'title', 'description', 'created_at']
