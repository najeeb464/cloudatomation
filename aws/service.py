from boto3 import Session
import json
import base64
from PIL import Image
# from StringIO import StringIO
import io
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

    def rds_image(self,type_='cpu'):
        if type_=="cpu":
            rds = '{"metrics": [["AWS/RDS", "CPUUtilization"]]}'
        elif type_=="storage":
            rds = '{"metrics": [["AWS/RDS", "FreeStorageSpace"]]}'
        elif type_=="memory":
            rds = '{"metrics": [["AWS/RDS", "FreeableMemory"]]}'
        client = self.session.client('cloudwatch')
        response = client.get_metric_widget_image(MetricWidget=rds)
        # return response["MetricWidgetImage"]
        bytes_data=io.BytesIO(response["MetricWidgetImage"])
        fr=base64.b64encode(bytes_data.getvalue())
        
        # im = Image.open(bytes_data)
        return fr
    def ec2_list(self):
        ess=self.session.client("ec2")
        all_regions=ess.describe_regions()
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
        
    def ec2_graph(self,type_="cpu"):
        instance_list=[]
        instance_image_list=[]
        data=[]
        ec2_li=self.ec2_list()
        instance_ids=[i["InstanceId"] for i in ec2_li]
        client = self.session.client('cloudwatch')
        for ins in instance_ids:
            if type_=="cpu":
                data.append(["AWS/EC2", "CPUUtilization", "InstanceId",str(ins)])
            elif type_=="in":
                data.append(["AWS/EC2", "NetworkIn", "InstanceId",str(ins)])
            elif type_=="out":
                data.append(["AWS/EC2", "NetworkOut", "InstanceId",str(ins)])
            elif type_=="pin":
                data.append(["AWS/EC2", "NetworkPacketsIn", "InstanceId",str(ins)])
            filter_data={"metrics":data}



        response = client.get_metric_widget_image(MetricWidget=json.dumps(filter_data))
        bytes_data=io.BytesIO(response["MetricWidgetImage"])
        fr=base64.b64encode(bytes_data.getvalue())
        return fr


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