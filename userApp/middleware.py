import datetime
from django.shortcuts import redirect
from contextlib import redirect_stderr
from django.conf import settings
from django.contrib.auth import logout
from django.utils.timezone import now, make_aware
from django.urls import reverse

# Log users out to promote safety
class AutoLogoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # looks for logged in users
        if request.user.is_authenticated:
            current_time = now()

            last_activity = request.session.get('last_activity')

            # if the last activity is more than SESSION_COOKIE_AGE, logs them out
            if last_activity:
                last_activity_time = make_aware(datetime.datetime.fromtimestamp(last_activity))
                elapsed_time = current_time - last_activity_time
                if elapsed_time.total_seconds() > settings.SESSION_COOKIE_AGE:
                    logout(request)
                    return redirect('login')

            # update last activity timestamp in the session
            request.session['last_activity'] = current_time.timestamp()

        response = self.get_response(request)
        return response

class CheckActiveMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if user is authenticated and inactive
        print(f"User authenticated: {request.user.is_authenticated}, Activated: {getattr(request.user, 'activated', None)}")
        if request.user.is_authenticated and not request.user.activated:
            # Prevent infinite redirect loop by checking for the 'deactivated' path
            if request.path != reverse('deactivated') and request.path != reverse('logout'):
                return redirect('deactivated')

        # Continue with request processing if user is active
        return self.get_response(request)
