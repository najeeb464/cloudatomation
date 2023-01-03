from rest_framework import serializers
from aws.models import AccountConfiguration
from aws.service import AwsService



class AccountConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model=AccountConfiguration
        fields=['id','user_name','region_name','arn',"user_id","access_key","secret_access_key","is_default"]
    
    def validate(self, attrs):
        print("attrs",attrs)
        is_default=attrs.get("is_default",False)
        qs=AccountConfiguration.objects.all()
        if qs.exists():
            qs=qs.filter(is_default=True)
            if qs.exists():
                if is_default==True:
                    for i in qs:
                        i.is_default=False
                        i.save()
            else:
                attrs["is_default"]=True
                
        else:
            attrs["is_default"]=True
        # if accountObj:
        attrs=super().validate(attrs)
        access_key=attrs.get('access_key')
        secret_access_key=attrs.get('secret_access_key')
        # service=AwsService(access_key=access_key,secret_access_key=secret_access_key)
        # user=service.get_user_detail()
        # attrs["user_name"]=user.get("user_name","")
        # attrs["arn"]=user.get("arn","")
        # attrs["user_id"]=user.get("user_id","")
        return attrs


class UserProfileSerilizers(serializers.Serializer):
    UserId=serializers.CharField()
    UserName=serializers.CharField()
    Arn=serializers.CharField()
    CreateDate=serializers.DateTimeField()

class S3Serializer(serializers.Serializer):
    Name=serializers.CharField()
    CreationDate=serializers.DateTimeField()