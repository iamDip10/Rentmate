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
    path("aboutus/", views.aboutus, name=""),
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
   

    path("__reload__/", include("django_browser_reload.urls")),
]

if settings.DEBUG:  
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  
