from django.shortcuts import render ,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from . models import Profile 
from django.contrib.auth import authenticate ,login as auth_login ,logout




# Create your views here.
def home(request):
    return render(request,'index.html')


def login(request):
    if request.method=='POST':
        email_input = request.POST.get('email')
        password_input =request.POST.get('password')
        try:
            user_object=User.objects.get(email=email_input)
            user_name=user_object.username
        except User.DoesNotExist:
            user_name=None

        user= authenticate(request,username=user_name,password=password_input)
        if user is not None:
            auth_login(request,user)
            return redirect('home_page')
        else:
            messages.info(request,'invalid username or password')
            return redirect('login')

    return render(request,'login.html')


def signup(request):
    if request.method =='POST':
        username= request.POST.get('username')
        email=request.POST.get('email')
        password=request.POST.get('password')
        cnf_password=request.POST.get('confirm_password')
        if cnf_password==password:
            if User.objects.filter(username=username).exists():
                messages.info(request ,'username occupied')
                return redirect('signup')
            elif User.objects.filter(email=email).exists():
                messages.info(request,'email already registered')
                return redirect('signup')
            else :
                user =User.objects.create_user(username=username ,email=email ,password= password)
                user_profile=Profile.objects.create(user=user)
                user_profile.save();
                return redirect('login')
        else:
            messages.info(request,'enter exact password')
            return redirect('signup')


    return render(request,'signup.html')


def loggout(request):
    logout(request)
    return redirect('login')