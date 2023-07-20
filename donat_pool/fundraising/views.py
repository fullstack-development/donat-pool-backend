from rest_framework import (
    viewsets,
    status,
)
from .models import Fundraising, CompletedFundraising
from .serializers import FundraisingSerializer, CompletedFundraisingSerializer
from django_filters import rest_framework as django_filters
from rest_framework.response import Response
from django.http import Http404
from rest_framework import filters

class FundraisingViewSet(
    viewsets.mixins.ListModelMixin,
    viewsets.mixins.CreateModelMixin,
    viewsets.mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    queryset = Fundraising.objects.all()
    serializer_class = FundraisingSerializer
    filter_backends = (
        django_filters.DjangoFilterBackend,
        filters.SearchFilter,
        )
    filterset_fields = [
        'author', 
        'path', 
        'category', 
        'tags', 
        'main', 
        'verified', 
        'promoted',
        ]
    search_fields = [
        'short_description',
        'description',
        ]

class CompletedFundraisingViewSet(
    viewsets.mixins.ListModelMixin,
    viewsets.mixins.CreateModelMixin,
    viewsets.mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    queryset = CompletedFundraising.objects.all()
    serializer_class = CompletedFundraisingSerializer
    filter_backends = (
        django_filters.DjangoFilterBackend,
        filters.SearchFilter,
        )
    filterset_fields = [
        'author', 
        ]
    search_fields = [
        'title', 
        ]
