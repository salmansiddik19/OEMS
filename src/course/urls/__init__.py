from django.urls import path, include

urlpatterns = [
    path('admin/', include('course.urls.admin'), name='course-admin-urls'),
]
