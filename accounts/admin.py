from django.contrib import admin

from .models import UserProfile, Organization

@admin.register(UserProfile)
class AdminUserProfile(admin.ModelAdmin):
    list_display = ('user', 'biography', 'photo')

@admin.register(Organization)
class AdminOrganization(admin.ModelAdmin):
    list_display = ('name',)
