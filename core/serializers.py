from .models import MyUser
from rest_framework import serializers
from django.conf import settings
import logging
logger = logging.getLogger(__name__)


class UserBasicInfoSerializer(serializers.ModelSerializer):
    profile_pic = serializers.SerializerMethodField()
    full_name = serializers.SerializerMethodField()

    def get_full_name(self, obj):
        if obj.last_name:
            return "%s %s"%(obj.first_name, obj.last_name)
        return obj.first_name


    def get_profile_pic(self, obj):
        return "%s%s"%(settings.STATIC_URL,obj.profile_pic)
    class Meta:
        model = MyUser
        fields = ('first_name','profile_pic', 'user_id','username', 'full_name')
