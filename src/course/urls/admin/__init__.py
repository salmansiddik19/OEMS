from django.urls import path
from course.views import AdminDRFCourseView, AdminCourseGetUpdateRetrieveView

urlpatterns = [
    path('create-list', AdminDRFCourseView.as_view(),
         name='course-admin-create-list'),
    path('list/<int:pk>', AdminCourseGetUpdateRetrieveView.as_view(),
         name='course-update-retrieve-delete-list'),
]
