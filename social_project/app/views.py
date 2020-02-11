from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView, CreateView, DetailView, UpdateView

from .forms import SignUpForm, StoryAddForm, SettingsForm, CommentForm
from .models import Story, Profile, Comment


def index(request):
    return render(request, 'index.html')


@login_required(login_url='sign_in')
def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user)
    stories = Story.objects.filter(author=user)
    context = {
        'profile': profile,
        'usr': user,
        'is_me': user == request.user,
        'stories': stories
    }
    return render(request, 'profile.html', context=context)


class UsersListView(LoginRequiredMixin, ListView):
    login_url = 'sign_in'
    model = Profile
    template_name = 'users.html'
    context_object_name = 'users_list'

    def get_queryset(self):
        return Profile.objects.order_by('-user__last_login')


# class StoryView(LoginRequiredMixin, DetailView, CreateView):
#     login_url = 'sign_in'
#     model = Story
#     template_name = 'story.html'
#     context_object_name = 'story'
#
#     form_class = CommentForm

class StoryView(LoginRequiredMixin, View):
    def get(self, request, **kwargs):
        story = get_object_or_404(Story, pk=kwargs.get('pk'))
        form = CommentForm()
        comments = Comment.objects.filter(story=story)

        return render(request, 'story.html', context={'story': story, 'form': form, 'comments': comments})

    def post(self, request, **kwargs):
        form = CommentForm(request.POST)
        story = get_object_or_404(Story, pk=kwargs.get('pk'))
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.story = story
            comment.save()
            return redirect('story', pk=kwargs.get('pk'), slug=kwargs.get('slug'))


class StoryEditView(LoginRequiredMixin, UpdateView):
    login_url = 'sign_in'
    model = Story
    template_name = 'story_edit.html'
    fields = ['title', 'as_md', 'text', 'published']

    def get(self, *args, **kwargs):
        user = self.request.user
        pk = kwargs.get('pk')
        author = Story.objects.get(pk=pk).author
        if not user.is_superuser and user != author:
            raise PermissionDenied
        return super().get(*args, **kwargs)


@login_required(login_url='sign_in')
def story_delete(request, **kwargs):
    story = get_object_or_404(Story, pk=kwargs.get('pk'))
    if not request.user.is_superuser and request.user != story.author:
        raise PermissionDenied
    story.delete()
    return redirect('stories')


class StoriesListView(LoginRequiredMixin, ListView):
    login_url = 'sign_in'
    model = Story
    template_name = 'stories.html'
    context_object_name = 'stories_list'

    def get_queryset(self):
        return Story.objects.filter(published=True)


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
        print(user)
        print(user.profile)
        user.profile.first_name = form.cleaned_data.get('first_name')
        user.profile.last_name = form.cleaned_data.get('last_name')
        user.profile.email = form.cleaned_data.get('email')
        user.profile.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return redirect('index')


class SignInView(LoginView):
    template_name = 'sign_in.html'


class SignOutView(LogoutView):
    template_name = 'sign_out.html'


class SettingsView(View):
    def get(self, request):
        profile = get_object_or_404(Profile, user=request.user)
        form = SettingsForm(instance=profile)
        return render(request, 'profile_edit.html', context={'form': form})

    def post(self, request):
        profile = get_object_or_404(Profile, user=request.user)
        form = SettingsForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile', username=request.user.username)
