from codepen.functions import email_validation, user_validation
from user.models import User
from profiles.models import Profile


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
