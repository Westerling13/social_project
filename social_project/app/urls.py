from django.urls import path

from .views import IndexView, StoriesListView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('stories/', StoriesListView.as_view(), name='stories'),
]
