from rest_framework import serializers
from .models import appUser

class GetappUserSerializer(serializers.ModelSerializer):
    #Getting User info
    class Meta:
        model = appUser
        exclude = ("password","last_login","is_active","is_staff","is_superuser")

    
