from django.db import models
from django.utils import timezone
import uuid

class Staff(models.Model):
    POSITION_CHOICES = (
        ('SCT', 'Senior Computer Technician'),
        ('CT', 'Computer Technician'),
        ('SNA', 'Systems Network Administrator'),
        ('SPO', 'Senior Project Officer'),
        ('DPM', 'Deputy Programme Manager'),
        ('PM', 'Programme Manager'),
    )
    sid = models.AutoField(primary_key=True)
    username = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=15)
    last_name = models.CharField(max_length=15)
    position = models.CharField(max_length=3, choices=POSITION_CHOICES)

    def __str__(self):
        return '%s %s'%(self.first_name, self.last_name)

class Inventory(models.Model):
    iid = models.AutoField(primary_key=True)
    manufacture_name = models.CharField(max_length=20)
    model_name = models.CharField(max_length=20, null=True, blank=True)
    device_type = models.CharField(max_length=20)
    serial_number = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return '%s %s %s %s %s'%(self.iid, self.manufacture_name, self.model_name, self.device_type, self.serial_number)

class Transactions(models.Model):

    class Meta:
        ordering = ['-date']

    STATUS_CHOICES = (
        ('Active', 'ACTIVE'),
        ('Inactive', 'INACTIVE'),
        ('Not Working', 'NOT WORKING'),
        ('Disposed', 'DISPOSED'),
    )
    OPERATION_CHOICES = (
        ('Add','ADD'),
        ('Transfer','TRANSFER'),
        ('Remove','REMOVE'),
        ('Change Status','CHANGE STATUS'),
        ('Disposed', 'DISPOSED'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    sid = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True)
    iid = models.ForeignKey(Inventory, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(default=timezone.now, blank=True)
    operation = models.CharField(max_length=14, choices=OPERATION_CHOICES)
    remarks = models.TextField(null=True, blank=True)
    location = models.CharField(max_length=120)
    proprietor = models.CharField(max_length=30)
    status = models.CharField(max_length=12, choices=STATUS_CHOICES)

    def __str__(self):
        return '%s %s %s %s'%(self.id, self.sid, self.iid, self.operation)