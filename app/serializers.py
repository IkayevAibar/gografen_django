from rest_framework import serializers
from .models import appUser

class GetappUserSerializer(serializers.ModelSerializer):
    #Getting User info
    class Meta:
        model = appUser
        exclude = ("password","last_login","is_active","is_staff","is_superuser","groups","user_permissions")


class GetappUserPublicSerializer(serializers.ModelSerializer):
    #Getting public User info
    class Meta:
        model = appUser
        exclude = ("password","phone","email","groups","user_permissions","last_login","is_active","is_staff","is_superuser")

    
