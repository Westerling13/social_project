from django.contrib import admin

from .models import Profile, Story, Comment

admin.site.register(Profile)
admin.site.register(Story)
admin.site.register(Comment)

