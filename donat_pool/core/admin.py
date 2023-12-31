from django.contrib import admin
from .models import (
    Category, 
    Tag,
    SiteSettings,
    Feedback,
    UnwantedWord
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

class FeedbackAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'contact',
        'processed',
        'created_at',
        )
    
class UnwantedWordAdmin(admin.ModelAdmin):
    search_fields = ['word',]

admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(SiteSettings, SiteSettingsAdmin)
admin.site.register(Feedback, FeedbackAdmin)
admin.site.register(UnwantedWord, UnwantedWordAdmin)
