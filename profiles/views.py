from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render
from profiles.models import Profile


# Create your views here.
def index(request, username):
    auth_user = request.user.is_authenticated
    if auth_user:
        user_id = request.user.id
        profile = Profile.objects.filter(user_id=user_id)

        context = {
            'username': request.user.username,
            'id': request.user.id,
            'profile': profile,
            'user': request.user
        }
        return render(request, 'profiles/index.html', context)
    else:
        return render(request, 'profiles/index.html')
