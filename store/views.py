from django.shortcuts import render,redirect,get_object_or_404

from django.views.generic import View

from store.forms import SignUpForm,SignInForm,BookingConfirmForm

from django.core.mail import send_mail

from store.models import User,Car,CarBooking,BookingItem

from django.contrib import messages

from django.contrib.auth import authenticate,login,logout

from django.views.decorators.csrf import csrf_exempt

from django.utils.decorators import method_decorator

from decouple import config



RZP_KEY_ID=config('RZP_KEY_ID')

RZP_KEY_SECRET=config('RZP_KEY_SECRET')







# Create your views here.

def send_otp_email(user):

    user.genarate_otp()

    subject="Verify your Email"

    message=f"otp for Account Verification is {user.otp}"

    from_email="murshihz@gmail.com"

    to_email=[user.email]

    send_mail(subject,message,from_email,to_email)


class SignUpView(View):

    template_name="register.html"

    form_class=SignUpForm

    def get(self,request,*args,**kwargs):

        form_instance=self.form_class()

        return render(request,self.template_name,{"form":form_instance})
    
    def post(self,request,*args,**kwargs):

        form_data=request.POST

        form_instance=self.form_class(form_data)

        if form_instance.is_valid():

            #not save,commit=false not to database but get userobject,

            user_object=form_instance.save(commit=False)

            user_object.is_verified=False

            user_object.save()

            send_otp_email(user_object)

            return redirect("verify-email")
        return render(request,self.template_name,{"form":form_instance})



class VerifyEmailView(View):

    template_name="verify_email.html"

    def get(self,request,*args,**kwargs):

        return render(request,self.template_name)
    
    def post(self,request,*args,**kwargs):

# from verify email template get "name"=otp of text box
        
        otp=request.POST.get("otp")

        try:

            user_object=User.objects.get(otp=otp)

            user_object.is_verified=True

            user_object.is_active=True
    #after verify otp,otp=none for other user use this
            user_object.otp=None

            user_object.save()

            return redirect("signin")
        
        except:

            messages.error(request,"Invalid Otp")

            return render(request,self.template_name)


class SignInView(View):

    template_name="signin.html"

    form_class=SignInForm

    def get(self,request,*args,**kwargs):

        form_instance=self.form_class()

        return render(request,self.template_name,{"form":form_instance})

    def post(self,request,*args,**kwargs):

        form_data=request.POST

        form_instance=self.form_class(form_data)

        if form_instance.is_valid():

            data=form_instance.cleaned_data

            uname=data.get("username")

            pswd=data.get("password")

            user_object=authenticate(request,username=uname,password=pswd)

            if user_object:

                login(request,user_object)

                return redirect("car-list")
            

        return render(request,self.template_name,{"form":form_instance})


class CarListView(View):

    template_name="car_list.html"

    def get(self,request,*args,**kwargs):

        qs=Car.objects.all()
        
        return render(request,self.template_name,{"data":qs})

class CarDetailView(View):

    template_name="car_detail.html"

    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        qs=Car.objects.get(id=id)



        return render(request,self.template_name,{"data":qs})
    
#Booking view or booking confirm


import razorpay

class CarBookingConfirmView(View):

    template_name="booking_confirm.html"

    form_class=BookingConfirmForm

    def get(self,request,*args,**kwargs):

        car_id=kwargs.get("pk")

        car=Car.objects.get(id=car_id)

        form_instance=self.form_class()

        return render(request,self.template_name,{"form":form_instance,"car":car})
    
    def post(self,request,*args,**kwargs):

        form_data=request.POST

        form_instance=self.form_class(form_data)

        car_id=kwargs.get("pk")

        car=Car.objects.get(id=car_id)

        # for availabilty for choosing date

        availability_status="Available"

        total_payment = None

        if form_instance.is_valid():

            from_date=form_instance.cleaned_data.get("from_date")

            to_date=form_instance.cleaned_data.get("to_date")

            payment_method=form_instance.cleaned_data.get("payment_method")

            print(payment_method)

            duration = (to_date - from_date).days  # Calculate booking duration

           


            # check car is available for the choosing dates

            overlapping_bookings=CarBooking.objects.filter(

                product_object=car,

                to_date__gte=from_date,
                
                from_date__lte=to_date,
            )

            if overlapping_bookings.exists():

                availability_status="Not Available"

                messages.error(request,"The Selected dates are not availble")

            else:

                 # Determine the total payment
                if duration <= 7:
                    total_payment = duration * car.price_per_day
                elif duration <= 30:
                    total_payment = car.price_per_week
                else:
                    total_payment = car.price_per_month


                booking=form_instance.save(commit=False)

                booking.customer=request.user

                booking.product_object=car

                booking.is_order_placed=True

                booking.total_payment = total_payment

                

                booking.save()

                


                # create bookingitem

                BookingItem.objects.create(

                    booking_object=booking,

                    order_object=car,

                    price_per_day=car.price_per_day,

                    


                )

                if payment_method=="ONLINE":

                    client = razorpay.Client(auth=(RZP_KEY_ID,RZP_KEY_SECRET))

                    total_amount=(total_payment)*100


                    data = { "amount": total_amount, "currency": "INR", "receipt": "order_rcptid_11" }

                    payment = client.order.create(data=data)

                    rzp_order_id=payment.get("id")

                    booking.rzp_order_id=rzp_order_id            #from model

                    booking.save()

                    context={
                        "amount":total_amount,

                         "currency":"INR",

                        "key_id":RZP_KEY_ID,

                        "order_id":rzp_order_id

                       
                    }

                    return render(request,"payment.html",context)
                
                
                
                # messages.success(request,"Booking confirmed Successfully!!")

                # print(f"Total Payment: {total_payment}")
                
        return redirect("booking-summary")
            
        
        

class BookingSummaryView(View):

    template_name="booking_summary.html"

    def get(self,request,*args,**kwargs):

        qs=request.user.booking.all()

        # qs=CarBooking.objects.filter(customer=request.user)

        return render(request,self.template_name,{"bookings":qs})

@method_decorator([csrf_exempt],name="dispatch")
class PaymentVerificationView(View):

    def post(self,request,*args,**kwargs):

        client = razorpay.Client(auth=(RZP_KEY_ID, RZP_KEY_SECRET))

        try:

            client.utility.verify_payment_signature(request.POST)
            print("payment sucess")

            order_id=request.POST.get('razorpay_order_id')

            booking_object=CarBooking.objects.get(rzp_order_id=order_id)

            booking_object.is_paid=True

            booking_object.save()

            login(request,booking_object.customer)

        except:

            print("payment failed")


        print(request.POST)

        return redirect("booking-summary")
    
