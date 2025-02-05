from django import forms

from store.models import User,CarBooking

from django.contrib.auth.forms import UserCreationForm



class SignUpForm(UserCreationForm):

    class Meta:

        model=User

        fields=["username","email","password1","password2","phone"]


class SignInForm(forms.Form):

    username=forms.CharField()

    password=forms.CharField()

    

    



class BookingConfirmForm(forms.ModelForm):

    class Meta:

        model=CarBooking

        fields=['fullname', 'from_date','to_date','phone','email','address','city','pickup_location','special_request','with_driver','payment_method']

        widgets={

            

            "from_date":forms.DateInput(attrs={"class":"form-control","type":"date"}),

            "to_date":forms.DateInput(attrs={"class":"form-control","type":"date"}),

            "with_driver":forms.Select(attrs={"class":"form-control form-select"})
        }

    

    def clean(self):

        cleaned_data=super().clean()

        car=self.instance.product_object

        if car and car.stock_car <= 0:

            raise forms.ValidationError("This car is out of stock!")
        
        return cleaned_data




   
   