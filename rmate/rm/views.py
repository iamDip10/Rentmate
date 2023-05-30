from django.shortcuts import render, redirect
from urllib.parse import urlencode
from django.urls import *
from django.http import*
from django.core import signing
from django.conf import settings as con_set
from .models import *
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
    return render(req, "index.html")

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
            own = Pro_owner.objects.get(number = phnn)
            if passs == own.psword:
                req.session['owner'] =phnn
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
        files = ResRent.objects.filter(user_id = real_v)
        obj = json.dumps(list(pay.values()))
        noti = Notifications.objects.filter(user = real_v) 
        noti_dump = noti.filter(status="unread").count()
        
        print(files, objtt)
        data = {
            'owner' : objtt,
            'key' : val,
            'pay': obj, 
            'noti': noti,
            'cont': noti_dump,
            'files':files,
            'fname':files.values('files')
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
        
        rta = rating.objects.get(residnt = objtt)
        _rate = json.dumps(rta.rate)
        data = {
            'owner' : objtt,
            'key' : val,
            'comp': comp,
            'year': ye,
            'solve':s_solve,
            'noti': noti,
            'cont':cnt,
            'rate' : _rate,
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
        aid = req.POST.get("aid", None)
        
        if typ == "Residant":
            res = Residant(fname = f_name, lname = lname, gender = gen, phn = phn, mail = mail, psword = passs, p_addrs = p_add, div = div, area = "madaripur", nid = nid, hown = Pro_owner.objects.get(number = hid), apps = apartment.objects.get(id = aid+"-"+hid))
            print(res)
            
            res.save()
            activ = activity(user = res)
            activ.save()
            _rat = rating(residnt = res, owner = res.hown) 
            _rat.save() 
            apps = apartment.objects.get(id = aid+"-"+hid)
            apps.occupy = "YES"
            apps.save()
        
        if typ == "Property owner":
            p_owner = Pro_owner(fname = f_name, lname = lname, gender = gen, number = phn, mail = mail, psword = passs, p_addrs = p_add, div = div, area = "madaripur", nid = nid, hid = hid )
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
    u = Residant.objects.get(phn=real) 
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
        com = Complain(date = datee, prob_type = typee, prob_desc = des, user=Residant.objects.get(phn=real), year=year, nei_ID = ne_id, owner = u.hown, app = u.apps )
        com.save() 

    return redirect ("complain", phn=id)

def rate(req, phn):
    phone = signing.loads(phn, key=key)
    res = Residant.objects.get(phn = phone)
    print(res.hown)   
    if req.method == "POST":
        _rat = req.POST['rating']
        if req.POST['text'] != "" :
            _comnt = req.POST['text'] 
        else:
            _comnt = "" 
        rat_obj = rating.objects.get(residnt = res)
        print(rat_obj)
        
        rat_obj.rate = _rat 
        rat_obj.commnt = _comnt
        rat_obj.save() 
        
    return redirect('complain', phn=phn)
        
        


def payment(req, phn):
    real = signing.loads(phn, key=key)
    if req.method == "POST":
        datee = str(req.POST['date']) 
        strr = datee.split("-")[1]
        # uniqID = real + "-" + datee.split("-")[0] + "-" + datee.split("-")[1]
        res = ResRent.objects.filter(user_id = real).filter(month = calendar.month_name[int(strr)])
  
        res.update(date = datee, status = "PAID", paymentID = uuid.uuid1().hex) 
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
    user_ = Residant.objects.get(phn = signing.loads(phn, key=key))
    p_otp = req.POST['OTP'] 
    if p_otp ==  user_.OTP:
        user_.authheticate = "YES" 
        user_.save() 
        obj = otherActivity(user = user_, activ_time = datetime.datetime.now().strftime("%d-%m-%Y, %I:%M%p"), msg = "You have turned on two factor authentication!")
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
    if 'owner' in req.session:    
        phn = signing.loads(number, key=key)
        filter_r = Residant.objects.filter(hown_id = phn )
        obj = Pro_owner.objects.get(number = phn)
        _set = rating.objects.filter(owner_id=obj).values('rate').annotate(count = Count('rate'))
        fres = list(_set.values('rate', 'count'))
        jsons = json.dumps(fres) 
        cmnts = rating.objects.all()
        datee = datetime.datetime.now().month
        alltime = ResRent.objects.filter(owner_id = phn).filter(status='PAID').aggregate(sum = Sum('amount'))
        mothly = ResRent.objects.filter(owner_id = phn).filter(status = 'PAID').filter(month = calendar.month_name[datee]).aggregate(sum = Sum('amount'))
        yyear = ResRent.objects.filter(owner_id = phn).filter(status = 'PAID').filter(year = str(datetime.datetime.now().year)).aggregate(sum = Sum('amount'))
        apps = apartment.objects.filter(owner_id = phn)
        occupyy = apartment.objects.filter(occupy = "YES").annotate(count = Count("occupy"))
        adverr = apartment.objects.filter(adver = "YES")
        noccupy = apps.count() - occupyy.count()
        filter_notpaid = ResRent.objects.filter(owner_id = phn).filter(status = "NOT PAID").annotate(Count('status')) 
        filter_paid = ResRent.objects.filter(owner_id = phn).filter(status = "PAID").annotate(Count('status')) 

        data = {
            'mom' : obj,
            'jsonn': jsons,
            'cmnts': cmnts, 
            'alltime':alltime,
            'month': mothly,
            'year': yyear,
            'ttotal': apps.count(),
            'occupy': occupyy, 
            'noccupy': noccupy,
            'paid': filter_paid.count(),  
            'notpaid': filter_notpaid.count(),
            'num': number,
            'adver': adverr.count(),
        }
        return render(req, 'bwdashboard.html', data) 
    return redirect('login')
         


def bcomplain(req, number) :
    
    if 'owner' in req.session:
        phn = signing.loads(number, key=key)
        
        owner = Pro_owner.objects.get(number = phn)
        resdnts = Residant.objects.filter(hown_id = phn)
        complins = Complain.objects.filter(owner_id = owner)
        app = apartment.objects.filter(owner_id = owner)
        
    
        data = {
            'owner' : owner,
            'num' : number,
            'complain': complins,
            'app': app,
        }
        return render(req, 'bcomplains.html', data)
    return redirect('login')

def bcomplain_m(req, number):
    
    if 'owner' in req.session:
        month = req.GET.get('month')
        phn = signing.loads(number, key=key)
        
        owner = Pro_owner.objects.get(number = phn)
        resdnts = Residant.objects.filter(hown_id = phn)
        complins = Complain.objects.filter(owner_id = owner).filter(date__contains = "-"+ month+"-")
        app = apartment.objects.filter(owner_id = owner)
        print(month, complins)
        data = {
            'complain': complins,
            "num":number,
        }
        return render(req, 'sort_by_month.html', data)
    return redirect('login')

def bcomplain_s(req, number):
    
    if 'owner' in req.session:
        sts = req.GET.get('status')
        phn = signing.loads(number, key=key)
        
        owner = Pro_owner.objects.get(number = phn)
        resdnts = Residant.objects.filter(hown_id = phn)
        complins = Complain.objects.filter(owner_id = owner).filter(slv_status = sts)
        app = apartment.objects.filter(owner_id = owner)
        print(sts, complins)
        data = {
            'complain': complins,
            "num":number,
        }
        return render(req, 'sort_by_month.html', data)
    return redirect('login') 

def bcomplain_a(req, number):
    
    if 'owner' in req.session:
        apps = req.GET.get('apps')
        phn = signing.loads(number, key=key)
        
        owner = Pro_owner.objects.get(number = phn)
        resdnts = Residant.objects.filter(hown_id = phn)
        complins = Complain.objects.filter(owner_id = owner).filter(app_id = apps)
        app = apartment.objects.filter(owner_id = owner)
        print(apps, complins)
        data = {
            'complain': complins,
            "num":number,
        }
        return render(req, 'sort_by_month.html', data)
    return redirect('login')

def bcomplain_solv(req, number, pk) :
    comp = Complain.objects.get(comID = pk)
    comp.slv_status = "Solved"
    comp.save()
    return redirect('bcomp', number=number)

def bpayments(req, number) :
    if 'owner' in req.session:
        phn = signing.loads(number, key=key)
        
        owner = Pro_owner.objects.get(number = phn)
        resdnts = Residant.objects.filter(hown_id = phn)
        app = apartment.objects.filter(owner_id = owner)
        today_date = datetime.datetime.now().month
        total_rev = ResRent.objects.filter(owner_id = owner).filter(status = "PAID").aggregate(sum = Sum('amount'))
        month_rev = ResRent.objects.filter(owner_id = owner).filter(status = "PAID").filter(month = calendar.month_name[today_date]).aggregate(sum = Sum('amount'))
        due_payments = ResRent.objects.filter(owner_id = owner).filter(status = "NOT PAID").filter(month = calendar.month_name[today_date])
        
        pay = ResRent.objects.filter(owner_id = owner)
        data = {
            'num': number,
            'owner': owner,
            'total_rev': total_rev,
            'month_rev': month_rev,
            'due_pay' : due_payments,
            'month' : calendar.month_name[today_date],
            'apps': app,
            'pay': pay,
        }
        return render(req, 'bpayments.html', data)
    return redirect('login')

def bpayments_s (req, number) :
    if 'owner' in req.session:
        val = req.GET.get('sts')
        phn = signing.loads(number, key=key)
        
        owner = Pro_owner.objects.get(number = phn)
        if val != "":
            pay = ResRent.objects.filter(owner_id = owner).filter(status = val)
        else:
            print("HELLO")
            pay = ResRent.objects.filter(owner_id = owner)
        
        data = {
            'num' : number,
            'pay': pay,
        }
        return render(req, 'sort_pay.html', data)
    return redirect('login')

def bpayments_a(req, number):
    
    if 'owner' in req.session:
        val = req.GET.get('app')
        phn = signing.loads(number, key=key)
        
        owner = Pro_owner.objects.get(number = phn)
        if val != "":
            pay = ResRent.objects.filter(owner_id = owner).filter(apps = val)
        else:
            pay = ResRent.objects.filter(owner_id = owner)
        print(val.upper())
        data = {
            'num' : number,
            'pay': pay,
        }
        return render(req, 'sort_pay.html', data)
    return redirect('login')

def bpayments_m(req, number):
    
    if 'owner' in req.session:
        val = req.GET.get('app')
        phn = signing.loads(number, key=key)
        
        owner = Pro_owner.objects.get(number = phn)
        if val != "":
            pay = ResRent.objects.filter(owner_id = owner).filter(month = val)
        else:
            pay = ResRent.objects.filter(owner_id = owner)
        print(val.upper())
        data = {
            'num' : number,
            'pay': pay,
        }
        return render(req, 'sort_pay.html', data)
    return redirect('login')


def renters_view(req, number) :
    
    if 'owner' in req.session:
        phn= signing.loads(number, key=key)
        
        owner = Pro_owner.objects.get(number= phn)
        res = Residant.objects.filter(hown_id = owner)
        jsonn = json.dumps(list(res.values()))
        complt = ResRent.objects.filter(month = calendar.month_name[datetime.datetime.now().month]).filter(owner_id = phn).filter(status = "PAID")
        
        print(jsonn)
        data = {
            'num' : number,
            'owner': owner,
            'apps': jsonn,
            'res':res,
            'paycomplt': complt,
        }
        return render (req, 'renters.html', data)
    return redirect('login')


def store(req, number) :
    datee = datetime.datetime.now() 
    if req.method == "POST":
        month = req.POST['month_select']
        res = req.POST['res']
        amount = req.POST['amount']
        deadline = str(calendar.monthrange(datee.year, datetime.datetime.strptime(month, "%B").month)[1]) + "-" + str(datetime.datetime.strptime(month, "%B").month) +"-"+ str(datee.year)
        id = res+"-"+str(datetime.datetime.strptime(month, "%B").month)+"-"+str(datee.year)
        hous_own = Pro_owner.objects.get(number=signing.loads(number, key=key))
        year = datee.year
        apps = Residant.objects.get(phn = res).apps
        if 'filename' in req.FILES:
            files = req.FILES['filename']
        else:
            files = "-"
            
        
        res_obj = ResRent(amount = amount, status = "NOT PAID", deadline = deadline, month = month, user = Residant.objects.get(phn = res), uniqID = id, owner = hous_own, year = year, apps = apps, files = files)
        
        res_obj.save()
        
        
        
    return redirect('renters', number=number)


def ratestar(req, number, user) :
    
    usr = Residant.objects.get(phn=user)
    usr.rate = req.POST['rating']
    usr.save()
        
     
    return redirect('renters', number=signing.dumps(number, key=key))

def houseup(req, number):
    
    if 'owner' in req.session:
        owner = Pro_owner.objects.get(number=signing.loads(number, key=key))
        apps = apartment.objects.filter(owner_id = owner).filter(occupy = "NO").filter(adver = "NO")
        apps_o = Residant.objects.filter(hown_id = owner)
        apps_a = apartment.objects.filter(owner_id = owner).filter(adver = "YES")
        wait = waitforapproval.objects.filter(owner = signing.loads(number, key=key))
        data = {
            'num':number,
            'own' : owner,
            'apps': apps,
            'o': apps_o,
            'a': apps_a,
            'wait':wait,
        }
        return render(req, 'houseupgrade.html', data)
    return redirect('login')

def bsettings(req, number):
    
    if 'owner' in req.session:
        owner = Pro_owner.objects.get(number = signing.loads(number, key=key))
        
        data= {
            'ownn' : owner,
            'num': number,
        }
        return render(req, 'bsettings.html', data)
    return redirect('login')

def bgenralsettngs (req, number) :
    owner = Pro_owner.objects.get(number = signing.loads(number, key=key))
    
    if req.method == "POST":
        if 'profpic' in req.FILES:
            owner.picc = req.FILES['profpic']
        if req.POST['fname'] != "":
            owner.fname = req.POST['fname']
        if req.POST['lname'] != "":
            owner.lname = req.POST['lname']
        if req.POST['address'] != "":
            owner.p_addrs = req.POST['address']
        if req.POST['mobile'] != "":
            owner.number = req.POST['mobile']
        if req.POST['mail'] != "" :
            owner.mail = req.POST['mail']
        owner.save()   
    return redirect('bsettings', number = number)

def bsecuritysettings(req, number):
    owner = Pro_owner.objects.get(number = signing.loads(number, key=key))
    
    if req.method == "POST" :
        if req.POST['opass'] != "":
            if req.POST['opass'] == owner.psword:
                if req.POST['npass'] == req.POST['rnpass']:
                    owner.psword = req.POST['npass']
                    owner.save()
    
    return redirect('bsettings', number=number)


def authOTP (req, number) :
    owner = Pro_owner.objects.get(number = signing.loads(number, key=key))
    fullname = owner.fname + " " + owner.lname
    ran = random.randint(1000, 9999)
    owner.otp = str(ran)
    owner.save()
    subject = "Two factor authorization"
    message = "Dear "+fullname+ "\nThanks for using two factor authorization in your account. Your OTP is " + str(ran)+ ". Kindly provide this OTP to validate.\n\nThanks,\nRentemate."
    sndobj = sendmail(subject, message, con_set.EMAIL_HOST_USER, owner.mail )
    sndobj._send()
    return redirect('bsettings', number=number)

def validate (req, number):
    owner = Pro_owner.objects.get(number = signing.loads(number, key=key))
    
    if req.method =="POST":
        otp = req.POST['otp']
        if (otp == owner.otp):
            owner.twofact = "TURNED ON"
            owner.save() 
    return redirect ('bsettings', number=number)

def addapt(req, number ):
    own = Pro_owner.objects.get(number = signing.loads(number, key=key))
    if req.method == "POST":
        id = req.POST['id']+"-"+own.number 
        bed = req.POST['bed'] 
        bath = req.POST['bath']
        livin = req.POST['living']
        kitchen =req.POST['kitchen']
        bill = req.POST['bill']
        apps = apartment(id = id, owner = own, bed = bed , bath = bath, living = livin, kitchen = kitchen, occupy = "NO", bill=bill)
        apps.save()
    return redirect('houseup', number=number)

def advertisments(req, number):
    
    own = Pro_owner.objects.get(number = signing.loads(number, key=key))
    
    if req.method == "POST":
        app = req.POST['app_select'].upper()
        if 'picss_' in req.FILES:
            pik = req.FILES['picss_']
        print(app+"-"+own.number)
        apss = apartment.objects.get(id = app)
        apss.adver = "YES"
        apss.save()
        objeet = advertisment(apart = apartment.objects.get(id = app), picss = pik, owner = own, bill=apss.bill, area = own.area, number = own.number, address = own.p_addrs, bed = apss.bed, kitchen = apss.kitchen, bathroom = apss.bath, lroom = apss.living )
        objeet.save()  
          

    return redirect('houseup', number=number)
    
def sendnotice(req, to, num):
    n = Pro_owner.objects.get (number = signing.loads(num, key=key))
    too = Residant.objects.get(phn = to)
    messg = "Dear "+too.fname +" " + too.lname + "\nI am Mr. "+ n.fname+" "+n.lname + " and very sorry to say you have to leave your apartment within next month\n\nThanks,\n"+ n.fname+" "+n.lname 
    subject = "Notice of leaving apartment"
    obj = sendmail(subject, messg, con_set.EMAIL_HOST_USER, too.mail)
    obj._send() 
    return redirect('houseup', number = num)

def search(req):
    adver = advertisment.objects.filter(apart__occupy = "NO" )
    print(adver)
    jsonn = json.dumps(list(rating.objects.all().values()))
    jso = json.dumps(list(adver.values()))
    data = {
        'adver': adver,
        'js': jsonn,
        'j':jso,
    }
    return render (req, 'searchpage.html', data)

def waitforapproval_(req):
    if req.method == 'POST':
        apid = req.POST['apid']
        name = req.POST['name'] 
        nid = req.POST['nid']
        mail = req.POST['mail']
        num = req.POST['num']
        
        wait = waitforapproval(name = name, nid = nid, apps = apid, owner = num, email = mail)
        wait.save()
        
        return redirect('search')
    
def approve(req, to, num):
    owner = Pro_owner.objects.get(number= signing.loads(num, key=key))
    too = to
    messg = "Dear,\nI am Mr. "+ owner.fname+" "+owner.lname + " and happy to say you that we can reach an agreement regarding your request of renting apartment. Kindly goto the rentmate website and signup with your informations. \n\nKindly place "+owner.number +" as house owner number and the apartment ID you choose.\n\nThanks,\n"+ owner.fname+" "+owner.lname 
    subject = "Acceptance of the agreement"
    obj = sendmail(subject, messg, con_set.EMAIL_HOST_USER, too)
    obj._send() 
    
    return redirect('houseup', number=num)

def decline(req, to, num):
    owner = Pro_owner.objects.get(number= signing.loads(num, key=key))
    too = to
    messg = "Dear,\nI am Mr. "+ owner.fname+" "+owner.lname + " and sorry to say you that we can not reach an agreement regarding your request of renting apartment. We need to meet face-to-face then we can talk about it furthur.\n\nThanks,\n"+ owner.fname+" "+owner.lname 
    subject = "Decline of the agreement"
    obj = sendmail(subject, messg, con_set.EMAIL_HOST_USER, too)
    obj._send() 

    userr = waitforapproval.objects.filter(email = to)
    userr.delete()
    
    return redirect('houseup', number=num)

def messmember(req):
    return render(req, 'messmember.html')
def messleader(req):
    return render(req, 'messleader.html')

def adminm(req):
    return render(req, 'adminmain.html')
def adminp(req):
    rep = report.objects.all()
    data = {
        'cnt': rep.count(),
        'obj': rep,
    }
    
    return render(req, 'adminpayment.html', data)
def admins(req):
    return render(req, 'adminsettings.html')

def report_(req, phn):
    user = Residant.objects.get(phn = signing.loads(phn, key=key))
    own = Pro_owner.objects.get(number = user.hown_id)
    if req.method == "POST":
        prob = req.POST['text_']
        
        report(prob = prob, user = user, owner = own ).save()
    return redirect('complain', phn=phn )

def blogout(req):
    
    req.session.flush() 
    
    return redirect('login')