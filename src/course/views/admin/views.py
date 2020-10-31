import json

from django.contrib.auth.models import AnonymousUser
from django.views import View
from django.http import JsonResponse
from django.db import IntegrityError

from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated

from course.models import Course
from course.serializers import CourseSerializer


class AdminCourseView(View):
    def _searializer(self, course: Course):
        return {
            'id': course.id,
            'course_title': course.course_title,
            'created_by': course.created_by_id,
        }

    def post(self, request):
        if isinstance(request.user, AnonymousUser):
            return JsonResponse({'message': 'user need to login'}, status=400)
        body = json.loads(request.body.decode('utf-8'))
        print(request.user)
        try:
            course = Course(
                course_title=body.get('course_title'),
                course_code=body.get('course_code'),
                created_by=request.user
            )
            course.save()
            return JsonResponse({'massage': 'course created'}, status=201)
        except IntegrityError as e:
            print(e)
            return JsonResponse({'massage': f'cannot create course. reason : {e}'}, status=400)

    def get(self, request):
        if isinstance(request.user, AnonymousUser):
            return JsonResponse({'message': 'user need to login'}, status=400)
        return JsonResponse(data=[self._searializer(course=course) for course in Course.objects.all()], safe=False,
                            status=200)


class AdminDRFCourseView(ListCreateAPIView):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    permission_classes = [IsAuthenticated, ]
