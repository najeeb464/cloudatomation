from rest_framework import serializers
from aws.models import AccountConfiguration
from aws.service import AwsService
class AccountConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model=AccountConfiguration
        fields=['id','profile_name','region_name','available_profiles',"access_key","secret_access_key"]
    
    def validate(self, attrs):
        attrs=super().validate(attrs)
        access_key=attrs.get('access_key')
        secret_access_key=attrs.get('secret_access_key')
        service=AwsService(access_key=access_key,secret_access_key=secret_access_key)
        attrs["profile_name"]=service.profile_name
        attrs["region_name"]=service.region_name
        return attrs


class UserProfileSerilizers(serializers.Serializer):
    UserId=serializers.CharField()
    UserName=serializers.CharField()
    Arn=serializers.CharField()
    CreateDate=serializers.DateTimeField()

class S3Serializer(serializers.Serializer):
    Name=serializers.CharField()
    CreationDate=serializers.DateTimeField()