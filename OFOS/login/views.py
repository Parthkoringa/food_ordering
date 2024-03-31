from django.shortcuts import render,redirect
from .forms import Registration
from login.models import Product,CustomeUser,Order,Order_items
from django.contrib import messages
from django.contrib.auth import login, authenticate,logout
from django.utils.timezone import now
from django.contrib.auth.hashers import make_password
from django.http import FileResponse
from django.contrib.auth.forms import AuthenticationForm
from reportlab.pdfgen import canvas
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
    restobj = CustomeUser.objects.get(id=id)
    restname = restobj.username
    context = {
        'products' : objects,
        'id': id,
        'restname': restname,
        
    }
    return render(request,'rest_prod.html',context)

def reset_password(request):
    return render(request,'reset_password.html')

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

def profile(request,id):
    user = CustomeUser.objects.get(id=id)
    context = {
        'id': id,
        'user': user
    }
    return render(request,'profile.html',context)

def search(request):
    key = request.POST['search']
    restaurants = CustomeUser.objects.filter(username=key)
    context = {
        'restaurants' : restaurants,
    }
    return render(request,'home.html',context)
    
def reset(request):
    u_name = request.POST['username']
    pwd = make_password(request.POST['password']) 
    user = CustomeUser.objects.filter(username=u_name).update(password=pwd)  
    return redirect("login:login")


ordercontext = 0
orderitemcontext = 0
billcontext = 0
def confirm_order(request,id):
    neworder = Order()
    neworder.order_date = now()
    neworder.r_id = CustomeUser.objects.get(id=id)
    var1 = request.POST['total-price']
    var2 = var1.split("$")
    neworder.total_amt = var2[1]
    
    neworder.save()
    
    i=1
    while(True):
        stritem = "item" + (str)(i)
        if(request.POST.get(stritem)):
            # print(i)
            item = request.POST[stritem]
            lst = item.split(" ")
            newitem = Order_items()
            newitem.p_id = Product.objects.get(p_name=lst[0],user=id) 
            lst2 = lst[2].split("$")
            newitem.price = lst2[1]
            newitem.quantity=1
            newitem.o_id = neworder
            newitem.save() 
            i=i+1
        else:
            break
        
    global ordercontext,orderitemcontext
        
    ordercontext = Order.objects.get(id = neworder.id)
    orderitemcontext = Order_items.objects.filter(o_id= neworder.id)
    context = {
        'id': id,
        'ordercontext': ordercontext,
        'orderitemcontext': orderitemcontext
    }
    return render(request,'payment.html',context)
    
def bill(request):
    contact = request.POST['contact']
    email = request.POST['email']
    global ordercontext,orderitemcontext,billcontext
    billcontext={
        "ordercontext": ordercontext,
        "orderitemcontext": orderitemcontext,
        "contact": contact,
        "email": email
    }
    return render(request,'bill.html',billcontext)


def download(request):
        response = FileResponse(generate_pdf_file(request),as_attachment=True,filename="Order_bill.pdf")
        return response
        
def generate_pdf_file(request):
        from io import BytesIO
        buffer = BytesIO()
        p = canvas.Canvas(buffer)
        global ordercontext,orderitemcontext,billcontext
        var1 = ordercontext
        var2 = ordercontext.order_date
        var3 = ordercontext.total_amt
        var4 = ordercontext.order_status
        var6 = ordercontext.r_id.username
        var7 = ordercontext.r_id.address
        var5 = billcontext.get("contact")
        var8 = billcontext.get("email")
        p.drawString(50,803,f"Order Details:- ")
        p.drawString(50,773,f"Order id:- {var1}")
        p.drawString(50,753,f"Order date:- {var2}")
        p.drawString(50,733,f"Order price:- {var3}")
        p.drawString(50,713,f"Order status:- {var4}")
        p.drawString(50,693,f"Restaurant name:- {var6}")
        p.drawString(50,673,f"Restaurant address:- {var7}")
        p.drawString(50,653,f"Order status:- {var4}")
        p.drawString(50,633,f"Customer contact:- {var5}")
        p.drawString(50,613,f"Customer email:- {var8}")
        p.drawString(50,530,f"Order items:-")
        for i in orderitemcontext:
            count = 1
            var6 = 500
            p.drawString(50,var6,f"item{count}:-  {i.p_id.p_name} -- {i.price}")
            count = count + 1
            var6 = var6 - 20
        # p.drawString(50,19,f"item 1:- {orderitemcontext.p_id.p_name} -- {ordercontext.price}")
        
        p.showPage()
        p.save()
        buffer.seek(0)
        return buffer