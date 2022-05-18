from django.db import models
from django.db.models.functions import Lower
import uuid
from django.template.defaultfilters import slugify

# Create your models here.


class Staff(models.Model):
    station = (
        ('general', 'General'),
        ('branch', 'Branch'),
        ('warehouse', 'Warehouse'),
        ('service shop', 'Service Shop'),
    )

    id = models.UUIDField(primary_key=True, unique=True,
                          default=uuid.uuid4, editable=False)
    slug = models.SlugField(max_length=50, blank=True)
    first_name = models.CharField(max_length=50, blank=False)
    middle_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=False)
    dob = models.DateField()
    phone_number = models.CharField(max_length=15, blank=False)
    email = models.CharField(max_length=200, blank=False)

    designation = models.CharField(max_length=50, blank=False, choices=station)
    workplace = models.CharField(max_length=50, blank=False)
    role = models.CharField(max_length=50, blank=False)

    qualification = models.CharField(max_length=50, blank=True)
    institution = models.CharField(max_length=100, blank=True)

    salary = models.CharField(max_length=20, blank=True, null=True)

    date_joined = models.DateField()

    def save(self, *args, **kwargs):
        fullname = "{}-{}".format(self.first_name, self.last_name)
        self.slug = slugify(fullname)
        super(Staff, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        ordering = [Lower("first_name"), "-date_joined"]

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
