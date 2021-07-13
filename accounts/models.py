from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from datetime import datetime,timedelta
import jwt
from django.conf import settings

class UserManager(BaseUserManager):
    def create_user(self, username,first_name,last_name,email,password,state,city,pincode,phonenumber,is_Trader,is_Admin,is_Farmer,GSTIN="",company_name=""):
        if username is None:
            raise TypeError('Users must have a username.')
        if email is None:
            raise TypeError('Users must have an email address.')

        farmer = self.model(username=username, first_name=first_name,last_name=last_name,email=email,state=state,city=city,pincode=pincode,phonenumber=phonenumber,is_Trader=is_Trader,is_Admin=is_Admin,is_Farmer=is_Farmer,GSTIN=GSTIN,company_name=company_name)
        farmer.is_superuser = True
        farmer.is_staff = True
        farmer.set_password(password)
        farmer.save()
        return farmer
    
    def create_superuser(self, username,first_name,last_name,email,password,state,city,pincode,phonenumber,is_Trader=False,is_Admin=True,is_Farmer=False):
        if password is None:
            raise TypeError('Superusers must have a password.')
        admin = self.create_user(username,first_name,last_name,email,password,state,city,pincode,phonenumber,is_Trader,is_Admin,is_Farmer)
        admin.is_superuser = True
        admin.is_staff = True
        admin.save()
        return admin

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name=models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password= models.CharField(max_length=255)
    state= models.CharField(max_length=255)
    city= models.CharField(max_length=255)
    pincode= models.IntegerField()
    phonenumber= models.CharField(max_length=10)
    GSTIN = models.CharField(max_length=255,default="")
    company_name = models.CharField(max_length=255,default="")
    is_Trader = models.BooleanField(default=False)
    is_Farmer=models.BooleanField(default=False)
    is_Admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff= models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','first_name','last_name','state','city','pincode','phonenumber']
    objects = UserManager()

    def __str__(self):
        return self.email

    @property
    def token(self):
        return self._generate_jwt_token()

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    def _generate_jwt_token(self):
        dt = datetime.now() + timedelta(days=60)

        token = jwt.encode({
            'id': self.pk,
            'exp': int(dt.strftime('%s'))
        }, settings.SECRET_KEY, algorithm='HS256')

        return token.decode('utf-8')