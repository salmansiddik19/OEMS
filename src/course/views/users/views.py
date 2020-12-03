from course.models import Course
from course.serializers import CourseSerializer
from user.models import User
from user.permissions import IsCourseAdmin

from rest_framework.generics import (
    ListAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView
)
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status


class AllUserCourseListView(ListAPIView):
    serializer_class = CourseSerializer
    queryset = Course.objects.filter()
    permission_classes = [IsAuthenticated, ]


class ParticularUserCourseListView(ListAPIView):
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, IsCourseAdmin]

    def get_queryset(self):
        user = self.request.user
        return Course.objects.filter(created_by=user)


class CourseCreateView(ListCreateAPIView):
    serializer_class = CourseSerializer
    queryset = Course.objects.filter()
    permission_classes = [IsAuthenticated, IsCourseAdmin]


class CourseUpdateRetrieveDestroyView(RetrieveUpdateDestroyAPIView):
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, IsCourseAdmin]
    lookup_field = 'pk'

    def get_queryset(self):
        user = self.request.user
        return Course.objects.filter(created_by=user)

    def destroy(self, request, *args, **kwargs):
        obj: Course = self.get_object()
        obj.is_active = False
        obj.status = 'inactive'
        obj.save()
        return Response(data=self.get_serializer(obj).data, status=status.HTTP_200_OK)
