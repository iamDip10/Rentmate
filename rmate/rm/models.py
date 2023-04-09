from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Residant(models.Model):
    fname = models.CharField(max_length=10)
    lname = models.CharField(max_length=10)
    gender = models.CharField(max_length=8)
    phn = models.CharField(max_length=12, primary_key=True)
    mail = models.CharField(max_length=100)
    psword = models.CharField(max_length=40)
    p_addrs = models.CharField(max_length=200)
    div = models.CharField(max_length=10)
    area = models.CharField(max_length=10)
    nid = models.CharField(max_length=20)
    uname = models.CharField(max_length=30, null=True)
    per_addrs = models.CharField(max_length=100, null=True)
    about_me = models.CharField(max_length=500, null=True)
    authheticate = models.CharField(max_length=500, default="NO")
    OTP = models.CharField(max_length=100, null=True)
    image = models.ImageField(upload_to="img/", null=True)
    class Meta:
        db_table = "residant" 
        
class Pro_owner(models.Model):
    fname = models.CharField(max_length=10)
    lname = models.CharField(max_length=10)
    gender = models.CharField(max_length=8)
    phn = models.CharField(max_length=12, primary_key=True)
    mail = models.CharField(max_length=100)
    psword = models.CharField(max_length=40)
    p_addrs = models.CharField(max_length=200)
    div = models.CharField(max_length=10)
    area = models.CharField(max_length=10)
    nid = models.CharField(max_length=20)
    hid = models.CharField(max_length=50)
    
    class Meta:
        db_table = "pro_owner"
        
class Complain(models.Model):
    date = models.CharField(max_length=30)
    comID = models.AutoField(primary_key=True)
    slv_status = models.CharField(max_length=20, default="Not Solved")
    prob_type = models.CharField(max_length=50)
    prob_desc = models.CharField(max_length=200)
    nei_ID = models.CharField(max_length=50, null=True)
    user = models.ForeignKey(Residant, on_delete=models.CASCADE)
    year = models.CharField(max_length=7, default="0")
    class Meta:
        db_table = "complain"
        
        
class ResRent(models.Model):
    amount = models.IntegerField(null=True, default=0)
    status = models.CharField(max_length=30, default="NOT PAID", null=True)
    deadline = models.CharField(max_length=40, null=True, default="none")
    month = models.CharField(max_length=30, default="none", null=True)
    paymentID = models.CharField(max_length=100, default="none")
    user = models.ForeignKey(Residant, on_delete=models.CASCADE, default="NULL")
    date = models.CharField(max_length=50, default="0-0-0000", null=True)
    uniqID = models.CharField(max_length=60, primary_key=True) 
    
    class Meta:
        db_table = "residantrent"
        
class Notifications(models.Model):
    notification = models.CharField(max_length=400, null=True, default=" ")
    date = models.CharField(max_length=30, null=True, default=" ")
    user = models.ForeignKey(Residant, on_delete=models.CASCADE, default=" ")
    status = models.CharField(max_length=60, null=False, default="unread")
    class Meta:
        db_table = "notifications"
        
class activity(models.Model):
    user = models.ForeignKey(Residant, on_delete=models.CASCADE, default="")
    active_time = models.IntegerField(null=True)
    last_login = models.CharField(max_length=100, null=True)
    side_activity = models.CharField(max_length=150, null=True)
    last_log_time = models.CharField(max_length=100, null=True)
    class Meta:
        db_table = "activity"
        
class otherActivity(models.Model) :
    user = models.ForeignKey(Residant, on_delete=models.CASCADE, default="")
    activ_time = models.CharField(max_length=100, null=True)
    msg = models.CharField(max_length=140, null=True)
    
    class Meta:
        db_table = "otherActivity"