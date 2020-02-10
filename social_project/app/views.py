from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, CreateView, DetailView

from .forms import SignUpForm, StoryAddForm
from .models import Story, Profile


class IndexView(View):
    def get(self, request):
        context = {}
        return render(request, 'index.html', context=context)


class UsersListView(LoginRequiredMixin, ListView):
    login_url = 'sign_in'
    model = Profile
    template_name = 'users.html'
    context_object_name = 'users_list'


class StoryView(LoginRequiredMixin, DetailView):
    login_url = 'sign_in'
    model = Story
    template_name = 'story.html'
    context_object_name = 'story'


class StoriesListView(LoginRequiredMixin, ListView):
    login_url = 'sign_in'
    model = Story
    template_name = 'stories.html'
    context_object_name = 'stories_list'


class StoryAddView(LoginRequiredMixin, CreateView):
    login_url = 'sign_in'
    form_class = StoryAddForm
    template_name = 'story_add.html'

    def form_valid(self, form):
        story = form.save(commit=False)
        story.author = self.request.user
        story.save()
        return redirect('stories')


class SignUpView(CreateView):
    template_name = 'sign_up.html'
    form_class = SignUpForm

    def form_valid(self, form):
        user = form.save()
        user.refresh_from_db()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return redirect('index')


class SignInView(LoginView):
    template_name = 'sign_in.html'


class SignOutView(LogoutView):
    template_name = 'sign_out.html'