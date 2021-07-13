from django.shortcuts import render,HttpResponse
from .models import *
from django.contrib.auth import authenticate
from bidding.views import *
from passlib.hash import pbkdf2_sha256
# Create your views here.
def Register(request):
    if request.method == 'POST':
        username = request.POST["user"]   
        first_name = request.POST["fname"]
        last_name = request.POST["lname"]
        email = request.POST["em"]
        password= request.POST["pw"]
        state= request.POST["st"]
        city= request.POST["city"]
        pincode= request.POST["pc"]
        phonenumber= request.POST["pho"]
        flag= request.POST["exampleRadios"]
        print(flag)
        if flag == "option2":
            new_user=User.objects.create_user(
                username = username,
                first_name = first_name,
                last_name = last_name,
                email = email,
                password= password,
                state= state,
                city= city,
                pincode= pincode,
                phonenumber= phonenumber,
                is_Farmer=True,
                is_Trader=False,
                is_Admin=False
            )
        if flag == "option1":
            new_user=User.objects.create_user(
                username = username,
                first_name = first_name,
                last_name = last_name,
                email = email,
                password= password,
                state= state,
                city= city,
                pincode= pincode,
                phonenumber= phonenumber,
                is_Farmer=False,
                is_Trader=True,
                is_Admin=False
            )

        return render(request,'login.html')
    
    else :
        return render(request,'register.html')

def login(request):
    if request.method=="POST":
        email=request.POST['email']
        password=request.POST['password']
        flag = authenticate(email=email,password=password)
        print(flag)
        user=User.objects.filter(email=email).values()
        dist=user[0]
        print(dist['is_Trader'])
        if flag is not None:
            if dist['is_Trader'] :
                request.session['user'] = email
                request.session['role'] = 'Trader'
                return redirect('bid')
            if dist['is_Farmer'] :
                request.session['user'] = email
                request.session['role'] = 'Farmer'
                return redirect('index')
            else :
                return HttpResponse("ADMIN")
    else:
        return render(request,'login.html')

def logout(request):
    try :
        del request.session['user']
        del request.session['role']
    except:
        return redirect('login')
    return redirect('login')

