from django.contrib import admin
from .models import PostModel


@admin.register(PostModel)
class PostAdmin(admin.ModelAdmin):
    fields = ['post_url']
    list_display = ('post_url', 'id', 'date_time')
