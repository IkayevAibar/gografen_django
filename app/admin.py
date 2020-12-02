from django.contrib import admin
from .models import appUser,Course
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext, gettext_lazy as _

class CourseInline(admin.TabularInline):
    model = Course

class appUserAdmin(UserAdmin):
    list_display = ('username','id', 'email','phone', 'first_name', 'last_name', 'is_staff')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'fathername', 'email')}),
        (_('Additional info'), {'fields': ('gender', 'phone' ,'birth_date','card','position','country','subdivison','lead_activity','client_activity')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    # inlines = [CourseInline,]


class CourseAdmin(admin.ModelAdmin):
    # autocomplete_fields=["creator_id"]
    raw_id_fields=["creator_id"]
    wrapper_kwargs={""}
    readonly_fields = ('id',)
    list_display = ('title','id', 'cost','short_desc', 'start_date', 'end_date', 'course_programm','duration','pub_date','creator_id')
    fieldsets = (
        (None, {'fields': ('id', 'creator_id')}),
        (_('Информация'), {'fields': ('title', 'cost', 'short_desc', 'course_programm','duration')}),
        # (_('Additional info'), {'fields': ('gender', 'phone' ,'birth_date','card','position','country','subdivison','lead_activity','client_activity')}),
        # (_('Permissions'), {
        #     'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        # }),
        (_('Important dates'), {'fields': ('start_date', 'end_date','pub_date')}),
    )
   


admin.site.register(appUser,appUserAdmin)
admin.site.register(Course,CourseAdmin)

# Register your models here.
