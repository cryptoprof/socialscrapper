from django.contrib import admin
from .models import VkPosts
# Register your models here.
class VkPostsAdmin(admin.ModelAdmin):
    list_display = ('post_date', 'text', 'likes', 'comments', 'reposts', 'views')
admin.site.register(VkPosts,VkPostsAdmin)