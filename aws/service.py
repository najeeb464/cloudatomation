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
        # for x in response['Users']:
        #     data.append({"user_id":x["UserId"],"":x[''],"":x['']})

            

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
            
            for bucket in response['Buckets']:
                buckets.append(bucket)
        except Exception as ex:
            print("Couldn't get buckets.",ex)
            pass
        return buckets

    def s3_stats(self,bucket_list):
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
        data["buckets"]=[]
        data["buckets"].append(bucket_stats)
        return data

    def S3_bucket_objects_detail(self,bucket_name):
        s3_client=self.session.client("s3")
        response_data=[]
        your_bucket=s3_client.list_objects_v2(Bucket=bucket_name)
        try:
            for obj in your_bucket['Contents']:
                response_data.append(obj)
        except Exception as ex:
            print("ex")
            pass
        return response_data
    def list_rds_all_region(self):
        response_data=[]
        try:
            available_regions = self.session.get_available_regions('rds')
            print("available_regions",available_regions)
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
                        print("exception",ex)
                        continue
                        pass
                return response_data
        except Exception as ex:
            print("exception",ex)
            pass
        return response_data
    def list_rds(self):
        response_data=[]
     
        available_regions = self.session.get_available_regions('rds')
        print("available_regions",available_regions)
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
                "DBInstanceStatus":i["DBInstanceStatus"]
            })
            except Exception as ex:
                print("exception",ex)
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
        "InstanceId":instance_data["InstanceId"],
        "InstanceType":instance_data["InstanceType"],
        "State":instance_data["State"]["Name"],
        "PrivateIpAddress":instance_data["PrivateIpAddress"],
        "PublicIpAddress":instance_data["PublicIpAddress"],
        "SecurityGroups":instance_data["SecurityGroups"],
        }
        return response

    def rds_image(self):
        rds = '{"metrics": [["AWS/RDS", "CPUUtilization"]]}'
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
        # for each_region in all_regions["Regions"]:
        #     list_region.append(each_region["RegionName"])
        for instance in ess.describe_instances()["Reservations"]:
            for each_in in instance["Instances"]:
                response_data.append(self.instance_output_format(each_in))

        # for each_region in list_region:
        #     resource= self.session.resource("ec2",region_name=each_region)
        #     for each_instance in resource.instances.all():
        #         print("each_instance",each_instance)
        #         response_data.append({"Id":each_instance.id})
        # client_=self.session.client("ec2",region_name=each_region)
        # for each in client_.describe_instances()["Reservations"]:
        #     for each_in in each["Instances"]:
        #         print("each_in",each_in)
        #     print("instanceId",each_in["InstanceId"],each_in["State"]["Name"])
        return response_data
    
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
        
    def ec2_graph(self):
        client = self.session.client('cloudwatch')
        json = '{"metrics": [["AWS/EC2", "CPUUtilization", "InstanceId", \
                      "i-0f9b0d57300e87d3c"]]}'
        response = client.get_metric_widget_image(MetricWidget=json)
        bytes_data=io.BytesIO(response["MetricWidgetImage"])
        fr=base64.b64encode(bytes_data.getvalue())
        # im = Image.open(io.BytesIO(response["MetricWidgetImage"]))
        # im.save("cw-1.png")
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