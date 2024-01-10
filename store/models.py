from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class CustomUser(AbstractUser):
    pass

class Category(models.Model):
      name = models.CharField(max_length=100)
      

      def __str__(self):
        return self.name

class Product(models.Model):
     image = models.ImageField(upload_to='product_images/', null=True, blank=True)
     title = models.CharField(max_length=100)
     description = models.TextField()
     price = models.DecimalField(max_digits=10,decimal_places=2)
     categories = models.ManyToManyField(Category)

     def __str__(self):
        return self.title
     
class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} by {self.user.username} on {self.created_at}"
    
