from django.shortcuts import render,redirect,get_object_or_404

from django.views.generic import View

from store.forms import SignUpForm,SignInForm,BookingConfirmForm

from django.core.mail import send_mail

from store.models import User,Car,CarBooking,Brand,Category,BodyType,Discount

from django.contrib import messages

from django.contrib.auth import authenticate,login,logout

from django.db.models import Q

from django.core.paginator import Paginator

from django.views.decorators.csrf import csrf_exempt

from django.utils.decorators import method_decorator

from store.decorators import signin_required

from django.views.decorators.cache import never_cache


from django.utils import timezone

from decouple import config



RZP_KEY_ID=config('RZP_KEY_ID')

RZP_KEY_SECRET=config('RZP_KEY_SECRET')

decs=[signin_required,never_cache]






# Create your views here.

def send_otp_email(user):

    user.genarate_otp()

    subject="Verify your Email"

    message=f"otp for Account Verification is {user.otp}"

    from_email="murshihz@gmail.com"

    to_email=[user.email]

    send_mail(subject,message,from_email,to_email)

class LandingPageView(View):

    template_name="home.html"
    
    def get(self,request,*args,**kwargs):

        qs=Car.objects.all()

        brands=Brand.objects.all()


        
        
        return render(request,self.template_name,{"cars":qs,"brands":brands})
    
    def post(self,request,*args,**kwargs):

        cars=Car.objects.all()
        brands=Brand.objects.all()

        
        return render(request,self.template_name,{"cars":cars,"brands":brands})
    

class AboutUsView(View):

    template_name="aboutus.html"

    def get(self,request,*args,**kwargs):

       

        return render(request,self.template_name)
    
class ServicesView(View):

    template_name="services.html"

    def get(self,request,*args,**kwargs):

        

        return render(request,self.template_name)

        



        

    

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

                return redirect("home")
            

        return render(request,self.template_name,{"form":form_instance})

@method_decorator(decs,name="dispatch")
class CarListView(View):

    template_name="car_list.html"

    def get(self,request,*args,**kwargs):

        
        search_text=request.GET.get("filter")

        

        qs=Car.objects.all().prefetch_related("discounts")

        for car in qs:

            car.active_discount=car.discounts.filter(active=True).first()

        paginator=Paginator(qs,4)

        page_number=request.GET.get("page")

        page_object=paginator.get_page(page_number)

        

        all_title=Car.objects.values_list("title",flat=True).distinct()
        all_category_objects=Car.objects.values_list("category_objects",flat=True).distinct()
        all_brand_object=Car.objects.values_list("brand_object",flat=True).distinct()
        all_body=Car.objects.values_list("body",flat=True).distinct()
        all_condition=Car.objects.values_list("condition",flat=True).distinct()
        all_fuel_type=Car.objects.values_list("fuel_type",flat=True).distinct()
        all_color=Car.objects.values_list("color",flat=True).distinct()

        all_records=[]

        all_records.extend(all_title)
        all_records.extend(all_category_objects)
        all_records.extend(all_brand_object)
        all_records.extend(all_body)
        all_records.extend(all_condition)
        all_records.extend(all_fuel_type)
        all_records.extend(all_color)


        if search_text:

            qs=qs.filter(Q(title__contains=search_text)
                          |Q(category_objects__name__icontains=search_text) 
                          |Q(brand_object__name__contains=search_text) 
                          |Q(body__name__contains=search_text) 
                          |Q(condition__contains=search_text) 
                          |Q(fuel_type__contains=search_text) 
                          |Q(color__contains=search_text))


        
        return render(request,self.template_name,{"page_obj":page_object,"records":all_records})
    

    """
    current page number - ?page={{page_obj.number}}

    next page number - ?page={{page_obj.next_page_number}}

    previous page number - ?page={{page_obj.previous_page_number}}

    last page number - ?page={{page_obj.paginator.num_pages}}

    
    """



@method_decorator(decs,name="dispatch")
class CarDetailView(View):

    template_name="car_detail.html"

    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        qs=Car.objects.get(id=id)



        return render(request,self.template_name,{"data":qs})

@method_decorator(decs,name="dispatch")   
class CarDeleteView(View):

    def get(sef,request,*args,**kwargs):

        id=kwargs.get("pk")

        Car.objects.get(id=id).delete()

        return redirect("car-list")
    
#Booking view or booking confirm



import razorpay
@method_decorator(decs,name="dispatch")
class CarBookingConfirmView(View):

    template_name="booking_confirm.html"

    form_class=BookingConfirmForm

    def get(self,request,*args,**kwargs):

        car_id=kwargs.get("pk")

        car=Car.objects.get(id=car_id)

        form_instance=self.form_class()

        # get active discount

        discount=car.discounts.filter(active=True).first()
        
        return render(request,self.template_name,{"form":form_instance,"car":car, "discount": discount})
    
    def post(self,request,*args,**kwargs):

        form_data=request.POST

        form_instance=self.form_class(form_data)

        car_id=kwargs.get("pk")

        car=Car.objects.get(id=car_id)

        # check car is out of stock

        if car.stock_car <= 0:

            messages.error(request,"This car is out of stock")

            return redirect("car-list")

        if form_instance.is_valid():

            

            from_date=form_instance.cleaned_data.get("from_date")

            to_date=form_instance.cleaned_data.get("to_date")

            total_payment=form_instance.cleaned_data .get("total_payment") 

            final_price=form_instance.cleaned_data .get("final_price")

            discount_amount=form_instance.cleaned_data .get("discount_amount")


            payment_method=form_instance.cleaned_data.get("payment_method")

            
            print(payment_method)

            # days duration between dates
            duration_days=(to_date-from_date).days

            total_payment=0

            # calculate total_payment based on duration

            

            if duration_days <=7:

                total_payment=duration_days*car.price_per_day

            elif duration_days == 30:

                total_payment=car.price_per_month

            elif duration_days <=30:

                weeks=duration_days // 7

                remaining_days=duration_days % 7

                total_payment=(weeks*car.price_per_week)+(remaining_days*car.price_per_day)


            else:

                months=duration_days // 30

                remaining_days=duration_days % 30

                weeks=remaining_days // 7

                days=remaining_days % 7

                total_payment=(months*car.price_per_month)+(weeks*car.price_per_week)+(days*car.price_per_day)

            #apply active discount

            car_discount=car.discounts.filter(active=True).first()

            discount_amount=0

            if car_discount:

                if car_discount.discount_type =="percentage":

                    discount_amount = (total_payment * car_discount.value)/100

                elif car_discount.discount_type == "flat amount":

                    discount_amount = car_discount.value

            discounted_price = total_payment -discount_amount

            final_price = discounted_price

            booking=form_instance.save(commit=False)

            booking.customer=request.user

            booking.product_object=car

            booking.total_payment = total_payment

            booking.discount_amount = discount_amount

            booking.final_price = final_price

            booking.is_order_placed=True

            booking.save()

            #show stock reduce

            car.stock_car -= 1

            car.save()

            if payment_method=="ONLINE":

                client = razorpay.Client(auth=(RZP_KEY_ID,RZP_KEY_SECRET))

                # total_amount=(total_payment)*100

                total_amount = int(final_price * 100)  # Convert to paisa
                    
                data = { "amount": total_amount, "currency": "INR", "receipt": "order_rcptid_11" }

                payment = client.order.create(data=data)

                rzp_order_id=payment.get("id")

                booking.rzp_order_id=rzp_order_id            #from model

                booking.save()

                context={

                            "amount":total_amount,

                            "currency":"INR",

                            "key_id":RZP_KEY_ID,

                            "order_id":rzp_order_id,

                            "total_payment":final_price,

                            
                        }
                        

                    
                return render(request,"payment.html",context)
            
            return redirect("booking-summary")
        

# booking summary
            
@method_decorator(decs,name="dispatch")
class BookingSummaryView(View):

    template_name="booking_summary.html"

    def get(self,request,*args,**kwargs):

        # qs=request.user.booking.all()

        qs=CarBooking.objects.filter(customer=request.user)

        return render(request,self.template_name,{"booking_item":qs})


@method_decorator([csrf_exempt],name="dispatch")
@method_decorator(decs,name="dispatch")

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


@method_decorator(decs,name="dispatch")   
class SignOutView(View):

    def get(self,request,*args,**kwargs):

        logout(request)

        return redirect("signin")
