from django.urls import path

from user.views import LoginView, UserListView, TeacherCreateView, StudentCreateView

urlpatterns = [
    path('login', LoginView.as_view(), name='user-login-view'),
    path('list', UserListView.as_view(), name='user-list-view'),
    path('teacher/create-list', TeacherCreateView.as_view(),
         name='teacher-create-list-view'),
    path('student/create-list', StudentCreateView.as_view(),
         name='student-create-list-view'),
]
