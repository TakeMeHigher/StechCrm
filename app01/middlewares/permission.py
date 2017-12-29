import re

from django.shortcuts import redirect,HttpResponse
from django.conf import settings

class MiddlewareMixin(object):
    def __init__(self, get_response=None):
        self.get_response = get_response
        super(MiddlewareMixin, self).__init__()

    def __call__(self, request):
        response = None
        if hasattr(self, 'process_request'):
            response = self.process_request(request)
        if not response:
            response = self.get_response(request)
        if hasattr(self, 'process_response'):
            response = self.process_response(request, response)
        return response



class PerMiddleware(MiddlewareMixin):
    def process_request(self,request):
        current_url=request.path_info

        for url in settings.VALID_URL:
            if re.match(url,current_url):
                return None

        user=request.session.get('user')
        stu=request.session.get('stu')
        if user or stu:
            return None
        else:
            return redirect('/login/')

