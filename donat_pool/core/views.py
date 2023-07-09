from rest_framework import viewsets
from .models import SiteSettings
from .serializers import SiteSettingsSerializer

class SiteSettingsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SiteSettings.objects.all()
    serializer_class = SiteSettingsSerializer
