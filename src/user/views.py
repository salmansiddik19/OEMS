import json

from django.views import View
from django.http import JsonResponse
from django.conf import settings
from django.db import IntegrityError
from django.contrib.auth.models import Group

from rest_framework.generics import ListAPIView

from .serializers import UserSerializer

import jwt

from user.models import User


class LoginView(View):
    @staticmethod
    def _serializer(user):
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
    queryset = User.objects.filter()


class TeacherCreateView(View):
    @staticmethod
    def _serializer(user):
        return {
            'id': user.id,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'is_teacher': user.is_teacher,
            'groups': [group.name for group in user.groups.all()]
        }

    def post(self, request):
        body = json.loads(request.body.decode('utf-8'))
        try:
            user = User(
                first_name=body.get('first_name'),
                last_name=body.get('last_name'),
                username=body.get('username'),
                email=body.get('email'),
                password=body.get('password'),
                is_teacher=True,
            )
            user.save()
            groups = Group.objects.get(name='Teacher')
            groups.user_set.add(user)
            groups.save()
            return JsonResponse({'data': self._serializer(user)}, status=201)
        except IntegrityError as e:
            print(e)
            return JsonResponse({'massage': f'cannot create course. reason : {e}'}, status=400)


class StudentCreateView(View):
    @staticmethod
    def _serializer(user):
        return {
            'id': user.id,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'is_student': user.is_student,
            'groups': [group.name for group in user.groups.all()]
        }

    def post(self, request):
        body = json.loads(request.body.decode('utf-8'))
        try:
            user = User(
                first_name=body.get('first_name'),
                last_name=body.get('last_name'),
                username=body.get('username'),
                email=body.get('email'),
                password=body.get('password'),
                is_student=True,
            )
            user.save()
            groups = Group.objects.get(name='Student')
            groups.user_set.add(user)
            groups.save()
            return JsonResponse({'data': self._serializer(user)}, status=201)
        except IntegrityError as e:
            print(e)
            return JsonResponse({'massage': f'cannot create course. reason : {e}'}, status=400)
