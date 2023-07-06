from django.contrib import admin
from .models import Author, Fundraising, CompletedFundraising

class TagInline(admin.StackedInline):
    model = Fundraising.tags.through

class AuthorInline(admin.TabularInline):
    model = Author

class FundraisingInline(admin.TabularInline):
    model = Fundraising
    readonly_fields = ["path",]

class CompletedFundraisingInline(admin.TabularInline):
    model = CompletedFundraising
    readonly_fields = ["targetAmount", "raisedAmount"]
    
class AuthorAdmin(admin.ModelAdmin):
    readonly_fields = ["address",]
    list_display = (
        'trusted', 
        'untrustworthy', 
        'created_at',
        )
    inlines = [FundraisingInline]
    search_fields = ['pkh',]

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

admin.site.register(Author, AuthorAdmin)
admin.site.register(Fundraising, FundraisingAdmin)
admin.site.register(CompletedFundraising, CompletedFundraisingAdmin)
