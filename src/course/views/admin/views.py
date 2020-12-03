from course.models import Course
from course.serializers import CourseSerializer

from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework import status


class AdminDRFCourseView(ListCreateAPIView):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    permission_classes = [IsAdminUser, ]


class AdminCourseGetUpdateRetrieveView(RetrieveUpdateDestroyAPIView):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    permission_classes = [IsAdminUser, ]
    lookup_field = 'pk'

    def destroy(self, request, *args, **kwargs):
        obj: Course = self.get_object()
        obj.is_active = False
        obj.status = 'inactive'
        obj.save()
        return Response(data=self.get_serializer(obj).data, status=status.HTTP_200_OK)
