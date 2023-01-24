from codepen.functions import email_validation, user_validation
from user.models import User
from profiles.models import Profile
from pen.models import Pen


def get_user(value):
    print('Value: ', value)
    check_id = isinstance(value, int)
    if not check_id and email_validation(value):
        user = User.objects.all().filter(email=value)
        if user:
            return user
        else:
            return False
    elif not check_id and user_validation(value):
        user = User.objects.all().filter(username=value)
        if user:
            return user
        else:
            return False
    elif isinstance(value, int):
        user = User.objects.all().filter(id=value)
        if user:
            return user
        else:
            return False
    else:
        return False


def get_user_by_code(code):
    if code:
        user = User.objects.all().filter(user_verification_code=code)
        if user:
            return user
        else:
            return False
    else:
        return False


def get_user_by_token(token):
    if token:
        user = User.objects.all().filter(user_activation_key=token)
        if user:
            return user
        else:
            return False
    else:
        return False


def get_profile(value):
    check_id = isinstance(value, int)
    if not check_id and email_validation(value):
        profile = Profile.objects.all().filter(user__email=value)
        if profile:
            return profile
        else:
            return False
    elif not check_id and user_validation(value):
        profile = Profile.objects.all().filter(user__username=value)
        if profile:
            return profile
        else:
            return False
    elif isinstance(value, int):
        profile = Profile.objects.all().filter(id=value)
        if profile:
            return profile
        else:
            return False
    else:
        return False


def trending_pens():
    all_pens = Pen.objects.all()
    pen_list = {}
    for pen in all_pens:
        pen_love = pen.pen_love.count()
        pen_view = pen.pen_view.count()
        if pen_love and pen_view:
            pen_avg = pen_love / pen_view
            pen_ratio = round(pen_avg, 2) * 100
            pen_list[pen.id] = pen_ratio
    return sorted(pen_list, reverse=True)


def popular_pens():
    all_pens = Pen.objects.all()
    pen_list = {}
    for pen in all_pens:
        pen_love = pen.pen_love.count()
        if pen_love:
            pen_list[pen.id] = pen_love
    return sorted(pen_list, reverse=True)


def most_views():
    all_pens = Pen.objects.all()
    pen_list = {}
    for pen in all_pens:
        pen_views = pen.pen_view.count()
        if pen_views:
            pen_list[pen.id] = pen_views
    return sorted(pen_list, reverse=True)


