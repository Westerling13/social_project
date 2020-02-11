from django.urls import path

from .views import IndexView, StoriesListView, SignUpView, SignInView, SignOutView, UsersListView, StoryAddView, \
    StoryView, profile_view, SettingsView, StoryEditView, story_delete

urlpatterns = [
    path('', IndexView.as_view(), name='index'),

    path('sign_up', SignUpView.as_view(), name='sign_up'),
    path('sign_in', SignInView.as_view(), name='sign_in'),
    path('sign_out', SignOutView.as_view(), name='sign_out'),
    path('settings', SettingsView.as_view(), name='settings'),

    path('users/', UsersListView.as_view(), name='users'),
    path('users/@<slug:username>', profile_view, name='profile'),

    path('stories/', StoriesListView.as_view(), name='stories'),
    path('stories/add', StoryAddView.as_view(), name='story_add'),
    path('stories/<int:pk>-<str:slug>', StoryView.as_view(), name='story'),
    path('stories/<int:pk>-<str:slug>/edit', StoryEditView.as_view(), name='story_edit'),
    path('stories/<int:pk>-<str:slug>/delete', story_delete, name='story_delete')
]
