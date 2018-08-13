from django.db import models
from django.utils import timezone


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
    STATUS_CHOICES = (
        ('Active', 'ACTIVE'),
        ('Inactive', 'INACTIVE'),
        ('Not Working', 'NOT WORKING'),
        ('Disposed', 'DISPOSED'),
    )
    iid = models.AutoField(primary_key=True)
    manufacture_name = models.CharField(max_length=20)
    model_name = models.CharField(max_length=20, null=True, blank=True)
    device_type = models.CharField(max_length=20)
    serial_number = models.CharField(max_length=30, unique=True)
    location = models.CharField(max_length=120)
    proprietor = models.CharField(max_length=30)
    status = models.CharField(max_length=12, choices=STATUS_CHOICES)

    def __str__(self):
        return '%s %s %s %s %s %s %s'%(self.iid, self.manufacture_name, self.device_type, self.serial_number, self.location, self.proprietor, self.status)

class Add(models.Model):
    aid = models.AutoField(primary_key=True)
    sid = models.ForeignKey(Staff, on_delete=models.CASCADE)
    iid = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    added_date = models.DateTimeField(
        default=timezone.now)

    def additem(self):
        self.save()

    def __str__(self):
        return '%s %s %s %s'%(self.aid, self.sid, self.iid, self.added_date)

class Remove(models.Model):
    rid = models.AutoField(primary_key=True)
    sid = models.ForeignKey(Staff, on_delete=models.CASCADE)
    iid = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    removed_date = models.DateTimeField(default=timezone.now)
    reason = models.CharField(max_length=200)

    def removeitem(self):
        self.save()

    def __str__(self):
        return '%s %s %s %s'%(self.rid, self.sid, self.iid, self.removed_date)

class Transfer(models.Model):
    tid = models.AutoField(primary_key=True)
    sid = models.ForeignKey(Staff, on_delete=models.CASCADE)
    iid = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    to = models.CharField(max_length=120)
    transfered_date = models.DateTimeField(default=timezone.now)

    def transferitem(self):
        self.save()

    def __str__(self):
        return '%s %s %s %s %s'%(self.tid, self.sid, self.iid, self.to, self.transfered_date)

class Dispose(models.Model):
    did = models.AutoField(primary_key=True)
    sid = models.ForeignKey(Staff, on_delete=models.CASCADE)
    iid = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    disposed_date = models.DateTimeField(default=timezone.now)
    reason = models.CharField(max_length=200)
    
    def disposeitem(self):
        self.save()

    def __str__(self):
        return '%s %s %s %s'%(self.did, self.sid, self.iid, self.disposed_date)