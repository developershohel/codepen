from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.shortcuts import render


def error_404(request, exception):
    context = {
        'site_url': get_current_site(request)
    }
    return render(request, 'base/404.html', context)


def url_not_found(request):
    context = {
        'site_url': get_current_site(request)
    }
    return render(request, 'base/404.html', context)


def search(request):
    return HttpResponse('ok')
