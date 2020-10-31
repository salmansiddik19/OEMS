from django.urls import path
from course.views import AdminCourseView, AdminDRFCourseView

urlpatterns = [
    path('create-list', AdminDRFCourseView.as_view(),
         name='course-admin-create-list'),
]
