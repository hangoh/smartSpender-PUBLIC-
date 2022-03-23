from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager

# Create your models here.


class AccountManager(BaseUserManager):
    def create_user(self,email,username,currency,password):
        user = self.model(
            email = email,
            username =username,
            currency = currency
        )
        user.set_password(password)
        user.save(using = self._db)
        return user
    
    def create_superuser(self,email,username,password):
        user = self.create_user(
            email = email,
            username = username,
            password = password,
            currency = 'USD'
        )

        user.is_staff = True
        user.is_admin = True
        user.is_superuser = True
        user.save(using = self._db)
        return user



class Account(AbstractBaseUser):
    email = models.EmailField(unique=True,verbose_name='email',max_length=255,blank=False,null=False)
    username = models.CharField(max_length=150,blank=False,null=False)
    currency = models.CharField(default='USD',max_length=10,blank=False,null=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
  
    objects = AccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return str(self.username)

    def has_module_perms(self,app_label):
        return self.is_admin
    
    def has_perm(self,perm,obj=None):
        return True
