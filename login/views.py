from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template.loader import get_template, render_to_string
from django.urls import reverse
from django.views import View
from django.views.generic import DetailView, FormView, TemplateView

from login import forms
from login.forms import RegisterForm


class LoginView(FormView):
    form_class = forms.LoginForm
    template_name = 'login.html'

    def post(self, request, *args, **kwargs):
        #this needs to clear URL query params on error

        form = self.get_form()
        if form.is_valid():
            email, password = form.cleaned_data['email'], form.cleaned_data['password']
            form.password = ''
            user = authenticate(request, username=email, email=email, password=password)
            if not user:
                try:
                    User.objects.get(email=email)
                except User.DoesNotExist:
                    errors = ['No account found for {} - please register an account.'.format(email)]
                else:
                    errors = ['Invalid password.']
                print(errors)
                return render(request, self.template_name, context={'errors': errors, 'form':form})
            else:
                login(request, user)
                return redirect('home-view')

class RegisterView(FormView):
    form_class = RegisterForm
    template_name = 'register.html'

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        errors = []

        if form.is_valid():
            email, password, confirm_password = form.cleaned_data['email'], form.cleaned_data['password'], form.cleaned_data['confirm_password']
            if User.objects.filter(email=email).exists():
                errors.append('Email address already in use.')
            if password != confirm_password:
                errors.append('Passwords do not match.')
        else:
            errors = form.errors

        if errors:
            return render(request, self.template_name, context={'errors': errors, 'form': form})
        else:
            User.objects.create_user(username=email, email=email, password=password)
            # Trigger email verification here
            return redirect("{}?{}={}".format(reverse('login-view'), 'created', 'true'))


class HomeView(TemplateView):
    template_name = 'home.html'


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login-view')

