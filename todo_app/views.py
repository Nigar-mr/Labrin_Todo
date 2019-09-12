from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from todo_app.models import Unique, MyUser, Post, Verification
from todo_app.forms import LoginForm, RegisterForm, PostForm, ShareForm
from django.views.generic import View
from datetime import datetime, timedelta, timezone
from .tasks import *

User = MyUser


def get_context():
    context = {}
    context['unique'] = Unique.objects.last()
    return context


class ListView(generic.CreateView):
    template_name = 'index.html'
    success_url = '/'

    # ordering = ['-publish_date']

    def post(self, request, *args, **kwargs):
        user = self.request.POST.get('username', False)
        current_todo_id = self.request.POST.get('todo', False)
        print(current_todo_id)
        if user and current_todo_id:
            shared_user = User.objects.get(username=user)
            shared_todo = Post.objects.get(pk=current_todo_id)
            if shared_user and shared_todo:
                shared_todo.shared_user.add(shared_user)
                return redirect(reverse_lazy('list'))

    def get_context_data(self, **kwargs):
        self.request.POST.get("name")
        context = get_context()
        context['todo_list'] = Post.objects.all()
        context['share_form'] = ShareForm()
        return context


class PostDeleteView(generic.DeleteView):
    model = Post
    template_name = 'index.html'
    success_url = reverse_lazy('list')


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


class Notification(generic.View):

    def get(self, request):
        warning_email.delay()
        return HttpResponse("ok")