from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.sites.shortcuts import get_current_site
from codepen.functions import delete_cookie, get_client_ip, get_client_details_by_ip, home_url
from profiles.models import Profile
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail


def index(request):
    auth_user = request.user.is_authenticated
    site_url = get_current_site(request)
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
        return render(request, 'main/home/index.html', context)
    else:
        return render(request, 'main/home/index.html', context)


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

