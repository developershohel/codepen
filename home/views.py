import json
from requests import get
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.contrib.sites.shortcuts import get_current_site
from codepen.functions import delete_cookie, get_client_ip, get_client_details_by_ip, home_url, user_auth, \
    codepen_platform, pen_platform
from codepen.cp_user import get_user, trending_pens
from profiles.models import Profile
from pen.models import Pen
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail


def index(request):
    site_url = get_current_site(request)
    ip = get_client_details_by_ip('103.239.255.44')

    context = {
        'site_url': site_url,
        'codepen_platform': pen_platform,
    }
    if ip:
        context['country'] = ip['countryCode']
    if request.method == "GET":
        if user_auth(request):
            login_user = get_user(request.user.id)
            context['login_user'] = login_user
            pen = Pen.objects.all()
            context['pens'] = pen
            context['username'] = login_user.get().username
            return render(request, 'main/home/index.html', context)
        else:
            login_user = get_user('guest_user')
            context['login_user'] = login_user
            trending_pen = trending_pens()[:6]
            context['trending_pens'] = trending_pen
            return render(request, 'main/home/index.html', context)
    else:
        return HttpResponseRedirect(home_url())


def work_with_cookies(request):
    auth_user = request.user.is_authenticated
    site_url = get_current_site(request)
    context = {
        'site_url': site_url,
        'auth_user': auth_user
    }
    templates = render(request, 'main/home/index.html', context)
    return templates


def check_sent_email(request):
    sent_main = send_mail('Test', 'Test django message', 'sohelhossenbijoy@gmail.com', ['sohelhossenbijoy@gmail.com'])
    if sent_main:
        print('ok')
        return HttpResponseRedirect(home_url())
    else:
        return HttpResponseRedirect(home_url())

