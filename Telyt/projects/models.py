from django.db import models
from django.utils.timezone import now

# Create your models here.

#model storing project general details

class Projects(models.Model):
    # owner = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    project_name = models.CharField(max_length=300)
    created_date = models.DateTimeField(default=now, editable=True)
    project_status = models.CharField(max_length=1, choices=(('C', 'Completed'), ('Ip', 'InProgress'),('P','Pending')), blank=False, default='P')
    staff_handling = models.CharField(max_length=300,default="select staff")

    def __str__(self):
        return self.project_name

#model storing project specific files
class Files(models.Model):
    project_parent = models.ForeignKey(to=Projects, null=True, blank=True,on_delete=models.CASCADE)
    files = models.FileField(upload_to='clientfiles/',default='media/README')
    file_name = models.CharField(max_length=300,default="file name")
    upload_date = models.DateTimeField(default=now, editable=True)

    def __str__(self):
        return self.file_name
