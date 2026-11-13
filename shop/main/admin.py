from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'first_name', 'last_name', 'birth_date', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('id',)
