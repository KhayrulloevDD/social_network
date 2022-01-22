from datetime import datetime
from social_network.models import User


class LastActivityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        User.objects.filter(id=request.user.id).update(last_request=datetime.now())
        return response
