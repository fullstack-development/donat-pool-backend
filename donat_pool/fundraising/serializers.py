from rest_framework import serializers
from .models import (
    Author, 
    Fundraising, 
    CompletedFundraising,
    )

class FundraisingSerializer(serializers.ModelSerializer):
    author_pkh = serializers.CharField(source="author.pkh") 

    class Meta:
        model = Fundraising
        fields = [
            'path',
            'author_pkh',
            'category',
            'description',
            'image',
            'tags'
            ]
    
    def create(self, validated_data):
        author_pk = validated_data.get('author').get('pkh')
        author, _created = Author.objects.get_or_create(pkh=author_pk)
        if author.untrustworthy:
            err = "Can't create fundraising"
            raise serializers.ValidationError(err)

        fundraising = self.Meta.model.objects.create(
            path = validated_data['path'],
            author = author,
            category = validated_data['category'],
            description = validated_data['description'],
            image = validated_data['image'],
        )
        fundraising.tags.set(validated_data['tags'])
        return fundraising
    
class CompletedFundraisingSerializer(serializers.ModelSerializer):
    author_pkh = serializers.CharField(source="author.pkh", read_only=True) 

    class Meta:
        model = CompletedFundraising
        fields = [
            'path',
            'author_pkh',
            'title',
            'targetAmount',
            'raisedAmount',
            'completedAt',
            ]

    def create(self, validated_data):
        path = validated_data.get('path')
        try:
            fundraising = Fundraising.objects.get(pk=path)
        except Fundraising.DoesNotExist:
            err = "Fundraising doesn't exist"
            raise serializers.ValidationError(err)
        
        closed_fundraising = self.Meta.model.objects.create(
            path = path,
            author = fundraising.author,
            title = validated_data['title'],
            targetAmount = validated_data['targetAmount'],
            raisedAmount = validated_data['raisedAmount'],
        )
        return closed_fundraising
