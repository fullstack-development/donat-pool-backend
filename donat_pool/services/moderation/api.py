from .moderator import is_text_acceptable

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action
from donat_pool.core.models import UnwantedWord

class ModerationView(APIView):
    def post(self, request, action):
        if action == "check-text":
            return self.check_text(request)

    @action(methods=['post'], detail=False)
    def check_text(self, request):
        moderating_text = request.data.get("text", None)
        if moderating_text == None:
            return Response({"error": "can't moderate empty text"})
        
        unwanted_words = UnwantedWord.objects.values_list("word", flat=True)
        is_acceptable = is_text_acceptable(list(unwanted_words), moderating_text)
        return Response({"is_acceptable": is_acceptable})
