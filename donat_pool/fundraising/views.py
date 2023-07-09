from rest_framework import viewsets
from .models import Fundraising
from .serializers import FundraisingSerializer

class FundraisingViewSet(viewsets.ModelViewSet):
    queryset = Fundraising.objects.all()
    serializer_class = FundraisingSerializer
