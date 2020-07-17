from django.db import models
from django.contrib.auth.models import User, auth
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import forms

# Create your models here.

User._meta.get_field("email")._unique = True
# User._meta.get_field('username')._unique = False


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["email", "username", "password1", "password2"]
   

class Costumer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    email= models.CharField(max_length=200, null=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    isguest = models.BooleanField(default=False, null=True, blank=False)
    

    def __str__(self):
        return str(self.user)

class Product(models.Model):
    name = models.CharField(max_length=200, null=True)
    price = models.FloatField()
    digital = models.BooleanField(default=False, null=True, blank=False)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name
    
    @property
    def ImageUrl(self):
        try:
            url = self.image.url
        except:
            url = ""
        return url


class Order(models.Model):
    costumer = models.ForeignKey(Costumer, on_delete=models.SET_NULL, blank=True, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length= 200, null=True)

    @property
    def needsShipping(self):
        shipping = False
        orders = self.orderitem_set.all()
        for item in orders:
            if item.product.digital == False:
                shipping = True
        return shipping

    @property
    def get_total_cartP(self):
        todos_items = self.orderitem_set.all()
        for item in todos_items:
            print(item.get_total)
        total = sum([item.get_total for item in todos_items])
        return total
    
    @property
    def get_total_cartQ(self):
        todos_items = self.orderitem_set.all()
        total = sum([item.quantity for item in todos_items])
        return total


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    order= models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    data_added= models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

class ShippingAddress(models.Model):
    costumer = models.ForeignKey(Costumer, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True)
    zipcode = models.CharField(max_length=200, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address

    