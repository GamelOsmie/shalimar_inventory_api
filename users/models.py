from typing import List

from django.contrib.auth.models import (AbstractUser, BaseUserManager,
                                        PermissionsMixin)
from django.db import models
from django.db.models.functions import Lower
from django.template.defaultfilters import slugify


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser, PermissionsMixin):
    def default_designation():
       return {
           "id": "",
           "workplace": ""
       }

    class UserRole(models.TextChoices):
        SUPER_ADMIN = 'Super Admin', ('Super Admin')
        ADMIN = 'Admin', ('Admin')
        IMPORT_OFFICER = 'Import Officer', ('Import Officer')
        TRACKING_OFFICER = 'Tracking Officer', ('Tracking Officer')
        WAREHOUSE_OFFICER = 'Warehouse Officer', ('Warehouse Officer')
        BRANCH_OFFICER = 'Branch Officer', ('Branch Officer')
        SERVICE_STATION_OFFICER = 'Service Station Officer', ('Service Station Officer')
        WEBSITE_MANAGER = 'Website Manager', ('Website Manager')

    slug = models.SlugField(max_length=50, blank=True)

    email = models.EmailField(max_length=254, unique=True)
    first_name = models.CharField(max_length=40, blank=True, null=True)
    middle_name = models.CharField(max_length=40, blank=True, null=True)
    last_name = models.CharField(max_length=40, blank=True, null=True)
   
    role = models.CharField(max_length=50, choices=UserRole.choices, default=None, blank=True, null=True)
    workplace = models.CharField(max_length=50, default="General", blank=True, null=True)

    is_superuser = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=True)
    
    objects = CustomUserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['role', 'first_name', 'middle_name', 'last_name', 'workplace']


    def save(self, *args, **kwargs):
        if self.role == "Admin":
            self.is_staff == True
        #this line below give to the instance slug field a slug name
        self.slug = slugify("{} {}".format(self.first_name, self.last_name))
        #this line below save every fields of the model instance
        super(User, self).save(*args, **kwargs)

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)

    class Meta:
        ordering = [Lower('first_name')]

    @property
    def fullname(self):
        if self.first_name == None:
            first_name = ""
        else:
            first_name = self.first_name

        if self.first_name == None:
            middle_name = ""
        else:
            middle_name = self.middle_name

        if self.first_name == None:
            last_name = ""
        else:
            last_name = self.last_name

        name = f"{first_name} {middle_name} {last_name}"
        return name
