from django.contrib import admin
from .models import Profile, Follow, Post

# Register your models here.
admin.site.register(Profile)
admin.site.register(Follow)
admin.site.register(Post)