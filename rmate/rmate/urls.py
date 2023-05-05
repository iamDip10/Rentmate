"""rmate URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path, include
from rm import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path("", views.landingpage, name="landing"),
    path("aboutus/", views.aboutus, name="about"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutPage, name='logout'),
    path('register/', views.register, name="register"),
    path("p_dashboard/<str:phn>", views.dashboardR , name="dashP"),
    path("makecomplain/<str:phn>", views.makecomplain, name="complain"),
    path("payrent/<str:phn>", views.payrent, name="rent"),
    path("save/<str:phn>", views.savedata, name="save"),
    path("complain/<str:phn>", views.complain, name="submit_complain"),
    path("payment/<str:phn>", views.payment, name="payment"),
    path("notification/<str:phn>", views.noti, name="noti"),
    path("maps/<str:phn>", views.maps, name="maps"),
    path("setting/<str:phn>", views.settings, name="setting"),
    path("f_auth/<str:phn>", views.authfactor, name="authfactor"),
    path("sendotp/<str:phn>", views.sendotp, name="sendotp"),
    path("changepass/<str:phone>", views.passchange, name="chngpss"),
    path("ownerdahs/<str:number>", views.bwdash, name="b_dash"),
    path("rating/<str:phn>", views.rate, name="rate"),
    path("bcomplains/<str:number>", views.bcomplain, name="bcomp"),
    path("bcomplains_month/<str:number>", views.bcomplain_m, name="bcomp_m"),
    path("bcomplains_apps/<str:number>", views.bcomplain_a, name="bcomp_a"),
    path("bcomplains_sts/<str:number>", views.bcomplain_s, name="bcomp_s"),
    path("bcomplains_solved/<str:number>/<str:pk>", views.bcomplain_solv, name="bcomp_solv"),
    path("bpayments/<str:number>", views.bpayments, name="bpay"),
    path("bpayments_s/<str:number>", views.bpayments_s, name="bpay_s"),
    path("bpayments_a/<str:number>", views.bpayments_a, name="bpay_a"),
    path("bpayments_m/<str:number>", views.bpayments_m, name="bpay_m"),
    path("renters/<str:number>", views.renters_view, name="renters"),
    path("store/<str:number>", views.store, name="storein"),
    path("ratestar/<str:number>/<str:user>", views.ratestar, name="rate_s"),
    path("houseup/<str:number>", views.houseup, name="houseup"),
    path("bsettings/<str:number>", views.bsettings, name="bsettings"),
    path("bgeneralsettings/<str:number>", views.bgenralsettngs, name="bgsettings"),
    path("bsecuritysettings/<str:number>", views.bsecuritysettings, name="bssettings"),
    path("authOTP/<str:number>", views.authOTP, name="auth"),
    path("validate/<str:number>", views.validate, name="validate"),
    path("addapt/<str:number>", views.addapt, name="addapt"),
    path("advertisment/<str:number>", views.advertisments, name="adds"),
    path("sendnotice/<str:to>/<str:num>", views.sendnotice, name="sendnotice"),
    path("blogout/", views.blogout, name="loout"),
    path("search/", views.search, name="search"),
    path("waitforapproval/", views.waitforapproval_, name="wait"),
    path("approve/<str:to>/<str:num>", views.approve, name="approve"),
    path("decline/<str:to>/<str:num>", views.decline, name="decline"),
    path("messmember/", views.messmember, name="mess_m"),
    path("messleader/", views.messleader, name="mess_l"),
    path("adminsetting/", views.admins, name="admins"),
    path("adminpayment/", views.adminp, name="adminp"),
    path("adminmain/", views.adminm, name="adminm"),
    path("report/<str:phn>", views.report_, name="report"),
    

    path("__reload__/", include("django_browser_reload.urls")),
    
   
]

if settings.DEBUG:  
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  
