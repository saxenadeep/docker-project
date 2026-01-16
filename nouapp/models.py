from django.db import models

# Create your models here.

class login(models.Model):
    userid=models.CharField(primary_key=True, max_length=200)
    password=models.CharField(max_length=100)
    usertype=models.CharField(max_length=50)
    status=models.CharField(max_length=10)


class registration(models.Model):
    rollno=models.IntegerField(primary_key=True, max_length=20)
    name=models.CharField(max_length=225)
    fname=models.CharField(max_length=225)
    mname=models.CharField(max_length=225)
    gender=models.CharField(max_length=50)
    address=models.CharField(max_length=500)
    email=models.CharField(max_length=100)
    program=models.CharField(max_length=100)
    branch=models.CharField(max_length=100)
    year=models.CharField(max_length=50)
    contactno=models.CharField(max_length=15)
    password=models.CharField(max_length=50)
    profile_pic=models.ImageField(upload_to='')
    regdate=models.DateTimeField()


class tbl_contact(models.Model):
    id=models.IntegerField(primary_key=True, auto_created=True)
    name=models.CharField(max_length=100)
    gender=models.CharField(max_length=10)
    address=models.CharField(max_length=500)
    contactno=models.CharField(max_length=13)
    email=models.CharField(max_length=100)
    enquirytext=models.CharField(max_length=500)
    enqdate=models.DateTimeField()



class tbl_Usm(models.Model):
    id=models.IntegerField(primary_key=True, auto_created=True)
    program=models.CharField(max_length=100)
    branch=models.CharField(max_length=200)
    year=models.CharField(max_length=10)
    subject=models.CharField(max_length=100)
    new_file=models.FileField(upload_to='myimage')



class upload_lecture(models.Model):
    id=models.IntegerField(primary_key=True, auto_created= True)
    program=models.CharField(max_length=100)
    branch=models.CharField(max_length=200)
    year=models.CharField(max_length=10)
    subject=models.CharField(max_length=100)
    link=models.CharField(max_length=200)
   


class Upload_Assignment(models.Model):
    id=models.IntegerField(primary_key=True, auto_created=True)
    program=models.CharField(max_length=100)
    branch=models.CharField(max_length=200)
    year=models.CharField(max_length=10)
    subject=models.CharField(max_length=100)
    new_file=models.FileField(upload_to='myimage')


class Complaints(models.Model):
    id=models.IntegerField(primary_key=True, auto_created=True)
    name=models.CharField(max_length=200)
    program=models.CharField(max_length=100)
    branch=models.CharField(max_length=200)
    year=models.CharField(max_length=10)
    subject=models.CharField(max_length=100)
    comp=models.CharField(max_length=500)
    reqdate=models.DateTimeField()
    





class Feedback(models.Model):
    id=models.IntegerField(primary_key=True, auto_created=True)
    name=models.CharField(max_length=200)
    program=models.CharField(max_length=100)
    branch=models.CharField(max_length=200)
    year=models.CharField(max_length=10)
    subject=models.CharField(max_length=100)
    feed=models.CharField(max_length=500)
    reqdate=models.DateTimeField()
    

class tbl_noti(models.Model):
    id=models.IntegerField(primary_key=True, auto_created=True)
    notif=models.CharField(max_length=200)
    notireg=models.DateTimeField()