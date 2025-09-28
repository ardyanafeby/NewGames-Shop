import uuid
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Item(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    CATEGORY_CHOICES = [
        ('fashion olahraga', 'Fashion Olahraga'),
        ('peralatan olahraga', 'Peralatan Olahraga'),
        ('suplemen olahraga', 'Suplemen Olahraga'),
        ('kesehatan dan kebugaran', 'Kesehatan dan Kebugaran'),
        ('bola', 'Bola'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid, editable=False)
    name = models.CharField(max_length=100)                
    price = models.IntegerField()
    sale_price = models.IntegerField(blank=True, null=True)                      
    description = models.TextField()                       
    thumbnail = models.URLField()                          
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)             
    is_featured = models.BooleanField(default=False)       
    stock = models.PositiveIntegerField(default=0)
    brand = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.name
    
    @property
    def is_on_sale(self):
        return self.sale_price is not None and self.sale_price < self.price
    
