from django.contrib import admin
from .models import Category, Location, Post

admin.site.site_header = 'Администрирование Блогикума'
admin.site.index_title = 'Управление контентом'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'is_published', 'created_at')
    list_editable = ('is_published',)
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_published', 'created_at')
    list_editable = ('is_published',)
    search_fields = ('name',)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'author', 'category', 'pub_date',
        'is_published', 'created_at'
    )
    list_editable = ('is_published',)
    list_filter = ('category', 'location', 'author', 'is_published')
    search_fields = ('title', 'text')
    date_hierarchy = 'pub_date'
