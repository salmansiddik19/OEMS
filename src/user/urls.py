from django.urls import path

from user.views import LoginView, UserDRFCreateView

urlpatterns = [
    path('login', LoginView.as_view(), name='user-login-view'),
    path('create-list', UserDRFCreateView.as_view(),
         name='user-create-list-view'),
]
