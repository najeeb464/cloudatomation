from boto3 import Session
import json
import base64
from PIL import Image
# from StringIO import StringIO
import io
from datetime import datetime,timedelta
class AwsService:
    def __init__(self,access_key,secret_access_key,region_name=None):
        self.session=Session(aws_access_key_id=access_key,aws_secret_access_key=secret_access_key,region_name=region_name)
        self.iam =self.session.resource('iam').CurrentUser()
        self.profile_name=self.iam.user_name
        self.region_name=self.session.region_name if self.session.region_name else region_name
    
    @property
    def session_info(self):
        return self.session
    
    def get_user_detail(self):
        data={
            "user_name":self.iam.user_name,
            "user_id":self.iam.user_id,
            "arn":self.iam.arn
            }
        return data
    
    def list_user_account(self):
        client =  self.session.client('iam',region_name=self.region_name)
        response = client.list_users()
        return response
    
    def map_user_list_with_serializer(self):
        response=self.list_user_account()
        data=[]
        return response['Users']
            

    def render_list_user_account(self):
        _user_li=[]
        response=self.list_user_account()
        for x in response['Users']:
            _user_li.append(x['UserName'])
        return _user_li
   
    
    def list_s3(self):
        s3_client =  self.session.client('s3')
        buckets =[]
        try:
            response = s3_client.list_buckets()
            print("response",response['Buckets'])
            
            for bucket in response['Buckets']:
                buckets.append(bucket)
        except Exception as ex:
            pass
        return buckets
    
    def s3_graph(self,filters):
        type_           =filters.get("graphtype","allr")
        bucket_name           =filters.get("bucket_name",None)
        dimensions=[]
        if bucket_name is None:
            for i in self.list_s3():
                dimensions.append({'Name':'BucketName','Value':i["Name"]})
        else:
            dimensions.append({ 'Name': 'BucketName','Value':"alpha1122"})
        print("dimensions",dimensions)
        if type_=="allr":
            metricName="AllRequests"
        elif type_=="allfr":
            metricName="FailedRequests"
        elif type_=="gr":
            metricName="GetRequests"
        elif type_=="lr":
            metricName="ListRequests"
        elif type_=="pr":
            metricName="PutRequests"
        elif type_=="dr":
            metricName="DeleteRequests"
        elif type_=="hr":
            metricName="HeadRequests"
        elif type_=="allr":
            metricName="PostRequests"
        elif type_=="sr":
            metricName="SelectRequests"
        elif type_=="ssb":
            metricName="SelectScannedBytes"
        elif type_=="srb":
            metricName="SelectReturnedBytes"
        elif type_=="srr":
            metricName="SelectReturnedRecords"
        elif type_=="bd":
            metricName="BytesDownloaded"
        elif type_=="bu":
            metricName="BytesUploaded"
        elif type_=="4e":
            metricName="4xxErrors"
        elif type_=="5e":
            metricName="5xxErrors"
        elif type_=="fbl":
            metricName="FirstByteLatency"
        elif type_=="trl":
            metricName="TotalRequestLatency"
        else:
            metricName="AllRequests"
        cw = self.session.client('cloudwatch')
        start_time = datetime.utcnow() - timedelta(days=1)
        end_time = datetime.utcnow()
        print("metricName",metricName)
        period = 60
        statistics = ['Average']
        response = cw.get_metric_statistics(
            Namespace='AWS/S3',
            MetricName=metricName,
            Dimensions=[{'Name': 'BucketName','Value': 'aws-sam-cli-managed-default-samclisourcebucket-2mc20s10obol'}],
            StartTime=start_time,
            EndTime=end_time,
            Period=period,
            Statistics=statistics
        )
        cpu_utilization_data_points = response.get('Datapoints',[])
        print("cpu_utilization_data_points",cpu_utilization_data_points)
        try:
            cntx=[{"label":data["Timestamp"],"value":data["Average"]}for data in cpu_utilization_data_points]
        except:
            cntx=[]
        out_context={"key":response["Label"],"values":cntx}
        return out_context

    def s3_stats(self,bucket_list=[]):
        rs=self.session.resource('s3')
        bucket_stats=[]
        data={}
        if len(bucket_list)==0:
            s3_list=self.list_s3()
        else:
            s3_list=bucket_list
        data["count"]=len(s3_list)
        for i in s3_list:
            count=0
            size=0
            all_object=rs.Bucket(i["Name"]).objects.all()
            for obj in all_object:
                size+=obj.size
                count+=1
            inner_data={"bucket_name":i["Name"],"objects_count":count,"object_size":size}
            bucket_stats.append(inner_data)
        data["buckets"]=bucket_stats
        return data

    def S3_bucket_objects_detail(self,bucket_name):
        s3_client=self.session.client("s3")
        response_data=[]
        your_bucket=s3_client.list_objects_v2(Bucket=bucket_name)
        try:
            for obj in your_bucket['Contents']:
                response_data.append(obj)
        except Exception as ex:
            pass
        return response_data
    def list_rds_all_region(self):
        response_data=[]
        try:
            available_regions = self.session.get_available_regions('rds')
            for region in available_regions:
                client = self.session.client('rds',region_name=region)
                response = client.describe_db_instances()
                
                for i in response['DBInstances']:
                    try:
                        # response_data.append(i)
                        response_data.append({
                        "DBInstanceIdentifier": i['DBInstanceIdentifier'],
                        "DBInstanceClass":i["DBInstanceClass"],
                        "AllocatedStorage":i["AllocatedStorage"],
                        "Engine":i["Engine"],
                        "AvailabilityZone":i["AvailabilityZone"],
                        "DBInstanceArn":i["DBInstanceArn"],
                        "DBInstanceStatus":i["DBInstanceStatus"]
                    })
                    except Exception as ex:
                        continue
                        pass
                return response_data
        except Exception as ex:
            pass
        return response_data
    def list_rds(self):
        response_data=[]
     
        available_regions = self.session.get_available_regions('rds')
        client = self.session.client('rds')
        response = client.describe_db_instances()
        for i in response['DBInstances']:
            try:
                response_data.append({
                "DBInstanceIdentifier": i['DBInstanceIdentifier'],
                "DBInstanceClass":i["DBInstanceClass"],
                "AllocatedStorage":i["AllocatedStorage"],
                "Engine":i["Engine"],
                "AvailabilityZone":i["AvailabilityZone"],
                "DBInstanceArn":i["DBInstanceArn"],
                "DBInstanceStatus":i["DBInstanceStatus"],
                "MasterUsername":i["MasterUsername"]
            })
            except Exception as ex:
                continue
                pass
        return response_data

    def rds_detail(self,instance_arn):
        client = self.session.client('rds')
        response_data=[]
        response=client.describe_db_instances(DBInstanceIdentifier=instance_arn)
        for i in response.get('DBInstances',[]):
            response_data.append(i)
        return response_data

    def instance_output_format(self,instance_data):
        response={
        "InstanceId":instance_data.get("InstanceId",''),
        "InstanceType":instance_data.get("InstanceType",""),
        "State":instance_data["State"]["Name"],
        "PrivateIpAddress":instance_data.get("PrivateIpAddress",""),
        "PublicIpAddress":instance_data.get("PublicIpAddress",""),
        "SecurityGroups":instance_data.get("SecurityGroups",""),
        "Placement":instance_data.get("Placement",""),
        "Architecture":instance_data.get("Architecture",""),
        }
        return response

    def rds_image(self,filters):
        type_           =filters.get("graphtype","cpu")
        db_instance_id     =filters.get("db_instance_id",None)
        availability_zone   =filters.get("availability_zones",None)
        filters=[]
        print("qs",filters)
        if db_instance_id:
            filters.append({'Name': 'db-instance-id','Values': [db_instance_id]})
        dimensions=[]
        if db_instance_id is None or db_instance_id =="":
            rdslistqs=self.list_rds()
            print("rdslistqs",rdslistqs)
            for i in rdslistqs:
                dimensions.append({'Name': 'DBInstanceIdentifier','Value': i["DBInstanceIdentifier"]})
        # else:
        #     print("db_instance_id is None")
        #     dimensions.append({'Name': 'DBInstanceIdentifier','Value':db_instance_id})
        if availability_zone:
            dimensions.append({'Name': 'AvailabilityZone','Value': availability_zone})
        print("dimensions",dimensions)

        if type_=="cpu":
            metricName="CPUUtilization"
        elif type_=="storage":
            metricName="FreeStorageSpace"
        elif type_=="memory":
            metricName="FreeableMemory"
        elif type_=="bldu":
            metricName="BinLogDiskUsage"
        elif type_=="dc":
            metricName="DatabaseConnections"
        elif type_=="dqd":
            metricName="DiskQueueDepth"
        elif type_=="nrt":
            metricName="NetworkReceiveThroughput"
        elif type_=="ntt":
            metricName="NetworkTransmitThroughput"
        elif type_=="ri":
            metricName="ReadIOPS"
        elif type_=="rla":
            metricName="ReadLatency"
        elif type_=="rtp":
            metricName="ReadThroughput"
        elif type_=="rl":
            metricName="ReplicaLag"
        elif type_=="su":
            metricName="SwapUsage"
        elif type_=="wi":
            metricName="WriteIOPS"
        elif type_=="wl":
            metricName="WriteLatency"
        elif type_=="wtp":
            metricName="WriteThroughput"
        else:
            metricName="CPUUtilization"

        cw = self.session.client('cloudwatch')
        
     
        start_time = datetime.utcnow() - timedelta(hours=3)
        end_time = datetime.utcnow()
        period = 1800
        statistics = ['Average']
        if len(dimensions)>0:
            print("lebnght of dimension is greater than 0")
            response = cw.get_metric_statistics(
                Namespace='AWS/RDS',
                MetricName=metricName,
                Dimensions=dimensions,
                StartTime=start_time,
                EndTime=end_time,
                Period=period,
                Statistics=statistics
            )
        else:
            response = cw.get_metric_statistics(
                Namespace='AWS/RDS',
                MetricName=metricName,
                StartTime=start_time,
                EndTime=end_time,
                Period=period,
                Statistics=statistics
            )
        cpu_utilization_data_points = response.get('Datapoints',[])
        try:
            cntx=[{"label":data["Timestamp"],"value":data["Average"]}for data in cpu_utilization_data_points]
        except:
            cntx=[]
        out_context={"key":response["Label"],"values":cntx}
        return out_context

 
    def ec2_list(self,filters=[]):
        ess=self.session.client("ec2")
        all_regions=ess.describe_regions(Filters=filters)
        list_region=[]
        response_data=[]
        for instance in ess.describe_instances()["Reservations"]:
            for each_in in instance["Instances"]:
                response_data.append(self.instance_output_format(each_in))
        return response_data

    def ec2_state_stats(self):
        stats = {
            'pending': 0,
            'running': 0,
            'shutting-down': 0,
            'terminated': 0,
            'stopping': 0,
            'stopped': 0
            }
        ec2_instance = self.session.client('ec2')
        qs_ = ec2_instance.get_paginator('describe_instances')
        response_ = qs_.paginate()
        for rs in response_:
            for reservation in rs['Reservations']:
                for instance in reservation['Instances']:
                    state = instance['State']['Name']
                    stats[state] += 1
        graph_data=[]
        for i in stats.keys():
            graph_data.append({"key":i,"value":int(stats[i])})
        return graph_data
            
    def ec2_runing_instance(self):
        ess=self.session.resource("ec2")
        filters = [{
                'Name': 'instance-state-name', 
                'Values': ['running']
                 }
                ]
        instances = ess.instances.filter(Filters=filters)
        RunningInstances = []
        for instance in instances:
            RunningInstances.append(instance.id)
        return RunningInstances
        
    def ec2_graph(self,filters):
        start_time = datetime.utcnow() - timedelta(hours=1)
        end_time = datetime.utcnow()
        period = 600 
        instance_list=[]
        instance_image_list=[]
        instance_ids=[]
        data=[]
        
        type_           =filters.get("graphtype","cpu")
        instance_type           =filters.get("instance_types",None)
        instanceId_     =filters.get("instance_id",None)
        imageId         =filters.get("image_id",None)
        availability_zone         =filters.get("availability_zone",None)
        filters         =[]
        dimensions=[]
        if imageId:
            dimensions.append({'Name': 'image-id', 'Values': [imageId]})
        if instanceId_:
            dimensions.append({'Name': 'instance-id', 'Values': [instanceId_]})
            
        if availability_zone:
            dimensions.append({'Name': 'availability-zone', 'Values': [instanceId_]})
        if instance_type:
            dimensions.append({'Name': 'instance-type', 'Values': [instanceId_]})
        print("filters",filters)
        if instanceId_ is None or instanceId_=="":  
            ec2_li=self.ec2_list(filters=filters)
            instance_ids=[i["InstanceId"] for i in ec2_li]
        else:
            instance_ids=[instanceId_]

        if type_=="cpu":
            metricName="CPUUtilization"
        elif type_=="in":
            metricName="NetworkIn"
        elif type_=="out":
            metricName="NetworkOut"
        elif type_=="pin":
            metricName="NetworkPacketsIn"
        elif type_=="drb":
            metricName="DiskReadBytes"
        elif type_=="dro":
            metricName="DiskReadOps"
        elif type_=="dwb":
            metricName="DiskWriteBytes"
        elif type_=="dwo":
            metricName="DiskWriteOps"
        elif type_=="npo":
            metricName="NetworkPacketsOut"
        elif type_=="scf":
            metricName="StatusCheckFailed"
        elif type_=="scfi":
            metricName="StatusCheckFailed_Instance"
        elif type_=="scfs":
            metricName="StatusCheckFailed_System"

        
        
       
        client = self.session.client('cloudwatch')
        
        for ins in instance_ids:
            dimensions = [{'Name': 'InstanceId', 'Value': str(ins)} for ins in instance_ids]
        print("dimensions",dimensions)
        response = client.get_metric_statistics(
        Namespace="AWS/EC2",
        MetricName=metricName,
        Dimensions=dimensions,
        StartTime=start_time,
        EndTime=end_time,
        Period=period,
        Statistics=['Average']
        )
        print("response",response)
        cpu_utilization_data_points = response.get('Datapoints',[])
        try:
            cntx=[{"label":data["Timestamp"],"value":data["Average"]}for data in cpu_utilization_data_points]
        except:
            cntx=[]
        out_context={"key":response["Label"],"values":cntx}

        return out_context

            # if type_=="cpu":
                # metricName="CPUUtilization"
                # data.append(["AWS/EC2", "CPUUtilization", "InstanceId",str(ins)])
            # elif type_=="in":
                # metricName="NetworkIn"
                # data.append(["AWS/EC2", "NetworkIn", "InstanceId",str(ins)])
            # elif type_=="out":
                # metricName="NetworkOut"
                # data.append(["AWS/EC2", "NetworkOut", "InstanceId",str(ins)])
            # elif type_=="pin":
                # metricName="NetworkPacketsIn"
                # data.append(["AWS/EC2", "NetworkPacketsIn", "InstanceId",str(ins)])
            # filter_data={"metrics":data}
        


        # response = client.get_metric_widget_image(MetricWidget=json.dumps(filter_data))
        # bytes_data=io.BytesIO(response["MetricWidgetImage"])
        # fr=base64.b64encode(bytes_data.getvalue())
        # return fr


    def stop_ec2(self,ec2_instance):
        ec2 = self.session.resource('ec2')
        try:
            ec2.Instance(ec2_instance).stop()
        except:
            return False
        return True
    def start_ec2(self,ec2_instance):
        ec2 = self.session.resource('ec2')
        try:
            ec2.Instance(ec2_instance).start()
        except:
            return False
        return True


    def ec2_detail(self,instanceId):
        ess=self.session.client("ec2")
        ess.describe_instances(InstanceIds=[instanceId])
        return
    
    def list_ec2_filter_choices(self):
        ec2=self.session.client("ec2")
        context={}
        response = ec2.describe_instances()
        instances = response['Reservations']

        instance_ids = []
        image_ids=[]
        availability_zones=[]
        instance_types = []

        for instance in instances:
            instance_id = instance['Instances'][0]['InstanceId']
            image_id = instance['Instances'][0]['ImageId']
            availability_zone = instance['Instances'][0]['Placement']['AvailabilityZone']
            instance_type = instance['Instances'][0]['InstanceType']
            instance_ids.append(instance_id)
            image_ids.append(image_id)
            availability_zones.append(availability_zone[:-1])
            instance_types.append(instance_type)
        context["instance_types"]=[ {"key":i,"value":i}for i in instance_types]
        context["availability_zones"]=[{"key":i,"value":i}for i in availability_zones]
        context["instance_ids"]=[{"key":i,"value":i} for i in instance_ids]
        context["image_ids"]=[{"key":i,"value":i} for i in image_ids]
        return context
    
    def list_rds_filter_choices(self):
        rds = self.session.client('rds')
        context={}
        response = rds.describe_db_instances()
        dbinstances=response['DBInstances']
        instance_ids=[]
        avalibilty_zone=[]
        for instance in dbinstances:
            instance_ids.append(instance['DBInstanceIdentifier'])
            avalibilty_zone.append(instance["AvailabilityZone"])
        context["db_identifier"]=[ {"key":i,"value":i}for i in instance_ids]
        context["availability_zones"]=[ {"key":i,"value":i}for i in avalibilty_zone]
        return context





