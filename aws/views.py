from django.shortcuts import render

# Create your views here.
from rest_framework.viewsets import ModelViewSet
from aws.serializers import (
    AccountConfigurationSerializer,
    UserProfileSerilizers,S3Serializer,
    S3Serializer)

from aws.models import AccountConfiguration
from rest_framework.response import Response
from rest_framework import status

from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from aws.service import AwsService

from rest_framework.permissions import IsAuthenticated,AllowAny

class AccountConfigurationView(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset=AccountConfiguration.objects.all().order_by("-id")
    serializer_class=AccountConfigurationSerializer
    def destroy(self, request, *args, **kwargs):
        obj=self.get_queryset()
        if len(obj)<=1:
            return Response({"detail":"You must atleast one account configure"},status=status.HTTP_400_BAD_REQUEST)

        instance = self.get_object()
        if instance.is_default==True:
            return Response({"detail":"You must atleast one default  acoount"},status=status.HTTP_400_BAD_REQUEST)
        self.perform_destroy(instance)
        # qs=AccountConfiguration.objects.all()
        # print("qs",qs)
        
        # if qs.count()==1:
        #     qs.first().is_default=True
        #     qs.first().save()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ChangeAccountStatus(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,*args,**kwargs):
        account_id=self.kwargs.get("account_id")
        try:
            qs=AccountConfiguration.objects.all()
            for i in qs:
                i.is_default=False
                i.save()
            ac=AccountConfiguration.objects.get(id=account_id)
            ac.is_default=True
            ac.save()
            return Response({},status=status.HTTP_200_OK)
        except:
            return Response({"error":"Invalid Account Configure"},status=status.HTTP_400_BAD_REQUEST)


class AccountStatus(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        qs=AccountConfiguration.objects.all()
        if qs.exists():
            flagObj=qs.filter(is_default=True)
            if flagObj.exists():
                return Response({"aws_id":flagObj.first().id,"user_id":flagObj.first().user_id,"user_name":flagObj.first().user_name},status=status.HTTP_200_OK)
            return Response({"aws_id":qs.first().id,"user_id":qs.first().user_id,"user_name":qs.first().user_name},status=status.HTTP_200_OK)

        else:
            return Response({},status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        items = AccountConfiguration.objects.all()
        data=[]
        for item in items:
            s=AwsService(access_key=item.access_key,secret_access_key=item.secret_access_key)
            data.append({"profile_name":item.profile_name,
                "users":s.list_user_account()['Users']})
        return Response(data)


class S3ListView(APIView):
    # permission_classes = [IsAuthenticated]
    permission_classes = []
    def get(self,*args,**kwargs):
        account_id=kwargs.get("account_id",None)
        try:
            item = AccountConfiguration.objects.get(id=account_id)
        except Exception as ex:
            return Response({"error":"Invalid Account Configure"},status=status.HTTP_400_BAD_REQUEST)
        data=[]
        s=AwsService(access_key=item.access_key,secret_access_key=item.secret_access_key)
        buckets_list=s.list_s3()
        data.append({"profile_name":item.user_name,
                "buckets":buckets_list,"stats":s.s3_stats(buckets_list)})
        # for item in items:
        #     s=AwsService(access_key=item.access_key,secret_access_key=item.secret_access_key)
        #     data.append({"profile_name":item.profile_name,
        #         "buckets":s.list_s3()})
        return Response(data)


class S3ObjectListView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request,*args,**kwargs):
        bucket_name=kwargs.get("bucket_name",None)
        account_id=kwargs.get("account_id",None)
        try:
            item = AccountConfiguration.objects.get(id=account_id)
        except Exception as ex:
            return Response({"error":"Invalid Account Configure"},status=status.HTTP_400_BAD_REQUEST)
        item = AccountConfiguration.objects.all()
        data=[]
        s=AwsService(access_key=item.access_key,secret_access_key=item.secret_access_key)
        data.append({"profile_name":item.user_name,
            "bucket_objects":s.S3_bucket_objects_detail(bucket_name)})
        return Response(data)

class RDSListView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request,*args,**kwargs):
        account_id=kwargs.get("account_id",None)
        try:
            item = AccountConfiguration.objects.get(id=account_id)
        except Exception as ex:
            return Response({"error":"Invalid Account Configure"},status=status.HTTP_400_BAD_REQUEST)
        data=[]
        s=AwsService(access_key=item.access_key,secret_access_key=item.secret_access_key,region_name="us-east-1")
        data.append({"profile_name":item.user_name,
            "rds_list":s.list_rds()})
        return Response(data)
class RDSDetailView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request,*args,**kwargs):
        instance_arn=kwargs.get("instance_arn",None)
        account_id=kwargs.get("account_id",None)
        try:
            item = AccountConfiguration.objects.get(id=account_id)
        except Exception as ex:
            return Response({"error":"Invalid Account Configure"},status=status.HTTP_400_BAD_REQUEST)
        data=[]
        s=AwsService(access_key=item.access_key,secret_access_key=item.secret_access_key,region_name="us-east-1")
        data.append({"profile_name":item.user_name,
            "rds_list":s.rds_detail(instance_arn=instance_arn)})
        return Response(data)
        

class EC2ListView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request,*args,**kwargs):
        account_id=kwargs.get("account_id",None)
        query_parms=dict(zip(self.request.query_params.keys(),self.request.query_params.values()))
        try:
            item = AccountConfiguration.objects.get(id=account_id)
        except Exception as ex:
            return Response({"error":"Invalid Account Configure"},status=status.HTTP_400_BAD_REQUEST)
        data=[]
        s=AwsService(access_key=item.access_key,secret_access_key=item.secret_access_key,region_name="us-east-1")
        data.append({"profile_name":item.user_name,
            "ec2_list":s.ec2_list(),"image":s.ec2_graph(filters=query_parms)})
        return Response(data)
class EC2Stop(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request,*args,**kwargs):
        account_id=kwargs.get("account_id",None)
        instance_id=kwargs.get("instance_id",None)
        try:
            item = AccountConfiguration.objects.get(id=account_id)
        except Exception as ex:
            return Response({"error":"Invalid Account Configure"},status=status.HTTP_400_BAD_REQUEST)
        data=[]
        s=AwsService(access_key=item.access_key,secret_access_key=item.secret_access_key,region_name="us-east-1")
        flag=s.stop_ec2(ec2_instance=instance_id)
        if flag:
            return Response({"flag":True},status=status.HTTP_200_OK)
        else:
            return Response({"flag":False},status=status.HTTP_400_BAD_REQUEST)

class EC2Start(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request,*args,**kwargs):
        account_id=kwargs.get("account_id",None)
        instance_id=kwargs.get("instance_id",None)
        try:
            item = AccountConfiguration.objects.get(id=account_id)
        except Exception as ex:
            return Response({"error":"Invalid Account Configure"},status=status.HTTP_400_BAD_REQUEST)
        data=[]
        s=AwsService(access_key=item.access_key,secret_access_key=item.secret_access_key,region_name="us-east-1")
        flag=s.start_ec2(ec2_instance=instance_id)
        if flag:
            return Response({"flag":True},status=status.HTTP_200_OK)
        else:
            return Response({"flag":False},status=status.HTTP_400_BAD_REQUEST)

# class EC2GraphView(APIView):
#     permission_classes = [IsAuthenticated]
#     def get(self, request,*args,**kwargs):
#         account_id=kwargs.get("account_id",None)
#         graph_type = self.request.query_params.get('graphtype',"cpu")
#         try:
#             item = AccountConfiguration.objects.get(id=account_id)
#         except Exception as ex:
#             return Response({"error":"Invalid Account Configure"},status=status.HTTP_400_BAD_REQUEST)
#         data=[]
#         s=AwsService(access_key=item.access_key,secret_access_key=item.secret_access_key,region_name="us-east-1")
#         data.append({"profile_name":item.user_name,
#         "image":s.ec2_graph(type_=graph_type)})
#         return Response(data)

# query_parms=dict(zip(self.request.query_params.keys(),self.request.query_params.values()))

class EC2GraphView(APIView):
    # permission_classes = [IsAuthenticated]
    permission_classes = []
    def get(self, request,*args,**kwargs):
        account_id=kwargs.get("account_id",None)
        query_parms=dict(zip(self.request.query_params.keys(),self.request.query_params.values()))
        graph_type = self.request.query_params.get('graphtype',"cpu")
        try:
            item = AccountConfiguration.objects.get(id=account_id)
        except Exception as ex:
            return Response({"error":"Invalid Account Configure"},status=status.HTTP_400_BAD_REQUEST)
        data=[]
        s=AwsService(access_key=item.access_key,secret_access_key=item.secret_access_key,region_name="us-east-1")
        # data.append({"profile_name":item.user_name,
        # "image":s.ec2_graph(filters=query_parms)})
        return Response([s.ec2_graph(filters=query_parms)])

class RDSGraphView(APIView):
    # permission_classes = [IsAuthenticated]
    permission_classes = []
    def get(self, request,*args,**kwargs):
        account_id=kwargs.get("account_id",None)
        query_parms=dict(zip(self.request.query_params.keys(),self.request.query_params.values()))
        graph_type = self.request.query_params.get('graphtype',"cpu")

        try:
            item = AccountConfiguration.objects.get(id=account_id)
        except Exception as ex:
            return Response({"error":"Invalid Account Configure"},status=status.HTTP_400_BAD_REQUEST)
        data=[]
        s=AwsService(access_key=item.access_key,secret_access_key=item.secret_access_key,region_name="us-east-1")
        # data.append({"profile_name":item.user_name,
        # "image":s.rds_image(filters=query_parms)})
        return Response([s.rds_image(filters=query_parms)])

class S3GraphView(APIView):
    # permission_classes = [IsAuthenticated]
    permission_classes = []
    def get(self, request,*args,**kwargs):
        account_id=kwargs.get("account_id",None)
        query_parms=dict(zip(self.request.query_params.keys(),self.request.query_params.values()))
        graph_type = self.request.query_params.get('graphtype',"cpu")

        try:
            item = AccountConfiguration.objects.get(id=account_id)
        except Exception as ex:
            return Response({"error":"Invalid Account Configure"},status=status.HTTP_400_BAD_REQUEST)
        data=[]
        s=AwsService(access_key=item.access_key,secret_access_key=item.secret_access_key,region_name="us-east-1")
        # data.append({"profile_name":item.user_name,
        # "image":s.rds_image(filters=query_parms)})
        return Response([s.s3_graph(filters=query_parms)])

class S3StatsView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request,*args,**kwargs):
        account_id=kwargs.get("account_id",None)
        try:
            item = AccountConfiguration.objects.get(id=account_id)
        except Exception as ex:
            return Response({"error":"Invalid Account Configure"},status=status.HTTP_400_BAD_REQUEST)
        data=[]
        s=AwsService(access_key=item.access_key,secret_access_key=item.secret_access_key,region_name="us-east-1")
        data.append({"profile_name":item.user_name,
        "stast":s.s3_stats()})
        return Response(data)

class EC2StateStatsView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request,*args,**kwargs):
        account_id=kwargs.get("account_id",None)
        try:
            item = AccountConfiguration.objects.get(id=account_id)
        except Exception as ex:
            return Response({"error":"Invalid Account Configure"},status=status.HTTP_400_BAD_REQUEST)
        data=[]
        s=AwsService(access_key=item.access_key,secret_access_key=item.secret_access_key,region_name="us-east-1")
        data.append({"profile_name":item.user_name,
        "stast":s.ec2_state_stats()})
        return Response(data)

class Ec2FilterChoices(APIView):
    permission_classes = []
    def get(self, request,*args,**kwargs):
        account_id=kwargs.get("account_id",None)
        try:
            item = AccountConfiguration.objects.get(id=account_id)
        except Exception as ex:
            return Response({"error":"Invalid Account Configure"},status=status.HTTP_400_BAD_REQUEST)
        data=[]
        s=AwsService(access_key=item.access_key,secret_access_key=item.secret_access_key,region_name="us-east-1")
        # data.append({"profile_name":item.user_name,
        # "stast":s.ec2_state_stats()})
        return Response(s.list_ec2_filter_choices())

class RDSFilterChoices(APIView):
    permission_classes = []
    def get(self, request,*args,**kwargs):
        account_id=kwargs.get("account_id",None)
        try:
            item = AccountConfiguration.objects.get(id=account_id)
        except Exception as ex:
            return Response({"error":"Invalid Account Configure"},status=status.HTTP_400_BAD_REQUEST)
        data=[]
        s=AwsService(access_key=item.access_key,secret_access_key=item.secret_access_key,region_name="us-east-1")
        return Response(s.list_rds_filter_choices())
