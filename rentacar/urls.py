"""
URL configuration for rentacar project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from store import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    path('',views.LandingPageView.as_view(),name="home"),

    path('aboutus/',views.AboutUsView.as_view(),name="aboutus"),

    path('sevices/',views.ServicesView.as_view(),name="services"),



    path('register/',views.SignUpView.as_view(),name="signup"),

    path('verify/otp/',views.VerifyEmailView.as_view(),name="verify-email"),

    path('signin/',views.SignInView.as_view(),name="signin"),

    path('carlist/',views.CarListView.as_view(),name="car-list"),

    path('car/<int:pk>/',views.CarDetailView.as_view(),name="car-detail"),

    path('car/<int:pk>/booking/',views.CarBookingConfirmView.as_view(),name="booking-confirm"),

    path('booking/summary/',views.BookingSummaryView.as_view(),name="booking-summary"),
    

    path('payment/verify/',views.PaymentVerificationView.as_view(),name="payment-verify"),

    path('car/<int:pk>/remove/',views.CarDeleteView.as_view(),name="car-delete"),

    path('signout/',views.SignOutView.as_view(),name="signout"),



    

    

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

