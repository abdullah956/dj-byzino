from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages

class AdminOnlyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_staff:
            return self.get_response(request)
        if (request.path.startswith('/admin/') or request.path.startswith('/dashboard/')) and not request.user.is_staff:
            messages.error(request, "You do not have permission to access this route.")
            return redirect(reverse('login'))
        return self.get_response(request)