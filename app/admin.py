from django.contrib import admin
from .models import appUser
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext, gettext_lazy as _

class appUserAdmin(UserAdmin):
    list_display = ('username', 'email','phone', 'first_name', 'last_name', 'is_staff')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'fathername', 'email')}),
        (_('Additional info'), {'fields': ('gender', 'phone' ,'birth_date','card','position','country','subdivison','lead_activity','client_activity')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

admin.site.register(appUser,appUserAdmin)

# Register your models here.
