from django.db import models

# Create your models here.

class Products(models.Model):

    def __str__(self):
        return self.title
    title = models.CharField(max_length=200)
    price =models.FloatField()
    discount_price = models.FloatField()
    category = models.CharField(max_length=200)
    description = models.TextField()
    image = models.CharField(max_length=400)



class Orders(models.Model):

    def __str__(self):
        return self.name
    
    
    Items = models.CharField(max_length=1500 ,default="nothing")
    name = models.CharField(max_length=100,default="nothing" )
    email= models.EmailField(max_length=100,default="nothing" )
    password= models.CharField(max_length=100, default="nothing")
    address= models.CharField(max_length=100,default="nothing")
    city= models.CharField(max_length=100, default="nothing")
    state= models.CharField(max_length=100,default="nothing")
    zipcode= models.CharField(max_length=100,default="nothing")
    totalprice = models.FloatField( max_length=200 , default='nothing', blank=True) 