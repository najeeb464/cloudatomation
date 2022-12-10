from rest_framework import serializers
from aws.models import AccountConfiguration
from aws.service import AwsService


# Access 
# AKIAUXMC7CKZO7ZV6L7M
#Secret
#Xx19wVH70rYHKnWRNMUlHFSXR413O7QDADJLXD7r
class AccountConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model=AccountConfiguration
        fields=['id','user_name','region_name','arn',"user_id","access_key","secret_access_key"]
    
    def validate(self, attrs):
        attrs=super().validate(attrs)
        access_key=attrs.get('access_key')
        secret_access_key=attrs.get('secret_access_key')
        service=AwsService(access_key=access_key,secret_access_key=secret_access_key)
        user=service.get_user_detail()
        attrs["user_name"]=user.get("user_name","")
        attrs["arn"]=user.get("arn","")
        attrs["user_id"]=user.get("user_id","")
        # attrs["region_name"]=user.region_name
        return attrs


class UserProfileSerilizers(serializers.Serializer):
    UserId=serializers.CharField()
    UserName=serializers.CharField()
    Arn=serializers.CharField()
    CreateDate=serializers.DateTimeField()

class S3Serializer(serializers.Serializer):
    Name=serializers.CharField()
    CreationDate=serializers.DateTimeField()