from django.db import models
from django.db.models.functions import Lower
import uuid
from django.template.defaultfilters import slugify

# Create your models here.


class Staff(models.Model):
    department_options = (
        ('General Office', 'General Office'),
        ('Branch', 'Branch'),
        ('Warehouse', 'Warehouse'),
        ('Service Shop', 'Service Shop'),
    )

    
    role_options = (
        ('Accountant', 'Accountant'),
        ('HR', 'HR'),
        ('Sales Executive', 'Sales Executive'),
        ('Credit Officer', 'Credit Officer'),
    )
    
    
    qualification_options = (
        ('WASSCE', 'WASSCE'),
        ('Diploma', 'Diploma'),
        ('HND', 'HND'),
        ('Bachelors Degree', 'Bachelors Degree'),
        ('Masters Degree', 'Masters Degree'),
        ('Other', 'Other'),
    )
    

    id = models.UUIDField(primary_key=True, unique=True,
                          default=uuid.uuid4, editable=False)
    slug = models.SlugField(max_length=50, blank=True)
    first_name = models.CharField(max_length=50, blank=False)
    middle_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=False)
    dob = models.DateField(blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=False)
    email = models.CharField(max_length=200, blank=False)

    department = models.CharField(max_length=50, blank=False, choices=department_options)
    workplace = models.CharField(max_length=50, blank=False)
    role = models.CharField(max_length=50, blank=False, choices=role_options)

    qualification = models.CharField(max_length=50, blank=True, null=True, choices=qualification_options)
    institution = models.CharField(max_length=100, blank=True)

    salary = models.CharField(max_length=20, blank=True, null=True)

    date_joined = models.DateField(blank=True, null=True)

    def save(self, *args, **kwargs):
        fullname = "{}-{}".format(self.first_name, self.last_name)
        self.slug = slugify(fullname)
        super(Staff, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        ordering = [Lower("first_name"), "-date_joined"]

    def fullname(self):
        if self.first_name == None:
            first_name = ""
        else:
            first_name = self.first_name

        if self.middle_name == None:
            middle_name = ""
        else:
            middle_name = self.middle_name

        if self.last_name == None:
            last_name = ""
        else:
            last_name = self.last_name
            
        name = f"{first_name} {middle_name} {last_name}"

        return name
