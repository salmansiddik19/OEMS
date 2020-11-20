from course.models import Course
from course.serializers import CourseSerializer

from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated


class AdminDRFCourseView(ListCreateAPIView):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    permission_classes = [IsAuthenticated, ]
