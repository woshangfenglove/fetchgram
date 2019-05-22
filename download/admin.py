from django.contrib import admin
from . import models


@admin.register(models.PostModel)
class PostAdmin(admin.ModelAdmin):
    fields = ['post_url']
    list_display = ('post_url', 'id', 'date_time')
