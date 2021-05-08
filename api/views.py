import jwt
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import UserDataSerializer
from django.contrib.auth.models import User

from vk import settings


# text
def api_gaga(request):
    return JsonResponse('gaga', safe=False)


# доступ до даних користувача через токен
@api_view(['GET'])
def user_data(request):
    token = request.GET.get('token')
    try:
        token_decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        user = User.objects.get(id=token_decoded['id'])
        serializer = UserDataSerializer(user, many=False)
    except :
        return Response({'error': True})
    return Response(serializer.data)


class HelloView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {'first_name': request.user.first_name,
                   'last_name': request.user.last_name,
                   'email': request.user.email}

        return Response(content)
