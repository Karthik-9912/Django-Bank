from django.db import models


# Create your models here.
class Acc_type(models.Model):
    name=models.CharField(max_length=32)

    def __str__(self):
        return self.name
    
class Gender(models.Model):
    name=models.CharField(max_length=7)

    def __str__(self):
        return self.name
    
class BankDetails(models.Model):
    acc_num=models.BigAutoField(primary_key=True)
    name=models.CharField(max_length=32)
    phone=models.PositiveBigIntegerField(unique=True)
    email=models.EmailField(unique=True)
    aadhar_num=models.PositiveBigIntegerField(unique=True)
    profile=models.ImageField(upload_to='profile_pics')
    aadhar_photo=models.ImageField(upload_to='aadhar_details')
    acc_type = models.ForeignKey(Acc_type,on_delete=models.CASCADE)
    Gender=models.ForeignKey(Gender,on_delete=models.CASCADE)
    pin=models.CharField(max_length=32)
    balance=models.DecimalField(default=1000,max_digits=7,decimal_places=2)
    address=models.TextField()
    occupation=models.CharField(max_length=32)

    def save(self,*args,**kwargs):
        if not self.acc_num:
            last=BankDetails.objects.order_by('-acc_num').first()
            self.acc_num=(last.acc_num+1)if last else 9685741230
        super().save(*args,**kwargs)
    