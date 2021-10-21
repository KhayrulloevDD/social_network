from datetime import datetime
from social_network.models import User


def last_request_time(func):
    def wrapper(self, request, *args, **kwargs):
        User.objects.filter(id=request.user.id).update(last_request=datetime.now())
        return func(self, request, *args, **kwargs)
    return wrapper


def last_request_time_fbv(func):
    def wrapper(request, *args, **kwargs):
        User.objects.filter(id=request.user.id).update(last_request=datetime.now())
        return func(request, *args, **kwargs)
    return wrapper
