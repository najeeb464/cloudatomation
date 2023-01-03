from django.db import models
from accounts.models import User
# Create your models here.
from aws.service import AwsService
class AccountConfiguration(models.Model):
    user_name        =models.CharField(max_length=120,null=True,blank=True)
    region_name         =models.CharField(max_length=120,null=True,blank=True)
    arn                 =models.CharField(max_length=120,null=True,blank=True)
    user_id             =models.CharField(max_length=120,null=True,blank=True)
    access_key          =models.CharField(max_length=120)
    secret_access_key   =models.CharField(max_length=120)
    is_default          =models.BooleanField(default=True)

    def __str__(self):
        return str(self.id)
    @property
    def service(self):
        return AwsService(self.access_key,self.secret_access_key)
    

