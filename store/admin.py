from django.contrib import admin

from store.models import User,Category,Brand,BodyType,Car,Discount,CarBooking

# Register your models here.

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(BodyType)
admin.site.register(Car)
admin.site.register(CarBooking)
admin.site.register(Discount)

