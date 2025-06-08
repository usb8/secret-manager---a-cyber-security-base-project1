from django.contrib import admin
from .models import Secret


@admin.register(Secret)
class SecretAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at')
    list_filter = ('user', 'created_at')
    search_fields = ('title', 'content')
