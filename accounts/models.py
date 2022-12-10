from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
from django.contrib.auth.models import Permission, Group

class UserManager(BaseUserManager):
    def create_user(self, email, password=None ):
        if email is None:
            raise TypeError('Users should have a Email')
        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None):
        if password is None:
            raise TypeError('Password should not be none')
        user                = self.create_user( email, password)
        user.is_superuser   = True
        user.is_staff       = True
        user.is_verified    =True
        user.is_approved    =True
        for _p in Permission.objects.all():
            user.user_permissions.add(_p)
        user.save()
        return user

class User(AbstractBaseUser, PermissionsMixin):
    name      = models.CharField(max_length=120)
    email           = models.EmailField(max_length=255, unique=True, db_index=True)
    is_approved     = models.BooleanField(default=False)
    is_verified     = models.BooleanField(default=False)
    is_active       = models.BooleanField(default=True)
    is_staff        = models.BooleanField(default=False)
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)

    USERNAME_FIELD  = 'email'
    objects = UserManager()
    def __str__(self):
        return "%s"%(self.email)