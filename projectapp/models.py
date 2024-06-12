from django.db import models

# Create your models here.
class tbl_register(models.Model):
    username = models.CharField(max_length=20,null=True)
    email = models.CharField(max_length=20, null=True)
    password = models.CharField(max_length=20,null=True)
    confirmpassword = models.CharField(max_length=20, null=True)

class tbl_Product(models.Model):
    name = models.CharField(max_length=255,null=True)
    description = models.TextField(null=True)
    price = models.IntegerField(null=True)
    image = models.ImageField(upload_to='product_images/', null=True, blank=True)

    def __str__(self):
        return self.name
class ProductReview(models.Model):
    customer_name = models.CharField(max_length=255)
    review_title = models.TextField()
    rating = models.CharField(max_length=5)
    comment = models.TextField()


class Review_result(models.Model):
    review=models.TextField(null=True)
    result=models.CharField(max_length=100,null=True)
    comment = models.TextField(null=True)

