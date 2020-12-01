import json

from django.views import View
from django.http import JsonResponse
from django.conf import settings
from django.contrib.auth.models import Group

from rest_framework.generics import (
    ListAPIView,
    ListCreateAPIView,
    UpdateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .serializers import UserSerializer

import jwt

from user.models import User


class LoginView(View):
    @staticmethod
    def _serializer(user: User):
        return {
            'id': user.id,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'groups': [group.name for group in user.groups.all()]
        }

    def post(self, request):
        body = json.loads(request.body.decode('utf-8'))
        try:
            user = User.objects.get(username=body.get('username'))
            if not user.check_password(raw_password=body.get('password')):
                return JsonResponse({'message': 'invalid password'}, status=400)
            user_data = self._serializer(user=user)
            token = jwt.encode(payload=user_data,
                               key=settings.SECRET_KEY, algorithm='HS256')
            return JsonResponse({'access_token': token.decode('utf-8')}, status=200)
        except User.DoesNotExist:
            return JsonResponse({'massage': 'can not find user'}, status=404)


class UserListView(ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAdminUser, ]


class ProfileListView(ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        return User.objects.filter(username=self.request.user.username)


class ProfileUpdateAPIView(UpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, ]
    lookup_field = 'pk'

    def get_queryset(self):
        return User.objects.filter(username=self.request.user.username)


class UserCreateListAPIView(ListCreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        body = request.data
        user = User(
            first_name=body.get('first_name'),
            last_name=body.get('last_name'),
            username=body.get('username'),
            email=body.get('email'),
            password=body.get('password'),
            category=body.get('category'),
            status=body.get('status'),
        )
        user.set_password(user.password)
        user.save()
        if body['category'] == 'teacher':
            groups = Group.objects.get(name='Teacher')
            groups.user_set.add(user)
            groups.save()
        else:
            groups = Group.objects.get(name='Student')
            groups.user_set.add(user)
            groups.save()
        return Response(data=self.get_serializer(user).data, status=status.HTTP_200_OK)


class UserGetUpdateRetrieveDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.filter()
    permission_classes = [IsAdminUser, ]
    lookup_field = 'pk'

    def destroy(self, request, *args, **kwargs):
        obj: User = self.get_object()
        obj.is_active = False
        obj.status = 'inactive'
        obj.save()
        return Response(data=self.get_serializer(obj).data, status=status.HTTP_200_OK)
