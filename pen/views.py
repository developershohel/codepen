import datetime
import json
import os
import subprocess
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.core import serializers
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, Http404, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import Permission
from django.apps import apps
from django.urls import reverse
from django.utils.text import slugify
from datetime import date
from django.core.files import File
from django.views.decorators.csrf import csrf_exempt

from codepen.functions import pen_platform, home_url, create_pen_file_directory, random_token
from codepen.settings import BASE_DIR, BASE_URL
from setting.models import Setting
from .models import Pen, PenData
from codepen.cp_user import get_user, get_profile


def new_pen(request):
    if request.method == 'GET':
        pen_preview_link = request.GET.get('pen-preview-link')
        if pen_preview_link:
            return HttpResponseRedirect(pen_preview_link)
        else:
            context = {'base_url': BASE_URL}
            new_pen_platform = request.GET.get('platform')
            if request.user.is_authenticated:
                pen_user = get_user(request.user.id)
                context['pen_user'] = pen_user
            else:
                pen_user = get_user('guest_user')
                context['pen_user'] = pen_user

            if not new_pen_platform:
                new_pen_platform = 'html'
            pen_slug = random_token(12)
            new_pen = Pen.objects.create(user_id=pen_user.get().id, pen_title=f"Untitled {new_pen_platform}",
                                         pen_slug=pen_slug,
                                         pen_tag='HTML', pen_status='draft', pen_platform=new_pen_platform)
            if new_pen:
                pen = Pen.objects.all().filter(id=new_pen.id)
                context['pens'] = pen
                context['platform'] = new_pen.pen_platform
                context['pen_preview_link'] = f'/{new_pen.user.username}/pen/full/{new_pen.pen_slug}'
                html_val = '<!-- Default template is already include \nPlease write you code without using <html></html><body></body>\nWrite you code after body tag -->'
                css_val = '/*Welcome to VMS Editor\nCoding, design & Share you project*/'
                js_val = '/*Welcome to VMS Editor\n Coding, design & Share you project*/'
                context['html_value'] = html_val
                context['css_value'] = css_val
                context['js_value'] = js_val
                context['pen_type'] = 'new-pen'
                custom_file_val = '/*Welcome to VMS Editor\n Start Coding, build & Share you project*/'

                if new_pen.pen_platform == 'html':
                    file_path = create_pen_file_directory(request, new_pen.user.username, new_pen.pen_slug)
                    if not os.path.exists(file_path):
                        os.makedirs(file_path)
                    try:
                        with open(f'{file_path}/{new_pen.pen_slug}.html', 'w') as file:
                            html_file = File(file)
                            html_file.write(html_val)
                            html_file.close()
                            context['status'] = True
                    except Exception as e:
                        print(f'Error {e}')
                        context['status'] = False
                    try:
                        with open(f'{file_path}/{new_pen.pen_slug}.css', 'w') as file:
                            css_file = File(file)
                            css_file.write(css_val)
                            css_file.close()
                            context['status'] = True
                    except Exception as e:
                        print(f'Error {e}')
                        context['status'] = False
                    try:
                        with open(f'{file_path}/{new_pen.pen_slug}.js', 'w') as file:
                            js_file = File(file)
                            js_file.write(js_val)
                            js_file.close()
                            context['status'] = True
                    except Exception as e:
                        print(f'Error {e}')
                        context['status'] = False
                    PenData.objects.update_or_create(pen_id=new_pen.id, html=html_val, css=css_val, javascript=js_val)
                else:
                    if new_pen.pen_platform in pen_platform():
                        extension = pen_platform()[new_pen.pen_platform]['extension']
                    file_path = create_pen_file_directory(request, new_pen.username, new_pen.pen_slug)
                    if not os.path.exists(file_path):
                        os.makedirs(file_path)
                    try:
                        with open(f'{file_path}/{new_pen.pen_slug}.{extension}', 'w') as file:
                            custom_file = File(file)
                            custom_file.write(custom_file_val)
                            custom_file.close()
                            context['status'] = True
                    except Exception as e:
                        print(f'Error {e}')
                        context['status'] = False

            renter_template = render(request, 'main/pen/index.html', context)
            return renter_template
    else:
        return HttpResponseRedirect(home_url())


def single_pen(request, username, pen_slug):
    if request.user.is_authenticated:
        pen_user = get_user(request.user.id)
    else:
        pen_user = get_user('guest_user')
    context = {
        'site_url': get_current_site(request),
        'pen_date': datetime.date.today(),
        'pen_user': pen_user,
        'base_url': BASE_URL,
        'setting': Setting.objects.all().filter(user_id=pen_user.get().id)
    }
    if request.method == 'GET':
        if not username or not pen_slug:
            return HttpResponseRedirect(home_url())

        pens = Pen.objects.all().filter(pen_slug=pen_slug)
        if pens:
            context['pens'] = pens
            single_pen_platform = pens.get().pen_platform
            context['platform'] = single_pen_platform
            context['pen_slug'] = pens.get().pen_slug
            context['pen_type'] = 'single-pen'
            # context['pen_preview_link'] = pens.get().get_absolute_full_view_url() when live server
            context['pen_preview_link'] = f'/{pens.get().user.username}/pen/full/{pens.get().pen_slug}'

            pen_data = PenData.objects.all().filter(pen_id=pens.get().id)
            if pen_data:
                context['pen_data'] = pen_data
                json_data = serializers.serialize('json', pen_data)
                context['json_data'] = json_data
                print(json_data)
        login_user = get_user(username)

        if login_user:
            context['login_user'] = login_user
            profile = get_profile(username)

            if profile:
                context['profile'] = profile
        renter_template = render(request, 'main/pen/single.html', context)
        return renter_template
    else:
        return HttpResponseRedirect(home_url())


def single_pen_full(request, username, pen_slug):
    today = date.today()
    year = str(today.strftime("%Y"))
    month = str(today.strftime("%m"))
    context = {
        'site_url': get_current_site(request),
        'codepen_platform': pen_platform,
        'pen_date': datetime.date.today()
    }
    if request.method == 'GET':
        if not username or not pen_slug:
            return HttpResponseRedirect(home_url())

        pens = Pen.objects.all().filter(pen_slug=pen_slug)
        if pens:
            context['pens'] = pens
            single_pen_platform = pens.get().pen_platform
            context['platform'] = single_pen_platform
            pen_data = PenData.objects.all().filter(pen_id=pens.get().id)
            file_path = f'pen/{pens.get().username()}/{year}/{month}/{pens.get().pen_slug}'
            context['dynamic_css_file'] = f'{file_path}/{pens.get().pen_slug}.css'
            context[
                'dynamic_html_template'] = f'{file_path}/{pens.get().pen_slug}.html'
            print(f'{file_path}/{pens.get().pen_slug}.html')
            context['dynamic_js_file'] = f'{file_path}/{pens.get().pen_slug}.js'
            if pen_data:
                context['pen_data'] = pen_data
        renter_template = render(request, 'main/pen/full.html', context)
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


@csrf_exempt
def vms_save_pen(request):
    context = {}
    if request.method == 'POST':
        html_value = request.POST.get('html_value')
        css_value = request.POST.get('css_value')
        js_value = request.POST.get('js_value')
        pen_id = request.POST.get('pen_id')
        pen_user = request.POST.get('pen_user')
        pen_title = request.POST.get('pen_title')
        pen_description = request.POST.get('pen_description')
        pen_slug = request.POST.get('pen_slug')
        pen_tag = request.POST.get('pen_tag')
        pen_status = request.POST.get('pen_status')
        pen_type = request.POST.get('pen_type')

        if not pen_id:
            context['status'] = False
            return False
        else:
            if not html_value:
                html_value = ''
            if not css_value:
                css_value = ''
            if not js_value:
                js_value = ''
            create_pen_data = PenData.objects.update_or_create(
                pen_id=pen_id,
                defaults={
                    'html': html_value,
                    'css': css_value,
                    'javascript': js_value,
                }
            )
            if create_pen_data:
                context['status'] = True
            else:
                context['status'] = False
            return JsonResponse(context)
    else:
        context['status'] = False
        return JsonResponse(context)


def vms_live_pen(request):
    if request.method == 'POST':
        html_value = request.POST.get('html_value')
        css_value = request.POST.get('css_value')
        js_value = request.POST.get('js_value')
        pen_user = request.POST.get('pen_user')
        pen_title = request.POST.get('pen_title')
        pen_description = request.POST.get('pen_description')
        pen_slug = request.POST.get('pen_slug')
        pen_tag = request.POST.get('pen_tag')
        pen_status = request.POST.get('pen_status')
        pen_type = request.POST.get('pen_type')

    else:
        pass


@csrf_exempt
def vms_live_edit(request):
    context = {}
    if request.method == 'POST':
        editor_platform = request.POST.get('platform')
        pen_id = request.POST.get('pen_id')
        pen_user = request.POST.get('pen_user')
        pen_old_slug = request.POST.get('old_pen_slug')
        pen_new_slug = request.POST.get('new_pen_slug')

        if editor_platform in pen_platform() and editor_platform == 'html':
            html_value = request.POST.get('html_value')
            css_value = request.POST.get('css_value')
            js_value = request.POST.get('js_value')

            if pen_old_slug and pen_new_slug and pen_new_slug == pen_old_slug:
                file_path = create_pen_file_directory(request, pen_user, pen_new_slug)
                if not os.path.exists(file_path):
                    os.makedirs(file_path)
                if html_value:
                    try:
                        with open(f'{file_path}/{pen_new_slug}.html', 'w') as file:
                            html_file = File(file)
                            html_file.write(html_value)
                            html_file.close()
                            context['status'] = True
                    except Exception as e:
                        print(f'Error {e}')
                        context['status'] = False
                if css_value:
                    try:
                        with open(f'{file_path}/{pen_new_slug}.css', 'w') as file:
                            css_file = File(file)
                            css_file.write(css_value)
                            css_file.close()
                            context['status'] = True
                    except Exception as e:
                        print(f'Error {e}')
                        context['status'] = False
                if js_value:
                    try:
                        with open(f'{file_path}/{pen_new_slug}.js', 'w') as file:
                            js_file = File(file)
                            js_file.write(js_value)
                            js_file.close()
                            context['status'] = True
                    except Exception as e:
                        print(f'Error {e}')
                        context['status'] = False
            elif pen_new_slug and pen_old_slug and pen_new_slug != pen_old_slug:
                file_old_path = create_pen_file_directory(request, pen_user, pen_old_slug)
                if not os.path.exists(file_old_path):
                    os.makedirs(file_old_path)
                file_old_storage = FileSystemStorage(location=file_old_path)
                if file_old_storage.exists(f'{pen_old_slug}.html'):
                    os.remove(file_old_storage.path(f'{pen_old_slug}.html'))
                    # Check if the directory is empty
                    if not os.listdir(file_old_storage.location):
                        os.rmdir(file_old_storage.location)
                if file_old_storage.exists(f'{pen_old_slug}.css'):
                    os.remove(file_old_storage.path(f'{pen_old_slug}.css'))
                    # Check if the directory is empty
                    if not os.listdir(file_old_storage.location):
                        os.rmdir(file_old_storage.location)
                if file_old_storage.exists(f'{pen_old_slug}.js'):
                    os.remove(file_old_storage.path(f'{pen_old_slug}.js'))
                    # Check if the directory is empty
                    if not os.listdir(file_old_storage.location):
                        os.rmdir(file_old_storage.location)

                file_new_path = create_pen_file_directory(request, pen_user, pen_old_slug)
                if not os.path.exists(file_new_path):
                    os.makedirs(file_new_path)
                try:
                    with open(f'{file_new_path}/{pen_new_slug}.html', 'w') as file:
                        html_file = File(file)
                        html_file.write(html_value)
                        html_file.close()
                        context['status'] = True
                    with open(f'{file_new_path}/{pen_new_slug}.css', 'w') as file:
                        css_file = File(file)
                        css_file.write(css_value)
                        css_file.close()
                        context['status'] = True
                    with open(f'{file_new_path}/{pen_new_slug}.js', 'w') as file:
                        js_file = File(file)
                        js_file.write(js_value)
                        js_file.close()
                        context['status'] = True
                except Exception as e:
                    context['status'] = False
                    print(e)
            elif not pen_new_slug and pen_old_slug:
                file_old_path = create_pen_file_directory(request, pen_user, pen_old_slug)
                if not os.path.exists(file_old_path):
                    os.makedirs(file_old_path)
                try:
                    with open(f'{file_old_path}/{pen_old_slug}.html', 'w') as file:
                        html_file = File(file)
                        html_file.write(html_value)
                        html_file.close()
                        context['status'] = True
                    with open(f'{file_old_path}/{pen_old_slug}.css', 'w') as file:
                        css_file = File(file)
                        css_file.write(css_value)
                        css_file.close()
                        context['status'] = True
                    with open(f'{file_old_path}/{pen_old_slug}.js', 'w') as file:
                        js_file = File(file)
                        js_file.write(js_value)
                        js_file.close()
                        context['status'] = True
                except Exception as e:
                    context['status'] = False
                    print(e)
            elif pen_new_slug and not pen_old_slug:
                file_new_path = create_pen_file_directory(request, pen_user, pen_old_slug)
                if not os.path.exists(file_new_path):
                    os.makedirs(file_new_path)
                try:
                    with open(f'{file_new_path}/{pen_new_slug}.html', 'w') as file:
                        html_file = File(file)
                        html_file.write(html_value)
                        html_file.close()
                        context['status'] = False
                    with open(f'{file_new_path}/{pen_new_slug}.css', 'w') as file:
                        css_file = File(file)
                        css_file.write(css_value)
                        css_file.close()
                        context['status'] = False
                    with open(f'{file_new_path}/{pen_new_slug}.js', 'w') as file:
                        js_file = File(file)
                        js_file.write(js_value)
                        js_file.close()
                        context['status'] = False
                except Exception as e:
                    context['status'] = False
                    print(e)
        elif editor_platform in pen_platform() and editor_platform == 'python':
            editor_value = request.POST.get('editor_value')
            editor_extension = pen_platform()[editor_platform]['extension']
            if pen_old_slug and pen_new_slug and pen_new_slug == pen_old_slug:
                file_path = create_pen_file_directory(request, pen_user, pen_new_slug)
                file_storage = FileSystemStorage(location=file_path)
                with open(f'{file_path}.{editor_extension}', 'w') as file:
                    file.write(editor_value)
            elif pen_new_slug and pen_old_slug and pen_new_slug != pen_old_slug:
                file_old_path = create_pen_file_directory(request, pen_user, pen_old_slug)
                file_old_storage = FileSystemStorage(location=file_old_path)
                if file_old_storage.exists(f'{file_old_path}.{editor_extension}'):
                    os.remove(file_old_storage.path(f'{file_old_path}.{editor_extension}'))
                    # Check if the directory is empty
                    if not os.listdir(file_old_storage.location):
                        os.rmdir(file_old_storage.location)

                file_new_path = create_pen_file_directory(request, pen_user, pen_new_slug)
                file_new_storage = FileSystemStorage(location=file_new_path)

                with file_new_storage.open(f'{pen_new_slug}.{editor_extension}', 'w') as file:
                    file.write(editor_value)
            elif not pen_new_slug and pen_old_slug:
                file_old_path = create_pen_file_directory(request, pen_user, pen_old_slug)
                file_old_storage = FileSystemStorage(location=file_old_path)

                with file_old_storage.open(f'{file_old_path}.{editor_extension}', 'w') as file:
                    file.write(editor_value)
            elif pen_new_slug and not pen_old_slug:
                file_new_path = create_pen_file_directory(request, pen_user, pen_old_slug)
                file_new_storage = FileSystemStorage(location=file_new_path)

                with file_new_storage.open(f'{pen_new_slug}.{editor_extension}', 'w') as file:
                    file.write(editor_value)

        return JsonResponse(context)
    else:
        context['status'] = False
        return JsonResponse(context)
