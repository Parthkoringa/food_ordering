from django.shortcuts import render,redirect
from .forms import Registration
from login.models import Product,CustomeUser
from django.contrib import messages
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.forms import AuthenticationForm
from math import ceil

def landing(request):
    return render(request,'index.html')

def home(request):
    restaurants = CustomeUser.objects.filter(usertype='restaurant')
    
    context = {
        'restaurants' : restaurants,
    }
    return render(request,'home.html',context)

def rest_prod(request,id):
    objects = Product.objects.filter(user=id)
    context = {
        'products' : objects,
        'id': id,
    }
    return render(request,'rest_prod.html',context)


def register(request):
    if request.method == "POST":
        form = Registration(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful." )
            return redirect('login:home')
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = Registration()
    return render(request,'register.html',{'register_form' : form})

def logout_req(request):
    logout(request)
    messages.info(request,"You have successfully loged out!")
    return redirect("login:landing")


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("login:home")
            else:
                messages.error(request,"Invalid username or password.")
        else:
            messages.error(request,"Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="login.html", context={"login_form":form})


def search(request):
    key = request.POST['search']
    restaurants = CustomeUser.objects.filter(username=key)
    context = {
        'restaurants' : restaurants,
    }
    return render(request,'home.html',context)
    