from django.contrib import admin
from .models import (
    Category, 
    Tag,
    SiteSettings,
)

class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        )
    search_fields = ['name',]

class TagAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        )
    search_fields = ['name',]

class CategoryInline(admin.TabularInline):
    model = Category

class TagInline(admin.TabularInline):
    model = Tag

class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = (
        'name',
    )
    inlines = [
        CategoryInline,
        TagInline,
    ]

admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(SiteSettings, SiteSettingsAdmin)
