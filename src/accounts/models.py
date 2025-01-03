from django.db import models

from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager
)


class UserManager(BaseUserManager):
    def create_user(self, email, full_name=None, password=None, is_active=True, is_staff=False, is_admin=False):
        if not email:
            raise ValueError (" users must have an email address ")

        if not password:
            raise ValueError("user must input password")
        # if not full_name:
        #     raise ValueError("please enter your fullname")

        user_obj = self.model(
            email = self.normalize_email(email),
            full_name=full_name
        )
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.active = is_active

        user_obj.set_password(password)
        user_obj.save(using=self._db)
        return user_obj 

    def create_staffuser(self, email, full_name=None, password=None):
        user = self.create_user(
            email,
            full_name=full_name,
            password=password,
            is_staff=True,
        )
        return user

    def create_superuser(self, email, full_name=None, password=None):
        user = self.create_user(
            email,
            full_name=full_name,
            password=password,
            is_admin=True,
            is_staff=True,
        )

class User(AbstractBaseUser):
    email = models.EmailField(unique=True, max_length=225, default="abc123@gmail.com")
    full_name =models.CharField(max_length=225, blank=True, null=True)
    active  = models.BooleanField(default=True)
    staff =models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    timestamp   = models.DateField(auto_now=True)


    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS=[]  #'full_name'

    objects=UserManager()

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True    

    def __str__(self):
        return self.email

    def get_full_name(Self):
        return Self.email

    def get_short_name(self):
        if self.full_name:
            return self.full_name
        return self.email

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active


class GuestEmail(models.Model):
    email = models.EmailField()
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.email
    



