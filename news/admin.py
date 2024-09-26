from django.contrib import admin
from .models import Post, Category, PostCategory, Subscriber


def nullfy_rating(modeladmin, request, queryset):
    queryset.update(rating=0)
nullfy_rating.short_description = 'Обнулить рейтинг'


class PostAdmin(admin.ModelAdmin):
    list_display = ('pk', 'heading', 'type', 'rating')
    list_filter = ('rating', 'category')
    search_fields = ('heading', 'category__category_name')
    actions = [nullfy_rating]
    
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'category_name')
    

class PostCategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'post', 'category')
    

class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'category')


admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(PostCategory, PostCategoryAdmin)
admin.site.register(Subscriber, SubscriberAdmin)

