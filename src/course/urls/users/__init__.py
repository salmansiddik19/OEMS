from django.urls import path
from course.views import (
    AllUserCourseListView,
    ParticularUserCourseListView,
    CourseCreateView,
    CourseUpdateRetrieveDestroyView,
)

urlpatterns = [
    path('all-list', AllUserCourseListView.as_view(),
         name='course-all-user-list-view'),
    path('particular-list', ParticularUserCourseListView.as_view(),
         name='course-particular-user-list-view'),
    path('create-list', CourseCreateView.as_view(),
         name='course-create-list-view'),
    path('course-list/<int:pk>', CourseUpdateRetrieveDestroyView.as_view(),
         name='course-update-retrieve-destroy-view'),
]
