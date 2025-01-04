from django.db import models

from django.contrib.auth.models import AbstractUser

from django.db.models.signals import post_save

from random import randint

from django.utils import timezone

from datetime import timedelta



# Create your models here.

class User(AbstractUser):

    phone=models.CharField(max_length=10,unique=True)

    is_verified=models.BooleanField(default=False)

    otp=models.CharField(max_length=6,null=True,blank=True)

    #genarate otp for user

    def genarate_otp(self):

        self.otp=str(randint(1000,9999))+str(self.id)

        self.save()

class Profile(models.Model):

    owner=models.OneToOneField(User,on_delete=models.CASCADE)

    phone=models.CharField(max_length=15,unique=True)

    bio=models.TextField()

    profile_picture=models.ImageField(upload_to="profiles/",null=True,blank=True,default="profiles/default.png")

def create_profile(sender,instance,created,**kwargs):

    if created:

        Profile.objects.create(owner=instance)

post_save.connect(User,create_profile)

    
class BaseModel(models.Model):

    creaed_date=models.DateTimeField(auto_now_add=True)

    updated_date=models.DateTimeField(auto_now=True)

    is_active=models.BooleanField(default=False)

class Brand(BaseModel):

    name=models.CharField(max_length=200)

    def __str__(self):
        return self.name
    
class Category(BaseModel):

    name=models.CharField(max_length=200)

    def __str__(self):
        return self.name

class BodyType(BaseModel):

    name=models.CharField(max_length=1000)

    def __str__(self):
        return self.name
    
class Car(BaseModel):

    title=models.CharField(max_length=200)

    category_objects=models.ManyToManyField(Category)

    brand_object=models.ForeignKey(Brand,on_delete=models.CASCADE,related_name="brands")

    body=models.ForeignKey(BodyType,on_delete=models.CASCADE,related_name="cars")

    year=models.PositiveIntegerField()

    CONDITION_CHOICES=(
        ("New","New"),
        ("Used","Used"),
    )

    condition=models.CharField(max_length=20,choices=CONDITION_CHOICES,default="used")

    gear_type=models.CharField(max_length=100,default="Automatic")

    fuel_choices=(
        ("petrol","Petrol"),
        ("diesel","Diesel"),
        ("Electric","Electric"),
        ("Hybrid","Hybrid")
    )

    fuel_type=models.CharField(max_length=100,choices=fuel_choices,default="petrol")

    mileage=models.CharField(max_length=200)

    color=models.CharField(max_length=100)

    seats=models.PositiveIntegerField()

    picture=models.ImageField(upload_to="car_images",null=True,blank=True)

    price_per_day=models.PositiveIntegerField()

    price_per_week=models.PositiveIntegerField()

    price_per_month=models.PositiveIntegerField()


    description=models.TextField()

    def __str__(self):
        return self.title

class CarBooking(BaseModel):

    product_object=models.ForeignKey(Car,on_delete=models.CASCADE,related_name="booking")

    customer=models.ForeignKey(User,on_delete=models.CASCADE)

    fullname=models.CharField(max_length=100)

    from_date=models.DateField()

    to_date=models.DateField()

    phone=models.CharField(max_length=15,unique=True)

    email=models.EmailField()

    address=models.TextField()

    city=models.CharField(max_length=100)

    pickup_location=models.CharField(max_length=100)

    special_request=models.TextField()

    PAYMENT_OPTIONS=(
        ("COD","COD"),
        ("ONLINE","ONLINE")
    )

    payment_method=models.CharField(max_length=15,choices=PAYMENT_OPTIONS,default="COD")

    rzp_order_id=models.CharField(max_length=100)

    is_paid=models.BooleanField(default=False)

class BookingItem(BaseModel):

    booking_object=models.ForeignKey(CarBooking,on_delete=models.CASCADE,related_name="book_item")


    total=models.FloatField()