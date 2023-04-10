from django.shortcuts import render, redirect
from urllib.parse import urlencode
from django.urls import *
from django.http import*
from django.core import signing
from django.conf import settings as con_set
from .models import Residant, Pro_owner, Complain, ResRent, Notifications, activity, otherActivity
from datetime import date, datetime
from django.db.models import *
import json
from django.contrib.auth import authenticate, login, logout 
import uuid
import calendar
import gmplot
from django.contrib.auth.decorators import login_required
import random
from rm.sendmail import *
import datetime

key = "011201171"
def landingpage(req):
    return render(req, "landing.html")

def aboutus(req):
    return render(req, "aboutus.html")

def loginPage(req):
    if req.method == "POST":
        typee = req.POST['typp']
        phnn = req.POST['__phn']
        passs = req.POST['__pass']
        res = ''
        #req.POST['csrfmiddlewaretoken'] = req.COOKIES.get('csrftoken')
        if typee == "Residant":
            
            res = Residant.objects.get(phn=phnn)
            if res.psword == passs:
                active = activity.objects.get(user = phnn) 
                active.last_login = str(datetime.datetime.now().strftime("%d-%m-%Y, %I:%M%p"))
                active.last_log_time = str(datetime.datetime.now().strftime("%H:%M"))
                active.save()
                ecnr = signing.dumps(res.phn, key=key)
                req.session['residant'] = phnn
                return redirect('dashP', phn=ecnr)
        elif typee == "Property owner":
            own = Pro_owner.objects.get(phn = phnn)
            if passs == own.psword:
                encrp = signing.dumps(phnn, key=key) 
                return redirect('b_dash', number = encrp)
    return render(req, "loginn.html") 



def dashboardR(req, phn):
    if 'residant' in req.session:
        real_val = signing.loads(phn, key=key)
        objt = Residant.objects.get(phn = real_val)
        noti= Notifications.objects.filter(user = real_val)
        noti_dump = noti.filter(status='unread').count()
        data = {
            'obj' : objt,
            'enp' : phn,
            'noti': noti,
            'cont':noti_dump,
        }
        return render (req, "dashboardmain.html", data)
    return redirect('login')

def payrent(req, phn):
    if 'residant' in req.session:
        val = phn
        real_v = signing.loads(val, key=key)
        objtt = Residant.objects.get(phn=real_v)
        pay = ResRent.objects.filter(user_id = real_v)
        obj = json.dumps(list(pay.values()))
        noti = Notifications.objects.filter(user = real_v) 
        noti_dump = noti.filter(status="unread").count()
        
        print(pay)
        data = {
            'owner' : objtt,
            'key' : val,
            'pay': obj, 
            'noti': noti,
            'cont': noti_dump,
        }
        
        return render(req, "payrent.html", data)
    return redirect('login')

def makecomplain(req, phn):
    if 'residant' in req.session:
        val = phn
        real_v = signing.loads(val, key=key)
        objtt = Residant.objects.get(phn=real_v)
        comp = Complain.objects.filter(user_id = real_v) #filtering the complains of particular users. returns <queryset>
        yearr = comp.values("year").annotate(count=Count("year")) #grouping the year along with counting them
        ye = json.dumps(list(yearr.values('year', 'count'))) #converting to json
        
        f_solve = comp.filter(slv_status = "solved")
        g_solve = f_solve.values("year").annotate(cntt = Count('year'))
        
        s_solve = json.dumps(list(g_solve.values('year', "cntt")))
        noti = Notifications.objects.filter(user = real_v)
        cnt = noti.filter(status='unread').count()
        print(cnt) 
        data = {
            'owner' : objtt,
            'key' : val,
            'comp': comp,
            'year': ye,
            'solve':s_solve,
            'noti': noti,
            'cont':cnt,
        }
        return render(req, "makecomplain.html", data)
    return redirect('login')

def register(req):
    if req.method == "POST":
        typ = req.POST["typ"]
        f_name = req.POST["fname"]
        lname = req.POST["lname"]
        gen = req.POST["gender"]
        phn = req.POST["phn"]
        mail = req.POST["mail"]
        passs = req.POST["pass"]
        p_add = req.POST["paddrs"]
        div = req.POST["test"]
        area = req.POST["test_"]
        nid = req.POST["NID"]
        hid = req.POST.get("houseid", None)
        
        if typ == "Residant":
            res = Residant(fname = f_name, lname = lname, gender = gen, phn = phn, mail = mail, psword = passs, p_addrs = p_add, div = div, area = "madaripur", nid = nid )
            res.save()
        
        if typ == "Property owner":
            p_owner = Pro_owner(fname = f_name, lname = lname, gender = gen, phn = phn, mail = mail, psword = passs, p_addrs = p_add, div = div, area = "madaripur", nid = nid, hid = hid )
            p_owner.save()
        return redirect("login")
           
    return render(req, "register.html") 

def savedata(req, phn):
    val = signing.loads(phn, key=key)
    res = Residant.objects.get(phn=val)
    if req.method == "POST":
        
        if req.POST['uname'] != "":
            res.uname = req.POST['uname']
        if req.POST['fname'] != "":
            res.fname = req.POST['fname']
        if req.POST['mail']!= "":
            res.mail = req.POST['mail']
        if req.POST['lname']!= "":
            res.lname = req.POST['lname']
        if req.POST['per_add']!= "":
            res.per_addrs = req.POST['per_add']
        if req.POST['abt_me']!= "":
            res.about_me = req.POST['abt_me']
        if req.POST['phn']!= "":
            res.phn = req.POST['phn']
        if req.POST['add']!= "":
            res.p_addrs = req.POST['add']
        if 'image' in req.FILES:
            res.image = req.FILES['image']    
        res.save()   
           
    return redirect("dashP", phn=phn)

def complain(req, phn):
    id = phn
     
    real = signing.loads(id, key=key)
    if req.method == "POST":
        
        datee = date.today().strftime("%Y-%m-%d")
        typee = req.POST['typeS']
        des = req.POST['texta']
        year = datee.split("-")[0]
        if req.POST['nb'] != "":
            ne_id = req.POST['nb']
        else:
            ne_id = "null"
        print(ne_id)
        com = Complain(date = datee, prob_type = typee, prob_desc = des, user=Residant.objects.get(phn=real), year=year, nei_ID = ne_id)
        com.save() 

    return redirect ("complain", phn=id)

def rate(req, phn):
    phone = signing.loads(phn, key=key)
    if req.method == "POST":
        _rating = req.POST['rating']
        


def payment(req, phn):
    real = signing.loads(phn, key=key)
    if req.method == "POST":
        datee = str(req.POST['date']) 
        strr = datee.split("-")[1]
        uniqID = real + "-" + datee.split("-")[0] + "-" + datee.split("-")[1]
        res = ResRent.objects.get(uniqID=uniqID)
        res.month = calendar.month_name[int(strr)]
        res.date = datee
        res.status = "PAID"
        res.paymentID = uuid.uuid1().hex
        res.save() 
        noti = "You have paid your payment of " + calendar.month_name[int(strr)] + " on " + datee
    else:
        noti = "Your payment has not been completed."
    
    noty = Notifications(notification = noti, user =Residant.objects.get(phn=real) , date = datee)
    noty.save()     
    return redirect('rent', phn=phn)  

def noti(req, phn):
    print("Updated") 
    nots = Notifications.objects.filter(user = signing.loads(phn, key=key))
    nots.update(status="read") 
    cnt = Notifications.objects.filter(user=signing.loads(phn, key=key), status="unread").count()
    return JsonResponse({'count':cnt})

def maps(req, phn):
    #gm = gmplot.GoogleMapPlotter.from_geocode("Dhaka, Bangladesh", apikey=api)
    obj = Residant.objects.get(phn = signing.loads(phn, key=key))
    data = {
        "residant" : obj,
        'key' : phn
    }
    return render(req, 'maps.html', data) 

def settings(req, phn):
    print (phn)
    if 'residant' in req.session:
        obj = Residant.objects.get(phn = signing.loads(phn, key=key))
        act = activity.objects.get(user = signing.loads(phn, key=key))
        sts = json.dumps(obj.authheticate)
        actib = activity.objects.get(user = signing.loads(phn, key=key))
        hour = int(actib.active_time / 3600)
        minn = int((actib.active_time % 3600)/60)
        oa = otherActivity.objects.filter(user = signing.loads(phn, key=key)).values()
        print(hour, minn, oa)
        
        noti = Notifications.objects.filter(user = obj)
        cnt = noti.filter(status = "unread").count()
        dataa = {
            'obj' : obj ,
            'key' : phn,
            'auth' : sts,
            'activ': act,
            'hour': hour,
            'min':minn,
            'oa' :oa,
            'noti': noti,
            "cont":cnt,
        }
        
        return render(req, "profilesettings.html", dataa) 
    return redirect('login')

def authfactor(req, phn) :
    user = Residant.objects.get(phn = signing.loads(phn, key=key))
    p_otp = req.POST['OTP'] 
    if p_otp ==  user.OTP:
        user.authheticate = "YES" 
        user.save() 
        obj = otherActivity(user = signing.loads(phn, key=key), activ_time = datetime.datetime.now().strftime("%d-%m-Y, %I:%M%p"), msg = "You have turned on two factor authentication!")
        obj.save()
    return redirect('setting', phn=phn)
    

def sendotp(req, phn):
    if 'residant' in req.session:
        
        print("OTP sent") 
        ran = random.randint(1000, 9999) 
        res = Residant.objects.get(phn = signing.loads(phn, key=key))
        email = res.mail
        fullname = res.fname +" " + res.lname 
        subject = "Two factor authorization"
        message = "Dear "+fullname+ "\nThanks for using two factor authorization in your account. Your OTP is " + str(ran)+ ". Kindly provide this OTP to validate.\n\nThanks,\nRentemate."
        obj = sendmail(subject, message, con_set.EMAIL_HOST_USER,email)
        obj._send() 
        res.OTP = ran 
        res.save() 
        return redirect('setting', phn=phn) 
    return redirect('login')
    

def passchange(req, phone):
    user = Residant.objects.get(phn = signing.loads(phone, key=key))
    if req.method == "POST":
        old = req.POST['old']
        if (old == user.psword):
            new = req.POST['new'] 
            rnew = req.POST['renew']
            if (new == rnew):
                user.psword = new
                user.save()
                obj = otherActivity(user = Residant.objects.get(phn = signing.loads(phone, key=key)), activ_time = datetime.datetime.now().strftime("%d-%m-%Y, %I:%M%p"), msg = "You have change your password!")
                obj.save()
    
    return redirect('setting', phn=phone)

# def upload(req, phn) :
#     if req.method =="POST":
#         res = Residant.objects.get(phn=signing.loads(phn, key=key))
#         #print(req.FILES["file__"].name)
#         res.image = req.FILES['pic']
#         res.save()
    
#     return redirect('dashP', phn=phn)
    
def logoutPage(req):
    activ = activity.objects.get(user = req.session['residant'])
    strt = datetime.datetime.strptime(activ.last_log_time, "%H:%M")
    now = datetime.datetime.now().strftime("%H:%M")
    delta = int ((datetime.datetime.strptime(now, "%H:%M") - strt).total_seconds())
    print(delta)
    if delta < 0:
        print("_")
        activ.active_time = 82800+delta
    else:
        activ.active_time = delta
    activ.save()
    req.session.flush()
    return redirect('login')

def bwdash(req, number) :
    phn = signing.loads(number, key=key)
    obj = Pro_owner.objects.get(phn = phn)
    
    data = {
        'mom' : obj,
    }
    return render(req, 'bwdashboard.html', data)  
