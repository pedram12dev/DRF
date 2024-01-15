
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from .serializers import UserRegisterSerializer

class UserRegister(APIView):

    def post(self , request):
        serz_data = UserRegisterSerializer(data=request.POST)
        if serz_data.is_valid():
            User.objects.create_user(
                username = serz_data.validated_data['username'],
                email = serz_data.validated_data['email'],
                password=serz_data.validated_data['password'],
            )
            return Response(serz_data.data)
        return Response(serz_data.errors)
