from rest_framework import serializers
from publishers.models import Publisher


class PublisherSerializer(serializers.ModelSerializer):
    '''
    Serializer for Publisher model to expose id, name and description fields.
    '''
    class Meta:
        model = Publisher
        fields = ['id', 'name', 'description']
