from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from codepen.cp_user import get_user, get_profile
from codepen.functions import codepen_theme, codepen_platform, codepen_font
from pen.models import PenSetting
from setting.models import Setting


@login_required
@csrf_exempt
def profile_setting(request):
    username = request.user.username
    user_id = request.user.id
    user = get_user(user_id)
    profile = get_profile(username)
    context = {
        'user_id': user_id,
        'username': username,
        'user': user,
        'current_path_name': request.path_info[1:-1],
        'current_path': request.path[1:-1],
        'profile': profile,
    }

    render_template = render(request, 'dashboard/setting/profile-setting.html', context)
    return render_template


@login_required
def pen_setting(request):
    username = request.user.username
    user_id = request.user.id
    profile = get_profile(username)
    context = {
        'user_id': user_id,
        'username': username,
        'current_path_name': request.path_info[1:-1],
        'current_path': request.path[1:-1],
        'profile': profile
    }

    render_template = render(request, 'dashboard/setting/profile-setting.html', context)
    return render_template


@login_required
def account_setting(request):
    username = request.user.username
    user_id = request.user.id
    profile = get_profile(username)
    context = {
        'user_id': user_id,
        'username': username,
        'current_path_name': request.path_info[1:-1],
        'current_path': request.path[1:-1],
        'profile': profile
    }

    render_template = render(request, 'dashboard/setting/account-setting.html', context)
    return render_template


@login_required
def billing_setting(request):
    username = request.user.username
    user_id = request.user.id
    profile = get_profile(username)
    context = {
        'user_id': user_id,
        'username': username,
        'current_path_name': request.path_info[1:-1],
        'current_path': request.path[1:-1],
        'profile': profile
    }

    render_template = render(request, 'dashboard/setting/profile-setting.html', context)
    return render_template


@login_required
def appearance_setting(request):
    username = request.user.username
    user_id = request.user.id
    profile = get_profile(username)
    themes = PenSetting.objects.all().filter(user_id=user_id)

    context = {
        'user_id': user_id,
        'username': username,
        'current_path_name': request.path_info[1:-1],
        'current_path': request.path[1:-1],
        'profile': profile,
        'themes': themes,
        'all_theme': codepen_theme,
        'platform': codepen_platform,
        'fonts': codepen_font
    }

    render_template = render(request, 'dashboard/setting/appearance-setting.html', context)
    return render_template


@login_required
def notification_setting(request):
    username = request.user.username
    user_id = request.user.id
    profile = get_profile(username)
    context = {
        'user_id': user_id,
        'username': username,
        'current_path_name': request.path_info[1:-1],
        'current_path': request.path[1:-1],
        'profile': profile
    }

    render_template = render(request, 'dashboard/setting/profile-setting.html', context)
    return render_template


@login_required
def security_setting(request):
    username = request.user.username
    user_id = request.user.id
    profile = get_profile(username)
    context = {
        'user_id': user_id,
        'username': username,
        'current_path_name': request.path_info[1:-1],
        'current_path': request.path[1:-1],
        'profile': profile
    }

    render_template = render(request, 'dashboard/setting/profile-setting.html', context)
    return render_template


@login_required
def block_user_setting(request):
    username = request.user.username
    user_id = request.user.id
    profile = get_profile(username)
    context = {
        'user_id': user_id,
        'username': username,
        'current_path_name': request.path_info[1:-1],
        'current_path': request.path[1:-1],
        'profile': profile
    }

    render_template = render(request, 'dashboard/setting/profile-setting.html', context)
    return render_template


@csrf_exempt
def setting_update(request):
    context = {}
    if request.method == 'POST':
        user_id = request.user.id
        setting_name = request.POST.get('setting_name')
        field_name = request.POST.get('field_name')
        field_value = request.POST.get('field_value')
        if user_id and setting_name and field_value and field_name:
            setting_updated = Setting.objects.update_or_create(
                user_id=user_id,
                defaults={
                    'setting_name': setting_name,
                    f'{field_name}': field_value,
                }
            )

            if setting_updated:
                print(setting_updated)
                context['status'] = True
            else:
                context['status'] = False
        return JsonResponse(context)
    else:
        context['status'] = False
        context['get'] = 'GET'
        return JsonResponse(context)
