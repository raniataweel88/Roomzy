from django.db import models



class Hotel(models.Model):
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    description = models.TextField()
    address = models.CharField(max_length=255,default='')
    rating = models.FloatField(default=0)
    image = models.ImageField(upload_to='media/')
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    def __str__(self):
        return f"{self.name} - {self.city}"
