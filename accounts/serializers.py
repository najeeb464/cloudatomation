
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import serializers
# from django.contrib.auth.models import User
from accounts.models import User
from aws.models import AccountConfiguration
class SignInSerializer(serializers.ModelSerializer):
    email               =serializers.EmailField(required=True)
    password            =serializers.CharField(required=True,write_only=True)
    access              =serializers.CharField(read_only=True)
    refresh             =serializers.CharField(read_only=True)
    # configure_account=serializers.DictField(child=serializers.CharField(),read_only=True)


    class Meta:
        model=User
        fields=['email','name','password','access','refresh']
        extra_kwargs = {
        'name': {'read_only': True},
        }
    def validate(self, attrs):
        print("attrs",attrs)
        attrs=super().validate(attrs)
        try:
            user_Obj=User.objects.get(email=attrs['email'])
        except User.DoesNotExist:
            raise serializers.ValidationError({"user":"Provided credentional are not valid"})
        except User.MultipleObjectsReturned:
            raise serializers.ValidationError({"user":"Provided credentional are not valid"})
        if user_Obj and user_Obj.check_password(attrs.get('password')):
            if user_Obj.is_active:
                token=RefreshToken.for_user(user_Obj)
                # ac=AccountConfiguration.objects.all().first()
                
                # data={}
                # if ac:
                #     data["aws_user"]=ac.user_name
                #     data["aws_id"]=ac.id
                attrs['access']=str(token.access_token)
                attrs['refresh']=str(token)
                attrs['name']=user_Obj.name
                # attrs["configure_account"]=data
                return attrs
            else:
                raise serializers.ValidationError({"user":"Your account status is Inactive"})
        else:
            raise serializers.ValidationError({"user":"Provided credentionals are not valid"})
        return super().validate(attrs)


class SignUpSerializer(serializers.ModelSerializer):
    email               =serializers.EmailField(required=True)
    password            =serializers.CharField(required=True,write_only=True)
    class Meta:
        model=User
        fields=['email','name','password']
        
    def validate(self, attrs):
        if User.objects.filter(email__exact=attrs['email']).exists():
            raise serializers.ValidationError({"user":"account already exists with this username"})
        return super().validate(attrs)
    def create(self, validated_data):
        print("validated_data",validated_data)
        user_password=validated_data.pop('password')
        user=User(**validated_data)
        user.set_password(user_password)
        user.is_active=True
        user.save()
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=["email","name","is_active"]