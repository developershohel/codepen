import requests
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.contrib.sites.shortcuts import get_current_site
from django.views import View
from django.http import HttpRequest
from codepen.functions import delete_cookie, get_client_ip, get_client_details_by_ip
from profiles.models import Profile
from django.utils.crypto import get_random_string
from django.http import request as req, HttpRequest, cookie
import uuid
from django.contrib.sessions.models import Session

from user.models import User


def index(request):
    site_url = get_current_site(request)
    auth_user = request.user.is_authenticated
    context = {
        'site_url': site_url,
        'auth_user': auth_user,
        'ip': get_client_details_by_ip('103.239.255.44'),
        'line': request.GET.get('line-number')
    }
    if auth_user:
        user = request.user
        user_id = user.id
        profile = Profile.objects.all().filter(user_id=user_id)
        if profile:
            user_image = profile.get().profile_img
            context['user_image'] = user_image
        context['user'] = user
        return render(request, 'user/index.html', context)
    else:
        return render(request, 'home/index.html', context)


def work_with_cookies(request):
    site_url = get_current_site(request)
    auth_user = request.user.is_authenticated
    context = {
        'site_url': site_url,
        'auth_user': auth_user
    }
    templates = render(request, 'home/index.html', context)
    return templates

