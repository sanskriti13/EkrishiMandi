from django.db import models
import datetime
from datetime import datetime,timedelta
# Create your models here.
class crops(models.Model):
    cname = models.CharField(max_length=20)
    msp_current = models.IntegerField()
    msp_past = models.IntegerField()
    cimage = models.CharField(max_length=100)

    def __str__(self):
        return self.cname

class farmers(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    zipcode = models.IntegerField()
    crop = models.ForeignKey(crops,on_delete=models.CASCADE)
    qty = models.IntegerField(default = 0)
    entrytime = models.DateTimeField(default = datetime.now())
    active = models.BooleanField(default= True)

    def __str__(self):
        return self.name

class trader(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    zipcode = models.IntegerField()

    def __str__(self):
        return self.name

class trade(models.Model):
    farmer = models.ForeignKey(farmers, on_delete=models.CASCADE)
    crop = models.ForeignKey(crops,on_delete=models.CASCADE)
    trader = models.ForeignKey(trader,on_delete=models.CASCADE)
    lastBid = models.IntegerField()
