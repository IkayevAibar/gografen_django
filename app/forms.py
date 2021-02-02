from django import forms
from .models import Comment, HomeWork, Vector, appUser,Course,Lesson,School
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django.contrib.auth.models import Group,Permission
from django.core.exceptions import ValidationError

def validate_gografen(value): 
        if ".gografen.com" in value: 
            return value 
        else: 
            raise ValidationError("This field should have gogafen.com")

class SchoolSettingsChangeForm(forms.ModelForm):
    school_name = forms.CharField(max_length=100)
    sub_domen = forms.URLField(max_length=30,validators=[validate_gografen])
    school_logo_1 = forms.FileField()
    school_logo_2 = forms.FileField()
    
    class Meta:
        model=School 
        fields = ('school_name', 'sub_domen', 'school_logo_1','school_logo_2')

class CourseAddForm(forms.ModelForm):
    class Meta:
        model=Course 
        fields = ('title', 'cost', 'poster','mini_poster','short_desc', 'full_desc','end_date','vector_id')

class VectorAddForm(forms.ModelForm):
    class Meta:
        model=Vector 
        fields = ('title','short_desc', 'creator_id')

class HomeworkAddForm(forms.ModelForm):
    class Meta:
        model=HomeWork 
        fields = ('title','desc', 'files')



class LessonAddForm(forms.ModelForm):
    class Meta:
        model=Lesson 
        fields = ('title', 'files','short_desc', 'full_desc','duration','teacher_id','course_id')

class CommentAddForm(forms.ModelForm):
    class Meta:
        model=Comment 
        fields = ('content','user_id','course_id')

class LessonEditForm(forms.ModelForm):
    pass

class appUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30,error_messages={'name_length':"Слишком длинное имя"})
    email = forms.EmailField(error_messages={'email_exists':'Email exists'})
    phone = forms.CharField(max_length=20)
    
    class Meta:
        model=appUser 
        fields = ('username', 'password1', 'password2','first_name','email','phone')

class GroupCreationForm(forms.ModelForm):
    permissions = forms.MultipleChoiceField(label = "Права:", choices=Permission.objects.values_list('id', 'name'), widget = forms.CheckboxSelectMultiple)
    
    class Meta:
        model=Group 
        fields = ('name','description','permissions')

class GroupChangeForm(forms.ModelForm):
    permissions = forms.MultipleChoiceField(label = "Права:", choices=Permission.objects.values_list('id', 'name'), widget = forms.CheckboxSelectMultiple)
    
    class Meta:
        model=Group 
        fields = ('name','description','permissions')
 
class appUserAddingForm(UserCreationForm):
    first_name = forms.CharField(max_length=30,error_messages={'name_length':"Слишком длинное имя"})
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField(error_messages={'email_exists':'Email exists'})
    phone = forms.CharField(max_length=20)
    role = forms.CharField(max_length=30)

    class Meta:
        model=appUser 
        fields = ('username', 'password1', 'password2', 'first_name', 'last_name', 'email', 'phone', 'role')

class appUserChangeForm(forms.ModelForm):
    class Meta:
        model=appUser 
        fields = ('first_name', 'last_name', 'phone', 'fathername','gender','birth_date','country')

