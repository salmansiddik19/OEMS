from django.urls import path

from user.views import (
    LoginView,
    UserListView,
    UserCreateListAPIView,
    ProfileListView,
    ProfileUpdateAPIView,
    UserGetUpdateRetrieveDestroyAPIView
)

urlpatterns = [
    path('login', LoginView.as_view(), name='user-login-view'),
    path('list', UserListView.as_view(), name='user-list-view'),
    path('list/<int:pk>', UserGetUpdateRetrieveDestroyAPIView.as_view(),
         name='user-list-update-delete-view'),
    path('create-list', UserCreateListAPIView.as_view(),
         name='user-create-list-view'),
    path('profile', ProfileListView.as_view(), name='user-profile-view'),
    path('profile/<int:pk>', ProfileUpdateAPIView.as_view(),
         name='user-profile-update-view'),
]
