from django.contrib import admin

# Register your models here.
from aws.models import AccountConfiguration

admin.site.register(AccountConfiguration)