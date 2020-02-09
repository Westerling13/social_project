from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View
from django.views.generic import ListView

from .models import Story


class IndexView(View):
    def get(self, request):
        context = {}
        return render(request, 'index.html', context=context)


class StoriesListView(LoginRequiredMixin, ListView):
    login_url = 'sign_in'
    model = Story
    template_name = 'stories.html'
    context_object_name = 'stories_list'
