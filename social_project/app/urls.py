from django.urls import path

from .views import IndexView, StoriesListView, SignUpView, SignInView, SignOutView, UsersListView, StoryAddView, StoryView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),

    path('users/', UsersListView.as_view(), name='users'),
    path('users/sign_up', SignUpView.as_view(), name='sign_up'),
    path('users/sign_in', SignInView.as_view(), name='sign_in'),
    path('users/sign_out', SignOutView.as_view(), name='sign_out'),

    path('stories/', StoriesListView.as_view(), name='stories'),
    path('stories/add', StoryAddView.as_view(), name='story_add'),
    path('stories/<int:pk>-<str:slug>', StoryView.as_view(), name='story'),
]
