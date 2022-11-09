from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.core.files import storage
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from codepen.cp_user import get_profile
from codepen.functions import create_file_directory, get_mime_type, new_name, get_client_ip, \
    get_client_details_by_ip
from codepen.settings import MEDIA_URL
from pen.models import Pen, Comment, PenData
from user.models import User, UserLogs
from .models import Media


@login_required
@csrf_exempt
def dashboard(request):
    username = request.user.username
    user_id = request.user.id
    user = User.objects.all().filter(id=request.user.id)
    profile = get_profile(username)
    all_pen = Pen.objects.all().filter(user_id=user_id).order_by('-id')
    all_comments = Comment.objects.all().filter(user_id=user_id).order_by('-id')
    publish_pen = all_pen.filter(pen_status='published')
    private_pen = all_pen.filter(pen_status='private')
    draft_pen = all_pen.filter(pen_status='draft')
    trash_pen = all_pen.filter(pen_status='trash')
    login_status = UserLogs.objects.all().filter(user_id=user_id).order_by('-id')

    context = {
        'user_id': user_id,
        'username': username,
        'user': user,
        'current_path_name': request.path_info[1:-1],
        'current_path': request.path[1:-1],
        'all_pen': all_pen,
        'publish_pen': publish_pen,
        'private_pen': private_pen,
        'draft_pen': draft_pen,
        'trash_pen': trash_pen,
        'all_comments': all_comments,
        'login_status': login_status,
        'profile': profile
    }

    render_template = render(request, 'dashboard/dashboard.html', context)
    return render_template


@login_required
@csrf_exempt
def dashboard_pen(request):
    username = request.user.username
    user_id = request.user.id
    user = User.objects.all().filter(id=request.user.id)
    profile = get_profile(username)
    all_pen = Pen.objects.all().filter(user_id=user_id)
    all_comments = Comment.objects.all().filter(user_id=user_id)
    publish_pen = all_pen.filter(pen_status='published')
    private_pen = all_pen.filter(pen_status='private')
    draft_pen = all_pen.filter(pen_status='draft')
    trash_pen = all_pen.filter(pen_status='trash')

    context = {
        'user_id': user_id,
        'username': username,
        'user': user,
        'current_path_name': request.path_info[1:-1],
        'current_path': request.path[1:-1],
        'all_pen': all_pen,
        'all_comments': all_comments,
        'publish_pen': publish_pen,
        'private_pen': private_pen,
        'draft_pen': draft_pen,
        'trash_pen': trash_pen,
        'profile': profile
    }

    render_template = render(request, 'dashboard/pen.html', context)
    return render_template


@login_required
@csrf_exempt
def dashboard_comments(request):
    username = request.user.username
    user_id = request.user.id
    user = User.objects.all().filter(id=request.user.id)
    profile = get_profile(username)
    all_comments = Comment.objects.all().filter(user_id=user_id)

    context = {
        'user_id': user_id,
        'username': username,
        'user': user,
        'current_path_name': request.path_info[1:-1],
        'current_path': request.path[1:-1],
        'all_comments': all_comments,
        'profile': profile
    }

    render_template = render(request, 'dashboard/comments.html', context)
    return render_template


@login_required
@csrf_exempt
def dashboard_media(request):
    mime_type = get_mime_type()
    img_mime_type = ['.gif', '.jpg', '.jpe', '.jpeg', '.png', 'webp', '.svg']
    video_mime_type = ['.mp4', '.mpeg', '.m1v', '.mpa', '.mpe', '.mpg', '.mov', '.qt', '.webm', '.avi', '.movie']
    username = request.user.username
    profile = get_profile(username)
    all_media_list = Media.objects.all().order_by('-id')
    paginate_media = Paginator(all_media_list, 36)
    current_page = request.GET.get('page')
    media_list = paginate_media.get_page(current_page)
    context = {
        'user_id': request.user.id,
        'username': username,
        'current_path_name': request.path_info[1:-1],
        'current_path': request.path[1:-1],
        'url': request.get_host(),
        'mime': ','.join(mime_type),
        'img_mime_type': img_mime_type,
        'video_mime_type': video_mime_type,
        'media_list': media_list,
        'pagination': paginate_media,
        'profile': profile
    }
    render_template = render(request, 'dashboard/media.html', context)
    return render_template


@csrf_exempt
def upload_file(request):
    file = request.FILES.get('file')
    directory = create_file_directory(request)
    domain = get_current_site(request).domain
    user = int(request.user.id)
    file_title = file.name
    file_name = storage.get_valid_filename(file_title)
    only_name = file_name[:file_name.rfind('.')]
    file_url = f'{MEDIA_URL}{directory}/{file_name}'
    file_size = file.size
    file_mime = file.content_type
    file_ext = f".{file_name.split('.').pop()}"
    if file_mime == '':
        file_mime = 'unattached'

    if file_ext in get_mime_type():
        get_media = Media.objects.all()
        if get_media.filter(file_url__icontains=only_name):
            count_file = get_media.filter(file_url__icontains=only_name).count()
            name = new_name(file_name, count_file)
            new_url = f'{MEDIA_URL}{directory}/{name}'
            location = f'{directory}/{name}'
            upload_media = Media.objects.create(user_id=user, file_title=file_title, file_name=name, file_url=new_url,
                                                file_size=file_size, mime_type=file_mime)
            if upload_media:
                file_id = upload_media.id
                save_files = storage.FileSystemStorage()
                save_files.save(location, file)
                return JsonResponse({'file_id': file_id, 'file_url': new_url, 'file_name': name})
        else:
            upload_media = Media.objects.create(user_id=user, file_title=file_title, file_name=file_name,
                                                file_url=file_url, file_size=file_size, mime_type=file_mime)
            if upload_media:
                file_id = upload_media.id
                location = f'{directory}/{file_name}'
                save_files = storage.FileSystemStorage()
                save_files.save(location, file)
                return JsonResponse({'file_id': file_id, 'file_url': file_url, 'file_name': file_name})
    else:
        return False
    return JsonResponse({'file_url': file_url, 'file_name': file_name})


@login_required
def dashboard_profile(request):
    user_id = request.user.id
    user = User.objects.all().filter(id=user_id)
    username = user.get().username
    ip = get_client_ip(request)
    profile = get_profile(username)
    pens = Pen.objects.all().filter(user_id=user_id)
    pen_data = PenData.objects.all()
    comments = Comment.objects.all().filter(user_id=user_id)

    for pen in pens:
        var = pen.pen_love.all().count

    if profile and profile.get().screen_name:
        screen_name = profile.get().screen_name
    else:
        screen_name = request.user.get_full_name()
    if ip != '':
        user_details = get_client_details_by_ip('103.239.255.44')

    context = {
        'user_id': user_id,
        'username': username,
        'current_path_name': request.path_info[1:-1],
        'current_path': request.path[1:-1],
        'location': user_details['country'],
        'screen_name': screen_name,
        'profile': profile,
        'follower': user.get().follower.count(),
        'following': user.get().following.count(),
        'pens': pens,
        'pen_data': pen_data,
        'comments': comments,
    }
    if profile:
        context['social_links'] = profile.get().profile_links

    render_template = render(request, 'dashboard/profile.html', context)
    return render_template


@login_required
def activities(request):
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

    render_template = render(request, 'dashboard/profile.html', context)
    return render_template
