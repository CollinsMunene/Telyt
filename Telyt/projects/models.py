from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User
# Create your models here.

#model storing project general details

class Projects(models.Model):
    owner = models.ForeignKey(to=User, null=True, blank=True,on_delete=models.CASCADE)
    project_name = models.CharField(max_length=300)
    created_date = models.DateTimeField(default=now, editable=True)
    project_status = models.CharField(max_length=20, choices=(('C', 'Completed'), ('Ip', 'InProgress'),('P','Pending')), blank=False, default='P')
    staff_handling = models.CharField(max_length=300,default="select staff")

    def __str__(self):
        return self.project_name

#model storing project specific files
class Files(models.Model):
    project_parent = models.ForeignKey(to=Projects, null=True, blank=True,on_delete=models.CASCADE)
    file_upload = models.FileField(upload_to ='clientfiles/',default='media/README',null=True) 
    file_name = models.CharField(max_length=300,default="file name")
    upload_date = models.DateTimeField(default=now, editable=True)

    def __str__(self):
        return self.file_name
