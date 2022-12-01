from boto3 import Session
# najeebshah052
class AwsService:
    def __init__(self,access_key,secret_access_key,region_name):
        self.session=Session(aws_access_key_id=access_key,aws_secret_access_key=secret_access_key,region_name=region_name)
        self.profile_name=self.session.profile_name
        self.region_name=self.session.region_name if self.session.region_name else region_name
    
    @property
    def session_info(self):
        return self.session
    
    
    
    def list_user_account(self):
        client =  self.session.client('iam')
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
