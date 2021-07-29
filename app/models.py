from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxLengthValidator, MinValueValidator
from django.utils.safestring import mark_safe

# Create your models here.


class Customer(models.Model):
    STATE_CHOICES = (
        ('Dhaka', 'Dhaka'),
        ('Gazipur', 'Gazipur'),
        ('Chittagong', 'Chittagong'),
        ('Khulna', 'Khulna'),
        ('Sylhet', 'Sylhet'),
        ('Rajshahi', 'Rajshahi'),
        ('Mymensingh', 'Mymensingh'),
        ('Barisal', 'Barisal'),
        ('Rangpur', 'Rangpur'),
        ('Comilla', 'Comilla'),
        ('Narayanganj', '	Narayanganj'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=11)
    locality = models.CharField(max_length=200)
    city = models.CharField(max_length=100, choices=STATE_CHOICES)
    zipcode = models.PositiveIntegerField()

    def __str__(self):
        return f"Id: {self.id} - Name: {self.name}"


class Product(models.Model):
    CATEGORY_CHOICES = (
        ('M', 'Mobile'),
        ('L', 'Laptop'),
        ('H', 'Headphone'),
        ('T', 'Television'),
    )
    title = models.CharField(max_length=100)
    selling_price = models.PositiveIntegerField()
    discounted_price = models.PositiveIntegerField()
    description = models.TextField()
    brand = models.CharField(max_length=100)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    product_image = models.ImageField(upload_to='product_img')

    def __str__(self):
        return f"{self.title}"

    def image_tag(self):
        if self.product_image.url is not None:
            return mark_safe('<img src="{}" height="50px" />'.format(self.product_image.url))
        else:
            return ""


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.quantity}-{self.product.title}'


class OrderPlaced(models.Model):
    STATUS_CHOICES = (
        ('Accepted', 'Accepted'),
        ('Packed', 'Packed'),
        ('On The Way', 'On The Way'),
        ('Delivered', 'Delivered'),
        ('Cancel', 'Cancel'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=50, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f'{self.user.username}-{self.product.title}'
