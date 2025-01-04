from django.shortcuts import render,redirect

from django.views.generic import View

from store.forms import SignUpForm,SignInForm

from django.core.mail import send_mail

from store.models import User,Car

from django.contrib import messages

from django.contrib.auth import authenticate,login,logout


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

