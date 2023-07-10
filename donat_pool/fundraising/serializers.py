from rest_framework import serializers
from .models import (
    Author, 
    Fundraising, 
    CompletedFundraising,
    )

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = [
            'pkh',
            ]

class FundraisingSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()

    class Meta:
        model = Fundraising
        fields = [
            'path',
            'author',
            'category',
            'description',
            'image',
            'tags'
            ]
    
    def create(self, validated_data):
        author_pk = validated_data.get('author').get('pkh')
        author = Author.objects.get_or_create(pkh=author_pk)
        fundraising = self.Meta.model.objects.create(
            path = validated_data['path'],
            author = author[0],
            category = validated_data['category'],
            description = validated_data['description'],
            image = validated_data['image'],
        )
        fundraising.tags.set(validated_data['tags'])
        return fundraising
    
class CompletedFundraisingSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompletedFundraising
        fields = [
            'path',
            'author',
            'title',
            'targetAmount',
            'raisedAmount',
            'completedAt',
            ]
