from rest_framework import viewsets
from .models import Fundraising
from donat_pool.core.models import Category
from .serializers import FundraisingSerializer
from django_filters import rest_framework as filters

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
