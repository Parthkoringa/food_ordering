from django.shortcuts import render,redirect
from .forms import Registration
from django.contrib import messages
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.forms import AuthenticationForm

# Create your views here.
def home(request):
    return render(request,'home.html')

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
