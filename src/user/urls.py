from django.urls import path

from user.views import LoginView, UserListView, UserCreateListAPIView

urlpatterns = [
    path('login', LoginView.as_view(), name='user-login-view'),
    path('list', UserListView.as_view(), name='user-list-view'),
    path('create-list', UserCreateListAPIView.as_view(),
         name='user-create-list-view'),
]
