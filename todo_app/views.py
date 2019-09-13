from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import generic
from todo_app.models import Unique, MyUser, Post, Verification, CommentModel
from todo_app.forms import LoginForm, RegisterForm, PostForm, ShareForm, CommentForm
from django.views.generic import View
from django.core.paginator import Paginator
from datetime import datetime, timedelta, timezone
from .tasks import *

User = MyUser


def get_context():
    context = {}
    context['unique'] = Unique.objects.last()
    return context


class ListView(generic.CreateView, generic.ListView):
    model = CommentModel
    form_class = CommentForm
    template_name = 'index.html'
    paginate_by = 10
    success_url = '/'

    def get_queryset(self):
        qs = super(ListView, self).get_queryset()
        return qs.filter(user=self.request.user)


    def post(self, request, *args, **kwargs):
        user = self.request.POST.get('username', False)
        current_todo_id = self.request.POST.get('todo', False)
        print('----------------------',current_todo_id)
        if user and current_todo_id:
            shared_user = User.objects.get(username=user)
            shared_todo = Post.objects.get(pk=current_todo_id)
            if shared_user and shared_todo:
                shared_todo.shared_user.add(shared_user)
                return redirect(reverse_lazy('list'))
            # return redirect(reverse_lazy('list'))
        else:
            post = Post.objects.all()
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.user = request.user
                comment.post = post
                comment.save()



            return redirect('list')
    def form_valid(self, form):

        # # form.save()
        # # return super().form_valid(form)
        # form = form.save(commit=False)
        # form.user = self.request.user
        #
        # return super().form_valid(form)

        instance = form.save(commit=False)
        instance.user = self.request.user
        instance.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        self.request.POST.get("name")
        context = get_context()
        contact_list = Post.objects.filter(user=self.request.user)
        paginator = Paginator(contact_list, self.paginate_by)  # Show 25 contacts per page
        page = self.request.GET.get('page')
        todo_list = paginator.get_page(page)
        context['todo_list'] = todo_list
        context['share_form'] = ShareForm()
        context['comment_form'] = CommentForm()
        context['comment_model'] = CommentModel.objects.all()
        return context

    @method_decorator(login_required(login_url="/login"))
    def dispatch(self, request, *args, **kwargs):
        return super(ListView, self).dispatch(request, *args, **kwargs)


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
    form_class = PostForm
    template_name = 'post-add.html'
    success_url = '/'

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = self.request.user
        instance.save()
        return super().form_valid(form)


    def get_context_data(self, **kwargs):
        context = get_context()
        context['add_post'] = PostForm()
        return context


class Notification(generic.View):

    def get(self, request):
        warning_email.delay()
        return HttpResponse("ok")


class ShareListView(generic.CreateView):
    template_name = 'sharelist.html'
    model = Post

    def get_context_data(self, **kwargs):
        context = get_context()
        context['todo_share_list'] = Post.objects.all()

