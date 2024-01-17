from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserRegisterSerializer, UserSerializer
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from rest_framework import viewsets
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404


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


class UserViewSet(viewsets.ViewSet):
    queryset = User.objects.all()

    def list(self, request):
        serz_data = UserSerializer(instance=self.queryset, many=True)
        return Response(data=serz_data.data)

    def retrieve(self, request, pk=None):
        user = get_object_or_404(self.queryset, pk=pk)
        serz_data = UserSerializer(instance=user)
        return Response(data=serz_data.data)

    def partial_update(self, request, pk=None):
        user = get_object_or_404(self.queryset, pk=pk)
        if user != request.user:
            return Response({'permission denied': 'you are not the owner'})
        serz_data = UserSerializer(instance=user, data=request.POST, partial=True)
        if serz_data.is_valid():
            serz_data.save()
            return Response(data=serz_data.data)
        return Response(data=serz_data.errors)

    def destroy(self, request, pk=None):
        user = get_object_or_404(self.queryset, pk=pk)
        if user != request.user:
            return Response({'permission denied': 'you are not the owner'})
        user.is_active = False
        user.save()
        return Response({'message': 'user deactivated'})
