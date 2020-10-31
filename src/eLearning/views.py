from django.http import JsonResponse
from django.views.generic import View


class TestView(View):
    def get(self, request):
        data = {
            'success': True,
            'massage': 'This is the test view',
            'method': request.method
        }
        return JsonResponse(data=data, status=200)
