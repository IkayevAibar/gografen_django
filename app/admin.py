from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext, gettext_lazy as _

class CourseInline(admin.TabularInline):
    model = Course

class appUserAdmin(UserAdmin):
    raw_id_fields=["school_id"]
    # autocomplete_fields=["school_id"]
    list_display = ('username','id', 'email','phone', 'first_name', 'last_name', 'is_staff',"school_id")
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'fathername', 'email')}),
        (_('Additional info'), {'fields': ('gender', 'phone' ,'birth_date','card','position','country','subdivison','lead_activity','client_activity',"school_id")}),
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
    list_display = ('title','id', 'cost','short_desc', 'start_date', 'end_date','duration','pub_date','creator_id')
    fieldsets = (
        (None, {'fields': ('id', 'creator_id')}),
        (_('Информация'), {'fields': ('title', 'cost', 'short_desc','full_desc','duration','lesson_count','poster','mini_poster')}),
        # (_('Additional info'), {'fields': ('gender', 'phone' ,'birth_date','card','position','country','subdivison','lead_activity','client_activity')}),
        # (_('Permissions'), {
        #     'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        # }),
        (_('Important dates'), {'fields': ('start_date', 'end_date','pub_date')}),
    )

class SchoolAdmin(admin.ModelAdmin):
    # autocomplete_fields=["creator_id"]
    # raw_id_fields=["creator_id"]
    # wrapper_kwargs={""}
    readonly_fields = ('id',)
    list_display = ('school_name','id', 'sub_domen','creator_id')
    fieldsets = (
        (None, {'fields': ('id', 'school_name', 'creator_id')}),
        (_('Информация'), {'fields': ( 'sub_domen', 'school_logo_1','school_logo_2')}),
    )



admin.site.register(appUser,appUserAdmin)
admin.site.register(Course,CourseAdmin)
admin.site.register(Lesson)
admin.site.register(School,SchoolAdmin)

# Register your models here.
