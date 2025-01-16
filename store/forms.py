from django import forms

from store.models import User,CarBooking

from django.contrib.auth.forms import UserCreationForm


from django.utils.timezone import now

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

        fields=['fullname','from_date','to_date','phone','email','address','city','pickup_location','special_request','payment_method']

        widgets={

            

            "from_date":forms.DateInput(attrs={"class":"form-control","type":"date"}),

            "to_date":forms.DateInput(attrs={"class":"form-control","type":"date"}),

            "with_driver":forms.Select(attrs={"class":"form-control form-select"})
        }

    def clean(self):

        cleaned_data=super().clean()

        from_date=cleaned_data.get("from_date")

        to_date=cleaned_data.get("to_date")

        if from_date and to_date:

            if from_date < now().date():

                raise forms.ValidationError("Start date cannot be in the past")
            
            if to_date <= from_date:

                raise forms.ValidationError("End date must be after the start date")
            
        return cleaned_data

   