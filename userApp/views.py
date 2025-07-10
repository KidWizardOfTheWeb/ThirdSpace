from django.shortcuts import render
from django.http import HttpResponse

from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django.urls import reverse_lazy, reverse
from django.contrib.auth import login
from django.contrib import messages
from django.views import View
from django.views.generic import ListView
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.contrib.auth import logout as logout_view
from django.shortcuts import redirect
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect, Http404
from django.utils.decorators import method_decorator
from django.utils.dateparse import parse_date
from django.db.models import Q, F, Sum, Count, DecimalField, ExpressionWrapper, Prefetch
from datetime import datetime
import boto3, logging, csv
import requests
import json
import math
from urllib.parse import quote

from .forms import *
from .models import (AuditLog, NotificationSettings, Account)
from .helpers import *
# from notifications.signals import notify
# from notifications.models import Notification

def index(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'users/home.html')
    # return HttpResponse("Hello, world. You're at the userApp index.")

# Create your views here.

#-------------|| Login Functions ||-------------#

class LoginView(View):
    form_class = LoginForm
    template_name = 'users/login.html'

    def get(self, request, *args, **kwargs):
        # Check if the user is authenticated first
        if request.user.is_authenticated:
            return redirect('dashboard')

        # If the user is not authenticated, render the login form
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        username = ""
        if form.is_valid():
            try:
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']

                client = boto3.client('cognito-idp', region_name=settings.AWS_COGNITO_REGION)

                # https://stackoverflow.com/questions/73029150/how-can-i-get-the-client-ip-address-in-django
                x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
                if x_forwarded_for:
                    ip = x_forwarded_for.split(',')[0]
                else:
                    ip = request.META.get('REMOTE_ADDR')

                response = client.initiate_auth(
                    ClientId=settings.AWS_COGNITO_CLIENT_ID,
                    AuthFlow='USER_PASSWORD_AUTH',
                    AuthParameters={
                        'USERNAME': username,
                        'PASSWORD': password
                    },
                    UserContextData = {
                        'IpAddress': ip,
                    }
                )

                accesstoken=response['AuthenticationResult']['AccessToken']
                user, _ = User.objects.get_or_create(username=client.get_user(AccessToken=accesstoken)['Username'])
                user.aws_token=accesstoken
                user.save()
                login(request, user)

                # add the incrementation of points every time the driver logs in
                if is_basic(user):
                    account, _ = Account.objects.get_or_create(user=request.user)
                    # driver.point_balance += 10000
                    account.save()
                audit_log_write("Logged into account.", user=user, category=AuditLog.CATEGORY_CHOICES.LOGIN_ATTEMPT)
                return redirect('dashboard')
            except client.exceptions.NotAuthorizedException:
                form.add_error(None, "Username and password do not match.")
                try:
                    user = User.objects.filter(Q(username=username) | Q(email=username)).first()
                except:
                    user = None
                audit_log_write("There was a failed attempted login with username: " + username, user=user, category=AuditLog.CATEGORY_CHOICES.LOGIN_ATTEMPT)
            except client.exceptions.TooManyRequestsException:
                form.add_error(None, "Too many requests. Try again later.")
            except client.exceptions.PasswordResetRequiredException:
                form.add_error(None, "You must reset your password first.")
            except client.exceptions.UserNotFoundException:
                form.add_error(None, "This user does not exist in our system.")
            except client.exceptions.UserNotConfirmedException:
                form.add_error(None, "Your account is not verified yet! Check your email!")
            except Exception as e:
                form.add_error(None, str(e))

        return render(request, self.template_name, {'form': form})


def logout(request):
    logout_view(request)
    return redirect('home')

def audit_log_write(message, user=None, sponsor=None, category=AuditLog.CATEGORY_CHOICES.OTHER):
    # writes an audit log with a user and message passed in
    if sponsor:
        audit = AuditLog(user=user, log_message=message, sponsor=sponsor, timestamp=datetime.now(), category=category)
    else:
        audit = AuditLog(user=user, log_message=message, timestamp=datetime.now(), category=category)
    audit.save()
    pass

class RegisterView(View):
    form_class = RegisterForm
    template_name = 'users/register.html'

    def get(self, request, *args, **kwargs):
        # gets the website page(?)
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        # writes to the directory and goes to login page
        form = self.form_class(request.POST)

        if form.is_valid():
            # here, we need to send the SignUp request (add user details instead of set data here)
            try:
                client = boto3.client('cognito-idp', region_name=settings.AWS_COGNITO_REGION)
                response = client.sign_up(
                    ClientId = settings.AWS_COGNITO_CLIENT_ID,
                    # SecretHash='string',
                    Username=form.cleaned_data['username'], # clean data to prevent SQL injection
                    Password=form.cleaned_data['password1'],
                    UserAttributes=[
                        {
                            'Name': 'email',
                            'Value': form.cleaned_data['email']
                        },
                        {
                            'Name': 'updated_at',
                            'Value': '0'
                        },
                        {
                            'Name': 'picture',
                            'Value': 'default.png'
                        },
                        {
                            'Name': 'given_name',
                            'Value': form.cleaned_data['first_name']
                        },
                        {
                            'Name': 'family_name',
                            'Value': form.cleaned_data['last_name']
                        }
                    ]
                )

                user = User.objects.create_user(
                    username=form.cleaned_data['username'],
                    email=form.cleaned_data['email'],
                    first_name=form.cleaned_data['first_name'],
                    last_name=form.cleaned_data['last_name'],
                    phone_number=form.cleaned_data['phone'],
                    is_active=False
                )
                user.save()
                NotificationSettings.objects.create(user=user)
                Account.objects.create(user=user)

                return redirect(reverse('code_confirm')+"?username="+user.username)
            except client.exceptions.UsernameExistsException:
                form.add_error('username', 'This username already exists.')
            except client.exceptions.InvalidPasswordException as e:
                form.add_error('password1', e.response['Error']['Message'])
            except Exception as e:
                form.add_error(None, str(e))

        return render(request, self.template_name, {"form": form})

class ResetPasswordView(View):
    template_name = 'users/reset_pwd.html'
    form_class = ResetPasswordForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            client = boto3.client('cognito-idp', region_name=settings.AWS_COGNITO_REGION)

            response = client.forgot_password(
                ClientId=settings.AWS_COGNITO_CLIENT_ID,
                Username=form.cleaned_data['email'],
            )

            messages.success(request, "Password reset email has been sent.")
            return redirect('reset_pwd_confirm')

        return render(request, self.template_name, {'form': form})