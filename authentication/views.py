from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.contrib.auth import login
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
import json
from django.http import JsonResponse
from django.contrib import messages
from validate_email import validate_email
from .token import account_activation_token
from django.contrib import auth
from usersettings.models import UserSettings
from django.contrib.auth.tokens import default_token_generator


class UsernameValidationView(View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        username = data['username']
        if not str(username).isalnum():
            return JsonResponse({'username_error': 'Username should only contain alphanumeric characters'}, status=406)
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error': 'Sorry username is already taken,choose another one '}, status=409)
        if 5 > len(username) >= 1:
            return JsonResponse({'username_error': 'Username has to be more then 5 characters'}, status=406)
        return JsonResponse({'username_valid': True})


class EmailValidationView(View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        email = data['email']
        if not validate_email(email):
            return JsonResponse({'email_error': 'Please enter a valid email'}, status=400)
        if User.objects.filter(email=str(email).lower()).exists():
            return JsonResponse({'email_error': 'Email already taken'}, status=400)
        return JsonResponse({'email_valid': True})


class RegisterView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'authentication/register.html')

    def post(self, request, *args, **kwargs):
        user = request.POST
        context = {
            'fieldValues': request.POST
        }
        if not User.objects.filter(username=user['username']):
            if not User.objects.filter(email=user['email'].lower()):

                if user['password'] and user['password2']:
                    if user['password'] == user['password2']:
                        if len(user['password']) < 6:
                            messages.error(request, 'Password must be at least 6 digits long')
                            return render(request, 'authentication/register.html', context)

                        if len(user['username']) < 5:
                            messages.error(request, 'Username must be at least 5 digits long')
                            return render(request, 'authentication/register.html', context)

                        new_user = User.objects.create_user(username=user['username'], email=user['email'], password=user['password'])
                        new_user.is_active = False
                        new_user.save()

                        UserSettings.objects.create(user=new_user)

                        current_site = get_current_site(request)
                        subject = 'Activate your Account'
                        message = render_to_string('authentication/account_activation_email.html', {
                            'user': new_user,
                            'domain': current_site.domain,
                            'uid': urlsafe_base64_encode(force_bytes(new_user.pk)),
                            'token': account_activation_token.make_token(new_user),
                        })
                        new_user.email_user(subject=subject, message=message)

                        messages.success(request, 'Account successfully created an email has been sent to your email address')
                        return render(request, 'authentication/register.html')
                    else:
                        messages.error(request, 'Passwords must be identical')
                        return render(request, 'authentication/register.html', context)
                else:
                    messages.error(request, 'Please fill all the fields')
                    return render(request, 'authentication/register.html', context)

        messages.error(request, 'Username or email is invalid')
        return render(request, 'authentication/register.html', context)


class VerificationView(View):
    def get(self, request, uidb64, token):
        try:
            id = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)

            if not account_activation_token.check_token(user, token):
                return redirect('login'+'?message='+'User already activated')

            if user.is_active:
                return redirect('expenses:index')
            user.is_active = True
            user.save()

            messages.success(request, 'Account activated successfully')
            return redirect('authentication:login')

        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        return redirect('expenses:index')


class LoginView(View):
    def get(self, request, *args, **kwargs):

        return render(request, 'authentication/login.html')

    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        password = request.POST['password']
        context = {
            'username': username
        }

        if username and password:
            user = auth.authenticate(username=username, password=password)
            if user:
                if user.is_active:  # Maybe not needed 'if'
                    login(request, user)
                    messages.success(request, 'Welcome ' + user.username + '!')
                    return redirect('expenses:index')
            elif User.objects.filter(username=username).exists():
                messages.error(request, 'Account is not active,please check your email')
                return render(request, 'authentication/login.html', context)
            else:
                messages.error(request, 'Username or password is invalid, try again')
                return render(request, 'authentication/login.html', context)

        messages.error(request, 'Please fill all fields')
        return render(request, 'authentication/login.html', context)


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        auth.logout(request)
        messages.success(request, 'You have been logged out')
        return redirect('authentication:login')


class ChangePasswordView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'authentication/change_password.html')

    def post(self, request, *args, **kwargs):
        password = request.POST['password']
        new_password1 = request.POST['new_password1']
        new_password2 = request.POST['new_password2']

        user = User.objects.get(id=request.user.id)
        print(user.password)
        if user.check_password(password):
            if new_password1 and new_password2:
                if new_password1 == new_password2:
                    if len(new_password1) < 6:
                        messages.error(request, 'Password must be at least 6 digits long')
                        return render(request, 'authentication/change_password.html')
                    if password == new_password1:
                        messages.error(request, 'New password must be different form the old password')
                        return render(request, 'authentication/change_password.html')
                    user.set_password(new_password1)
                    user.save()
                    login(request, user)
                    messages.success(request, 'Password has been changed')
                    return render(request, 'authentication/change_password.html')
                else:
                    messages.error(request, 'Passwords must be identical')
                    return render(request, 'authentication/change_password.html')
            else:
                messages.error(request, 'Please fill all the fields')
                return render(request, 'authentication/change_password.html')

        else:
            messages.error(request, 'Wrong password')
            return render(request, 'authentication/change_password.html')


class RequestPasswordResetView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'authentication/reset_password.html')

    def post(self, request, *args, **kwargs):
        email = request.POST['email']

        context = {
            'values': request.POST
        }
        if not validate_email(email):
            messages.error(request, 'Please enter a valid email')
            return render(request, 'authentication/reset_password.html', context)
        if not User.objects.filter(email=email).exists():
            messages.error(request, 'Account with this email does not exist')
            return render(request, 'authentication/reset_password.html', context)

        this_user = User.objects.get(email=email)
        print(this_user.username)

        current_site = get_current_site(request)
        subject = 'Reset password for FinanceControl.com'
        message = render_to_string('authentication/reset_password_email.html', {
            'user': this_user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(this_user.pk)),
            'token': default_token_generator.make_token(this_user),
        })
        this_user.email_user(subject=subject, message=message)
        messages.success(request, f'A link has been send to {email}')

        return render(request, 'authentication/reset_password.html')


class PasswordResetConfirmView(View):

    def get(self, request, uidb64, token):
        try:
            context = {
                'uidb64': uidb64,
                'token': token
            }
            id = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)
            return render(request, 'authentication/reset_password_confirm.html', context)

        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        return redirect('expenses:index')

    def post(self, request, uidb64, token):

        try:
            context = {
                'uidb64': uidb64,
                'token': token
            }
            id = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)
            password = request.POST['password']
            password2 = request.POST['password2']
            if password and password2:
                if len(password) < 6:
                    messages.error(request, 'Password must be at least 6 digits long')
                    return render(request, 'authentication/reset_password_confirm.html', context)
                if password == password2:
                    user.set_password(password)
                    user.save()
                    login(request, user)
                    return render(request, 'dashboard/index.html')
                else:
                    messages.error(request, 'Passwords must be the same')
                    return render(request, 'authentication/reset_password_confirm.html', context)
            else:
                messages.error(request, 'Please fill all fields')
                return render(request, 'authentication/reset_password_confirm.html', context)

        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        return redirect('expenses:index')

