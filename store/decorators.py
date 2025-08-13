# store/decorators.py

from django.http import HttpResponse
from django.shortcuts import redirect

def admin_only(view_func):
    def wrapper_function(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_staff:
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponse('You are not authorized to view this page.')
    return wrapper_function