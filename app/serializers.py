from rest_framework import serializers
from .models import appUser

class GetappUserSerializer(serializers.ModelSerializer):
    #Getting User info
    class Meta:
        model = appUser
        exclude = ("password","last_login","is_active","is_staff","is_superuser","groups","user_permissions","sub_domen","school_logo_1","school_logo_2")


class GetappUserPublicSerializer(serializers.ModelSerializer):
    #Getting public User info
    class Meta:
        model = appUser
        exclude = ("password","phone","email","groups","user_permissions","last_login","is_active","is_staff","is_superuser","sub_domen","school_logo_1","school_logo_2")

class CreateappUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    #Getting User info
    class Meta:
        model = appUser
        exclude = ("client_activity","lead_activity","last_login","is_active","is_staff","is_superuser","groups","user_permissions","school_name","sub_domen","school_logo_1","school_logo_2")
    def create(self, validated_data):
        user = super(CreateappUserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
