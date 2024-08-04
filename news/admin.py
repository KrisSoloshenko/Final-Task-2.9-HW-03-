from django.contrib import admin
from .models import Post, Category, PostCategory, Subscriber


admin.site.register(Post)
admin.site.register(Category)
admin.site.register(PostCategory)
admin.site.register(Subscriber)

