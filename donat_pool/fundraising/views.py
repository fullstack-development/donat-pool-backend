from rest_framework import (
    viewsets,
    status,
)
from .models import Fundraising, CompletedFundraising
from .serializers import FundraisingSerializer, CompletedFundraisingSerializer
from django_filters import rest_framework as filters
from rest_framework.response import Response
from django.http import Http404

class FundraisingViewSet(
    viewsets.mixins.ListModelMixin,
    viewsets.mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    queryset = Fundraising.objects.all()
    serializer_class = FundraisingSerializer
    filter_backends = (
        filters.DjangoFilterBackend,
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
        'path', 
        'description',
        ]

class CompletedFundraisingViewSet(
    viewsets.mixins.ListModelMixin,
    viewsets.mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    queryset = CompletedFundraising.objects.all()
    serializer_class = CompletedFundraisingSerializer
    filter_backends = (
        filters.DjangoFilterBackend,
        )
    filterset_fields = [
        'author', 
        ]
    search_fields = [
        'title', 
        ]

    def create(self, request, *args, **kwargs):
        data = request.data
        path = data.get('path', None)
        serializer = self.get_serializer(data=data)
        
        try:
            related_fundraising = Fundraising.objects.get(path=path)
        except Fundraising.DoesNotExist:
                raise Http404
        
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
