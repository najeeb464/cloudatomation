from django.shortcuts import render

# Create your views here.
from rest_framework.viewsets import ModelViewSet
from aws.serializers import (
    AccountConfigurationSerializer,
    UserProfileSerilizers,S3Serializer,
    S3Serializer)

from aws.models import AccountConfiguration
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from aws.service import AwsService
class AccountConfigurationView(ModelViewSet):
    queryset=AccountConfiguration.objects.all().order_by("-id")
    serializer_class=AccountConfigurationSerializer


class UserProfileView(APIView):
    def get(self, request):
        items = AccountConfiguration.objects.all()
        data=[]
        for item in items:
            s=AwsService(access_key=item.access_key,secret_access_key=item.secret_access_key)
            data.append({"profile_name":item.profile_name,
                "users":s.list_user_account()['Users']})
        return Response(data)


class S3ListView(APIView):
    def get(self, request):
        items = AccountConfiguration.objects.all()
        data=[]
        for item in items:
            s=AwsService(access_key=item.access_key,secret_access_key=item.secret_access_key)
            data.append({"profile_name":item.profile_name,
                "users":s.list_s3()})
        return Response(data)


class S3ObjectListView(APIView):
    def get(self, request,*args,**kwargs):
        bucket_name=kwargs.get("bucket_name",None)

        items = AccountConfiguration.objects.all()
        data=[]
        for item in items:
            s=AwsService(access_key=item.access_key,secret_access_key=item.secret_access_key)
            data.append({"profile_name":item.profile_name,
                "bucket_objects":s.S3_bucket_objects_detail(bucket_name)})
        return Response(data)

class RDSListView(APIView):
    def get(self, request,*args,**kwargs):
        items = AccountConfiguration.objects.all()
        data=[]
        for item in items:
            s=AwsService(access_key=item.access_key,secret_access_key=item.secret_access_key,region_name="us-east-1")
            data.append({"profile_name":item.profile_name,
                "rds_list":s.list_rds()})
        return Response(data)
class RDSDetailView(APIView):
    def get(self, request,*args,**kwargs):
        instance_arn=kwargs.get("instance_arn",None)
        items = AccountConfiguration.objects.all()
        data=[]
        for item in items:
            s=AwsService(access_key=item.access_key,secret_access_key=item.secret_access_key,region_name="us-east-1")
            data.append({"profile_name":item.profile_name,
                "rds_list":s.rds_detail(instance_arn=instance_arn)})
        return Response(data)
        
