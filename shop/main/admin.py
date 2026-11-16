from django.contrib import admin

from .models import Mod, Tag, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'first_name', 'last_name', 'birth_date', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('id',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    search_fields = ('name', 'slug')
    ordering = ('name',)


@admin.register(Mod)
class ModAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug', 'category', 'mc_version', 'downloads')
    list_filter = ('category', 'tags')
    search_fields = ('name', 'slug', 'description')
    filter_horizontal = ('tags',)
    ordering = ('id',)
