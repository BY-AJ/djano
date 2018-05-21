from django.contrib import admin
from .models import UserProfile

# Register your models here.
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user","phone","birth")
    list_filter = ("phone",)
    search_fields = ("user","phone")
admin.site.register(UserProfile,UserProfileAdmin)    