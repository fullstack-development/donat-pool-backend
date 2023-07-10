from rest_framework import viewsets
from .models import SiteSettings, Feedback
from .serializers import SiteSettingsSerializer, FeedbackSerializer

class SiteSettingsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SiteSettings.objects.all()
    serializer_class = SiteSettingsSerializer

class FeedbackViewSet(
    viewsets.mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = FeedbackSerializer