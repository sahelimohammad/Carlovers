from django.contrib import admin
from .models import Relation , Profile 
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

class ProfileInline (admin.TabularInline):
    model = Profile
    can_delete = False

class ExtendedUserAdmin(UserAdmin):
    inlines = (ProfileInline,)

admin.site.register(Relation) 
admin.site.unregister(User)
admin.site.register(User , ExtendedUserAdmin) 

