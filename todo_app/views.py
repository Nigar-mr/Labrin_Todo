from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import generic
from todo_app.models import Unique, MyUser, Post, AddList, Verification
from todo_app.forms import LoginForm, RegisterForm, PostForm, AddListForm
from django.views.generic import View
from datetime import datetime, timedelta, timezone
from .tasks import *
User = MyUser

def get_context():
    context = {}
    context['unique'] = Unique.objects.last()
    return context


class ListView(generic.CreateView):
    model = AddList
    form_class = AddListForm
    template_name = 'index.html'
    success_url = '/list'

    def get_context_data(self, **kwargs):
        context = get_context()
        context['todo_list'] = Post.objects.all()
        context['add_list'] = AddListForm()
        context['list'] = AddList.objects.all()
        return context

class RegisterView(generic.CreateView):
    form_class = RegisterForm
    template_name = 'register.html'
    success_url = '/login'


    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()
        return redirect('list')

    def form_invalid(self, form):
        return redirect('register')



    def get_context_data(self, **kwargs):
        context = {}
        context['register_form'] = RegisterForm()
        return context


class AuthLoginView(LoginView):
    template_name = 'login.html'

    def get_context_data(self, **kwargs):
        context = {}
        context['login_form'] = LoginForm()
        return context

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('list')

class AddView(generic.CreateView):
    model = Post
    fields = ['name', 'more', 'datetime']
    template_name = 'post-add.html'
    success_url = '/'

    def form_valid(self, form):
        self.object = form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = get_context()
        context['add_post'] = PostForm()
        return context

#
# class SendEmail(generic.View):
#     now = datetime.now(timezone.utc)
#     post = Post.objects.all()
#     for post in post:
#         pass
#
#     def get(self, request):
#         notification.delay
#         return HttpResponse("ok")


# def SendEmail(request):
#     now = datetime.now(timezone.utc)
#     post = Post.objects.all()
#     user = MyUser.objects.all()
#     for post in post:
#         if post.datetime - now > timedelta(seconds=-600):
#             token = Verification.objects.create(
#                 post=post
#             )
#             warning_email.delay(user.email, token.get_verify_url())
#             return redirect('list')
#         else:
#             return messages.success("Please view your email")
#

class Notification(generic.View):

    def get(self, request):
        warning_email.delay()
        return HttpResponse("ok")

