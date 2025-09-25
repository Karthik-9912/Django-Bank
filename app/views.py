from django.shortcuts import render , HttpResponse ,redirect
from .forms import RegisterForm
from django.core.mail import send_mail
from django.conf import settings
from .models import BankDetails
from random import randint
import hashlib




# Create your views here.

def encrypt(request):
    return hashlib.shake_256(str(pin).encode()).hexdigest(length=16)

def index(request):
    return render(request,'index.html')

def create(request):
    form=RegisterForm()
    if request.method=='POST':
        form=RegisterForm(request.POST,request.FILES)
        if form.is_valid():
            email=request.POST.get('email')
            form.save()
            # print(email)
            data=BankDetails.objects.get(email=email)
            send_mail('Account Creation Successful',f'Dear User, Thank your for creating the account.Welcome to the SBI Bank. \n This is Your Account Number {data.acc_num} \n Best Regards \n SBI Manager (Karthik)',settings.EMAIL_HOST_USER,[email],fail_silently=False)
    context={
        'form':form
    }
    return render(request,'create.html',context)

def pin(request):
    msg=""
    data=None
    if request.method=='POST':
        acc_num=request.POST.get('acc')
        try:
            data=BankDetails.objects.get(acc_num=acc_num)
        except:
            msg="Please check your account number"
        if data:
            otp=randint(100000,999999)
            send_mail(f"THIS IS THE ONE TIME PASSWORD FOR PIN GENERATION {otp}","\n Regards \n SBI Manager (Karthik)",settings.EMAIL_HOST_USER,[data.email],fail_silently=False)
            request.session['otp']=otp
            request.session['acc']=data.acc_num
            return redirect("validate")
    context={
        'msg':msg
    }

    return render(request,'pin.html',context)

def validate(request):
    msg=""
    if request.method=="POST":
        c_otp=int(request.session['otp'])
        otp=int(request.POST.get('otp'))
        confirmotp=int(request.POST.get('confirmotp'))
        if otp==confirmotp:
            if otp==c_otp:
                return redirect("set")
            else:
                msg="Incorrect otp"
        else:
            msg="otp and confirm otp didn't match"

    context={
        'msg':msg
    }
    return render(request,'validate.html',context)

def set_pin(request):   
    if request.method=="POST":
        pin=request.POST.get('pin')
        cpin=request.POST.get('cpin')
        if pin==cpin:
            session_acc=request.session['acc']
            data=BankDetails.objects.get(acc_num=session_acc)
            data.pin=encrypt(pin)
            data.save()
            return redirect("index")
    return render(request,'setPin.html')

def deposit(request):
    msg=""
    data=None
    if request.method=="POST":
        acc=request.POST.get('acc')
        pin=request.POST.get('pin')
        amt=request.POST.get('amt')

        try:
            data=BankDetails.objects.get(acc_num=acc)
        except:
            msg="Account NOt found"
        if data:
            epin=encrypt(pin)
            if data.pin==epin:
                if int(amt)>=100 and int(amt)<=10000:
                    data.balance+=int(amt)
                    data.save()
                    return redirect("index")
                else:
                    msg="You exceeded the aomunt range "
            else:
                msg="Incorrect Pin"
    context={
        'msg':msg
    }
    return render(request,'deposit.html',context)

def balance(request):
    data=None
    msg=""
    if request.method=="POST":
        acc=request.POST.get('acc')
        pin=request.POST.get('pin')
        try:
            data=BankDetails.objects.get(acc_num=acc)
        except:
            msg="Account Not Found"
        if data:
            cpin=encrypt(pin)
            if data.pin == cpin:
                msg=f"ur balance is {data.balance}"
            else:
                msg="Pin INvalid"
    context={
        'msg':msg
    }

    return render(request,'balance.html',context)