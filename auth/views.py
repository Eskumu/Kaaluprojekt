from django.conf import settings
from django.contrib.auth import views as django_auth_views
from django.shortcuts import redirect

from auth.forms import LoginForm

def login(request, **kwargs):

    if not request.user.is_anonymous():
        return redirect(settings.LOGIN_REDIRECT_URL)

    kwargs.update({
        'template_name': 'auth/login.html',
        'authentication_form': LoginForm,
    })

    return django_auth_views.login(request, **kwargs)