
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserRegisterSerializer

class UserRegister(APIView):

    def post(self , request):
        serz_data = UserRegisterSerializer(data=request.POST)
        if serz_data.is_valid():
            serz_data.create(serz_data.validated_data)
            return Response(serz_data.data , status=status.HTTP_201_CREATED)
        return Response(serz_data.errors)
