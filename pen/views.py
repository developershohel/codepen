import os
import subprocess

from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.models import Permission

from django.apps import apps
from django.urls import reverse

from codepen.functions import pen_platform, home_url
from codepen.settings import BASE_DIR
from .models import Pen, PenData

from codepen.cp_user import get_user, get_profile


def new_pen(request):
    context = {
        'all_pens': Pen.objects.all(),
        'apps': apps.get_app_configs()
    }
    subprocess.Popen("g++ templates/dashboard/test.cpp -o templates/dashboard/test", shell=True,
                     stdout=subprocess.PIPE)
    cwd = os.getcwd()
    os.chdir(f'{BASE_DIR}/templates/dashboard/')
    base_path = f'{BASE_DIR}/templates/dashboard/'
    print(BASE_DIR)
    proc = subprocess.Popen("test.exe", stdin=subprocess.PIPE, shell=True, stdout=subprocess.PIPE)

    # script_response = proc.stdout.read()
    # proc.stdout.close()
    context['script_response'] = proc.stdout.read().decode()
    os.chdir(cwd)
    renter_template = render(request, 'main/pen/index.html', context)
    return renter_template


def single_pen(request, username, slug):
    if request.method == 'GET':
        if not username or not slug:
            return HttpResponseRedirect(home_url())
        pens = Pen.objects.all().filter(pen_slug=slug)
        context = {
            'site_url': get_current_site(request),
            'codepen_platform': pen_platform,
            'pens': pens
        }
        user = get_user(username)
        if user:
            context['user'] = user
            profile = get_profile(username)
            if profile:
                context['profile'] = profile
        renter_template = render(request, 'main/pen/single.html', context)
        return renter_template
    else:
        return HttpResponseRedirect(home_url())


def pen_edit(request, username, pen_id):
    return HttpResponse('ok')


def pen_delete(request, username, pen_id):
    return HttpResponse('ok')


def tag(request, tag_name):
    return HttpResponse('ok')


def pen_filter(request):
    return None
