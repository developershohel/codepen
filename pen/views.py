import os
import subprocess

from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.models import Permission

from django.apps import apps
from django.urls import reverse

from codepen.settings import BASE_DIR
from .models import Pen, PenData


def pen(request, username):
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
    renter_template = render(request, 'pen/index.html', context)
    return renter_template


def single_pen(request, username, slug):
    context = {
        'site_url': get_current_site(request)
    }
    get_pen = Pen.objects.all().filter(pen_slug=slug)
    if get_pen:
        context['pens'] = get_pen
        pen_id = get_pen.get().id
        pen_data = PenData.objects.all().filter(pen_id=pen_id)

        if pen_data:
            context['pen_data'] = pen_data

    renter_template = render(request, 'pen/single.html', context)
    return renter_template


def pen_edit(request, username):
    return HttpResponse('ok')


def pen_delete(request, username):
    return HttpResponse('ok')


def tag(request, tag_name):
    return HttpResponse('ok')
