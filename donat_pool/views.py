from django.middleware.csrf import get_token
from rest_framework.response import Response
from django.http import JsonResponse

def get_csrf(request):
    return JsonResponse({"csrfToken": get_token(request)})

def csrf_failure(request, reason=""):
    return Response({"error": "CSRF verification failed. Request aborted: " + reason} , status=403)