from django.contrib import admin

from .models import UserOrig, Picture


class PictureInLine(admin.StackedInline):
    model = Picture
    extra = 3


class UserAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['email']}),
        (None, {'fields': ['files_directory']}),
    ]
    inlines = [PictureInLine]
    list_display = ('email', 'files_directory')
    search_fields = ['email']

class PictureAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['owner']}),
        (None, {'fields': ['file_name']}),
    ]
    list_display = ('owner', 'file_name')

admin.site.register(Picture, PictureAdmin)
