from django.contrib import admin
from .models import Post, Comment, ImagePost

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(ImagePost)
