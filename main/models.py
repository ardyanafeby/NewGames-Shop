import uuid
from django.db import models

# Create your models here.
class Item(models.Model):
    CATEGORY_CHOICES = [
        ('fashion olahraga', 'Fashion Olahraga'),
        ('peralatan Olahraga', 'Peralatan Olahraga'),
        ('suplemen Olahraga', 'Suplemen Olahraga'),
        ('kesehatan dan kebugaran', 'Kesehatan dan Kebugaran'),
        ('bola', 'Bola'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)                
    price = models.IntegerField()                          
    description = models.TextField()                       
    thumbnail = models.URLField()                          
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)             
    is_featured = models.BooleanField(default=False)       
    stock = models.PositiveIntegerField(default=0)
    brand = models.CharField(max_length=50, blank=True, null=True)


    def __str__(self):
        return self.name
    
    def increment_views(self):
        self.views += 1
        self.save()
