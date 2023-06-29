from django.contrib import admin
from .models import Author, Category, Fundraising, CompletedFundraising, Tag


class AuthorInline(admin.TabularInline):
    model = Author

class CategoryInline(admin.TabularInline):
    model = Category

class TagInline(admin.StackedInline):
    model = Fundraising.tags.through

class FundraisingInline(admin.TabularInline):
    model = Fundraising
    readonly_fields = ["path",]

class CompletedFundraisingInline(admin.TabularInline):
    model = CompletedFundraising
    readonly_fields = ["targetAmount", "raisedAmount"]
    
class AuthorAdmin(admin.ModelAdmin):
    readonly_fields = ["pkh",]
    list_display = (
        'trusted', 
        'untrustworthy', 
        'created_at',
        )
    inlines = [FundraisingInline]
    search_fields = ['pkh',]
    

class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        )
    search_fields = ['name',]

class FundraisingAdmin(admin.ModelAdmin):
    readonly_fields = ["path",]
    list_display = (
        'created_at',
        'category',
        'verified',
        'promoted',
        'main',
        )
    inlines = [TagInline, CompletedFundraisingInline]
    search_fields = ['path',]

class CompletedFundraisingAdmin(admin.ModelAdmin):
    list_display = (
        'completedAt',
        'targetAmount',
        'raisedAmount',
        )
    search_fields = ['fundraising__path',]


class TagAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        )
    search_fields = ['name',]

admin.site.register(Author, AuthorAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Fundraising, FundraisingAdmin)
admin.site.register(CompletedFundraising, CompletedFundraisingAdmin)
admin.site.register(Tag, TagAdmin)
