from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserRegisterSerializer
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class UserRegister(APIView):

    def post(self, request):
        serz_data = UserRegisterSerializer(data=request.POST)
        if serz_data.is_valid():
            serz_data.create(serz_data.validated_data)
            return Response(serz_data.data, status=status.HTTP_201_CREATED)
        return Response(serz_data.errors)

    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def create_auth_token(sender, instance=None, created=False, **kwargs):
        if created:
            Token.objects.create(user=instance)
