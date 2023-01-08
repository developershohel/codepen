import re
from datetime import date, datetime, timedelta
from django.utils import timezone
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.password_validation import CommonPasswordValidator
from django.contrib.auth.hashers import make_password
from django.contrib.sites.shortcuts import get_current_site
from django.views.decorators.csrf import csrf_exempt

from codepen.functions import user_validation, password_validation, email_validation, random_token, random_code, \
    admin_url, make_cookies_password, decode_cookies_password, name_validation, get_client_ip, get_client_details_by_ip, \
    dashboard_url, password_helper_text, home_url
from codepen.cp_user import get_user, get_user_by_code, get_user_by_token
from django.utils.html import strip_tags
from codepen.settings import EMAIL_HOST_USER, COOKIE_MAX_AGE
from .models import User, UserLogs

username_validator = UnicodeUsernameValidator
password_validator = CommonPasswordValidator


# Create your views here.
def user_login(request):
    site_url = get_current_site(request)
    context = {
        'site_url': site_url,
    }
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect(dashboard_url())
        cookies_username = request.COOKIES.get('username')
        cookies_password = request.COOKIES.get('password')
        if cookies_username:
            context['cookies_username'] = cookies_username
        if cookies_password:
            context['cookies_password'] = decode_cookies_password(cookies_password)
        return render(request, 'form/login_form.html', context)
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        rememberme = request.POST.get('rememberme')
        print(rememberme)
        redirect_url = request.GET.get('next')
        user_details = get_user(username)
        if user_details:
            auth_email = user_details.get().email
            if user_details.get().check_password(password):
                user_auth = authenticate(request, email=auth_email, password=password)
                if user_auth is not None:
                    login(request, user_auth)
                    user_ip = get_client_ip(request)
                    user_details_by_ip = get_client_details_by_ip(user_ip)
                    current_time = datetime.now()
                    if user_details_by_ip['status'] == 'success':
                        user_country = user_details_by_ip['country']
                        user_city = user_details_by_ip['city']
                        UserLogs.objects.create(user_id=user_details.get().id, user_country=user_country,
                                                user_city=user_city,
                                                user_login=current_time, user_ip=user_ip)
                    else:
                        UserLogs.objects.create(user_id=user_details.get().id, user_login=current_time,
                                                user_ip=user_ip)
                    delete_user_log = UserLogs.objects.all().filter(user_login__lte=datetime.now() - timedelta(30))

                    if delete_user_log:
                        delete_user_log.delete()
                    login_template = HttpResponseRedirect(dashboard_url())
                    login_template.delete_cookie('success')
                    login_template.delete_cookie('auth_error')
                    if rememberme:
                        hash_password = make_cookies_password(password)
                        login_template.set_cookie('password', hash_password, max_age=COOKIE_MAX_AGE)
                        login_template.set_cookie('username', username, max_age=COOKIE_MAX_AGE)
                    else:
                        login_template.delete_cookie('password')
                        login_template.delete_cookie('username')
                    if redirect_url:
                        login_template = HttpResponseRedirect(redirect_url)
                    return login_template
            else:
                context['invalid_password'] = 'password did not match'
                render_template = render(request, 'form/login_form.html', context)
                return render_template
        else:
            if re.search(r'@', username):
                context['invalid_username'] = f"{username} is incorrect email or didn't exists"
            else:
                context['invalid_username'] = f"{username} is incorrect username or didn't exists"
        render_template = render(request, 'form/login_form.html', context)
        return render_template
    else:
        return HttpResponseRedirect(home_url())


def signup(request):
    site_url = get_current_site(request)
    if request.user.is_authenticated:
        return redirect(dashboard_url())
    else:
        context = {
            'site_url': site_url,
        }
        render_template = render(request, 'form/signup_form.html', context)
        if request.method == "POST":

            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            cpassword = request.POST.get('cpassword')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')

            if username and user_validation(username):
                user = get_user(username)
                if user:
                    context['username_error'] = f'{username} already exists.'
                else:
                    context['username'] = username
                    username = username
            else:
                context['username_error'] = "Username validation error."

            if email and email_validation(email):
                user_email = get_user(email)
                if user_email:
                    context['email_error'] = f'{email} already exits.'
                else:
                    context['email'] = email
                    email = email
            else:
                context['email_error'] = "Email validation error."

            if password != cpassword:
                context['password_error'] = "Those passwords didn't match. Try again."
            elif password and not password_validation(password):
                context['password_error'] = "Your field password didn't match our password validation rules"
            else:
                context['password'] = password
                password = password

            if first_name and not name_validation(first_name):
                context['fname_error'] = "First name validation error"
            else:
                context['fname'] = first_name
                first_name = first_name

            if last_name and not name_validation(last_name):
                context['lname_error'] = "First name validation error"
            else:
                context['lname'] = last_name
                last_name = last_name

            if username and user_validation(username) and not get_user(username) and email and email_validation(
                    email) and not get_user(email) and password and password_validation(
                password) and password == cpassword and first_name and last_name:
                create_user = User.objects.create_user(username=username, email=email, password=password,
                                                       first_name=first_name, last_name=last_name)
                if create_user:
                    verified_code = random_code(111111, 999999)
                    verified_token = random_token(32)
                    get_date = date.today()
                    year = get_date.strftime("%Y")
                    update_user = get_user(username)
                    update_user.update(user_activation_key=verified_token, user_verification_code=verified_code)
                    email_context = {
                        'site_url': site_url,
                        'username': first_name,
                        'email': email,
                        'verified_code': verified_code,
                        'verified_token_url': f'{site_url.domain}/auth/verified-token?token={verified_token}',
                        'year': year
                    }
                    template = render_to_string('form/login_email_template.html', email_context)
                    email_template = strip_tags(template)
                    subject = f'{first_name} verify your {site_url.name} account'

                    mail = EmailMultiAlternatives(subject, email_template, EMAIL_HOST_USER, [email])
                    mail.fail_silently = True
                    mail.attach_alternative(template, 'text/html')
                    mail.send()
                    if mail:
                        signup_template = HttpResponseRedirect('/auth/verified-code')
                        signup_template.set_cookie('success',
                                                   'Your account create successfully. Please verify your account')
                        return signup_template
                else:
                    context['auth_error'] = "Something went to wrong to create your account. Please try again"
            else:
                context[
                    'auth_error'] = "Something went to wrong to create your account. Please check the error and try again"
                render_template = render(request, 'form/signup_form.html', context)
                return render_template
        else:
            return render_template


def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('/')
    else:
        return redirect('/login')


def verified_code(request):
    site_url = get_current_site(request)
    if request.user.is_authenticated:
        return redirect('dashboard_url')
    else:
        context = {
            'site_url': site_url,
            'form_name': "Verification Code",
            'resend_url': '/auth/verified-code-resend'
        }
        verification_code = request.POST.get('verification')
        render_template = render(request, 'form/otp-verification.html', context)
        if request.method == "POST":
            user = get_user_by_code(verification_code)
            success_template = HttpResponseRedirect('/login')
            if user:
                if user.get().is_staff and user.get().is_active and user.get().user_status:
                    success_template.set_cookie('success', f'{user.get().first_name} Your account already verified')
                    return success_template
                else:
                    update_user = user.update(user_status=True, is_staff=True, is_active=True)
                    if update_user:
                        user.update(user_verification_code=0, user_activation_key='')
                        success_template.set_cookie('success', 'Your account successfully verified')
                        return success_template
                    else:
                        context['auth_error'] = "Something went to wrong to verified your account. Please try again"
                        render_template = render(request, 'form/otp-verification.html', context)
                        return render_template
            else:
                context['code_error'] = "Your verification code is invalid"
                render_template = render(request, 'form/otp-verification.html', context)
                render_template.delete_cookie('success')
                return render_template
        else:
            return render_template


def verified_token(request):
    if request.user.is_authenticated:
        return redirect('dashboard_url')
    else:
        token = request.GET.get('token')
        user = get_user_by_token(token)
        render_template = HttpResponseRedirect('/login')
        if user:
            user.update(user_status=True, user_activation_key="", user_verification_code=0,
                        is_staff=True, is_active=True)
            render_template.set_cookie('success', 'Your account successfully verified')
            return render_template
        else:
            render_template.set_cookie('auth_error',
                                       "Something went to wrong to verified your account. Please try again")
            return render_template


def verified_code_resend(request):
    site_url = get_current_site(request)
    if request.user.is_authenticated:
        return redirect('dashboard_url')
    else:
        context = {
            'site_url': site_url,
            'form_name': 'Resend verification code'
        }
        render_template = render(request, 'form/forgot-password.html', context)
        if request.method == "POST":
            username = request.POST.get('username')
            verified_code = random_code(111111, 999999)
            verified_token = random_token(32)
            get_date = date.today()
            year = get_date.strftime("%Y")
            user = get_user(username)
            if user:
                email = user.get().email
                code_template = redirect('user:auton_code')
                user.update(user_activation_key=verified_token, user_verification_code=verified_code)
                email_context = {
                    'site_url': site_url,
                    'username': user.get().first_name,
                    'email': email,
                    'verified_code': verified_code,
                    'verified_token_url': f'{site_url.domain}/auth/verified-token?token={verified_token}',
                    'year': year
                }
                template = render_to_string('form/change_password_email_template.html', email_context)
                email_template = strip_tags(template)
                subject = f'{user.get().first_name} verify your {site_url.name} account'
                mail = EmailMultiAlternatives(subject, email_template, EMAIL_HOST_USER, [email])
                mail.fail_silently = True
                mail.attach_alternative(template, 'text/html')
                mail.send()
                code_template.set_cookie('success', 'Your verification code sent successfully')
                return code_template
            else:
                context['username_error'] = f"{username} didn't exists. Check your email and try again."
                render_template = render(request, 'form/forgot-password.html', context)
                return render_template
        else:
            return render_template


def forgot_password(request):
    site_url = get_current_site(request)
    if request.user.is_authenticated:
        return redirect('dashboard_url')
    else:
        context = {
            'site_url': site_url,
            'form_name': "Forgot Password"
        }
        render_template = render(request, 'form/forgot-password.html', context)
        if request.method == "POST":
            username = request.POST.get('username')
            verified_code = random_code(111111, 999999)
            verified_token = random_token(32)
            get_date = date.today()
            year = get_date.strftime("%Y")
            user = get_user(username)
            if user:
                email = user.get().email
                forgot_layout = HttpResponseRedirect('/auth/change-password-code')
                user.update(user_activation_key=verified_token, user_verification_code=verified_code)
                email_context = {
                    'site_url': site_url,
                    'username': user.get().first_name,
                    'email': email,
                    'verified_code': verified_code,
                    'verified_token_url': f'{site_url.domain}/auth/change-password-token?token={verified_token}',
                    'year': year
                }
                template = render_to_string('form/change_password_email_template.html', email_context)
                email_template = strip_tags(template)
                subject = f'{user.get().first_name} verify your {site_url.name} account'
                mail = EmailMultiAlternatives(subject, email_template, EMAIL_HOST_USER, [email])
                mail.fail_silently = True
                mail.attach_alternative(template, 'text/html')
                mail.send()
                forgot_layout.set_cookie('success', f'Please type the password resend code send to {email}')
                return forgot_layout
            else:
                context['username_error'] = f"{username} didn't exists. Check your username and try again."
                render_template = render(request, 'form/forgot-password.html', context)
                return render_template
        else:
            return render_template


def change_password(request):
    site_url = get_current_site(request)
    context = {
        'site_url': site_url,
        'form_name': 'Change Password'
    }
    render_template = render(request, 'form/change-password.html', context)
    if request.method == "POST":
        username = request.COOKIES.get('username')
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword')
        if password and cpassword and password == cpassword:
            if password and password_validation(password):
                username_template = HttpResponseRedirect('/login')
                if username:
                    user = get_user(username)
                    if user:
                        change_password_template = HttpResponseRedirect('/login')
                        hash_password = make_password(password)
                        user.update(password=hash_password)
                        change_password_template.delete_cookie('username')
                        change_password_template.delete_cookie('auth_error')
                        change_password_template.set_cookie('success', "Your password change successfully")
                        return change_password_template
                    else:
                        context['username_error'] = "username didn't exists"
                        render_template = render(request, 'form/change-password.html', context)
                        return render_template
                else:
                    username_template.set_cookie('auth_error', "We didn't find any username")
                    return username_template
            else:
                context['password_error'] = "Your field password didn't match our password rules"
                render_template = render(request, 'form/change-password.html', context)
                return render_template
        else:
            context['password_error'] = "Those password didn't match"
            render_template = render(request, 'form/change-password.html', context)
            return render_template
    else:
        return render_template


def change_password_code(request):
    site_url = get_current_site(request)
    if request.user.is_authenticated:
        return redirect('dashboard_url')
    else:
        context = {
            'site_url': site_url,
            'form_name': "OTP Verification",
            'resend_url': '/auth/change-password-resend-code'
        }
        render_template = render(request, 'form/otp-verification.html', context)
        verification_code = request.POST.get('verification')
        if verification_code and request.method == "POST":
            user = get_user_by_code(verification_code)
            if user:
                username = user.get().username
                change_template = HttpResponseRedirect('/auth/change-password')
                user.update(user_verification_code=0, user_activation_key='')
                change_template.set_cookie('success', 'Your are on the last stage. Change your password')
                change_template.set_cookie('username', username)
                return change_template
            else:
                context['code_error'] = "Your verification code is invalid"
                render_template = render(request, 'form/otp-verification.html', context)
                return render_template
        else:
            return render_template


def change_password_resend_code(request):
    site_url = get_current_site(request)
    if request.user.is_authenticated:
        return redirect('dashboard_url')
    else:
        context = {
            'site_url': site_url,
            'form_name': 'Resend change password Code',
        }
        render_template = render(request, 'form/forgot-password.html', context)
        if request.method == "POST":
            username = request.POST.get('username')
            verified_code = random_code(111111, 999999)
            verified_token = random_token(32)
            get_date = date.today()
            year = get_date.strftime("%Y")
            user = get_user(username)
            if user:
                code_template = HttpResponseRedirect('/auth/change-password-code')
                email = user.get().email
                user.update(user_activation_key=verified_token, user_verification_code=verified_code)
                email_context = {
                    'site_url': site_url,
                    'username': user.get().first_name,
                    'email': email,
                    'verified_code': verified_code,
                    'verified_token_url': f'{site_url.domain}/auth/change-password-token?token={verified_token}',
                    'year': year
                }
                template = render_to_string('form/change_password_email_template.html', email_context)
                email_template = strip_tags(template)
                subject = f'{user.get().first_name} verify your {site_url.name} account'
                mail = EmailMultiAlternatives(subject, email_template, EMAIL_HOST_USER, [email])
                mail.fail_silently = True
                mail.attach_alternative(template, 'text/html')
                mail.send()
                code_template.set_cookie('success', f'Please type the password resend code send to {email}')
                return code_template
            else:
                context['username_error'] = f"{username} didn't exists. Check your username and try again."
                render_template = render(request, 'form/forgot-password.html', context)
                return render_template
        else:
            return render_template


def change_password_token(request):
    if request.user.is_authenticated:
        return redirect('dashboard_url')
    else:
        login_template = HttpResponseRedirect('/login')
        if request.method == "GET":
            token = request.GET.get('token')
            user = get_user_by_token(token)
            if user:
                username = user.get().username
                change_layout = HttpResponseRedirect('/auth/change-password')
                user.update(user_verification_code=0, user_activation_key='')
                change_layout.set_cookie('success', 'Your are on the last stage. Change your password')
                change_layout.set_cookie('username', username)
                return change_layout
            else:
                login_template.set_cookie('auth_error',
                                          'Something went to wrong to verified your token. Please try again')
                return login_template
        return login_template


@csrf_exempt
def user_validation(request):
    if request.method == 'GET':
        return HttpResponseRedirect(home_url())
    elif request.method == 'POST':
        user_value = request.POST.get('user_value')
        validation_type = request.POST.get('type')
        print(user_value)
        print(validation_type)
        context = {}
        if validation_type == 'username':
            print('username ', user_value)
            if user_value:
                user = User.objects.all().filter(username=user_value)
                print('user :', user)
                if user:
                    print('problem come here')
                    context['result'] = user.get().username
                    return JsonResponse(context)
                else:
                    context['result'] = user_value
                    return JsonResponse(context)
        return JsonResponse(context)
