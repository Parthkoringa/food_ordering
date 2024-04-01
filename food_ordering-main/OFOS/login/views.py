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
from django.shortcuts import render,redirect
from .forms import Registration
from django.contrib import messages
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import ProductForm
from django.contrib import messages
from login.models import Product, Order
from django.shortcuts import (get_object_or_404,
                                render,
                                HttpResponseRedirect)

from django.contrib.auth.decorators import login_required


def landing(request):
    return render(request,'index.html')

@login_required
def home(request):
    restaurants = CustomeUser.objects.filter(usertype='restaurant')
    
    context = {
        'restaurants' : restaurants,
    }
    return render(request,'home.html',context)

@login_required
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
            return redirect('login:login')
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = Registration()
    return render(request,'register.html',{'register_form' : form})


@login_required
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
                name_temp = CustomeUser.objects.get(username=username)
                if name_temp.usertype == "restaurant":
                    return redirect("login:RestaurantHome")
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("login:home")
            else:
                messages.error(request,"Invalid username or password.")
        else:
            messages.error(request,"Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="login.html", context={"login_form":form})

@login_required
def profile(request,id):
    user = CustomeUser.objects.get(id=id)
    context = {
        'id': id,
        'user': user
    }
    return render(request,'profile.html',context)

@login_required
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
@login_required
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

@login_required    
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

@login_required
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


########################  Restaurent Owner Views #########################

# def restHome(request):
#     return render(request,'home.html')

# def register(request):
#     if request.method == "POST":
#         form = Registration(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             messages.success(request, "Registration successful." )
#             return redirect('login:home')
#         messages.error(request, "Unsuccessful registration. Invalid information.")
#     form = Registration()
#     return render(request,'register.html',{'register_form' : form})

# def login_request(request):
#     if request.method == "POST":
#         form = AuthenticationForm(request, data=request.POST)
#         if form.is_valid():
#             username = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password')
#             user = authenticate(username=username, password=password)
#             if user is not None:
#                 login(request, user)
#                 messages.info(request, f"You are now logged in as {username}.")
#                 return redirect("login:home")
#             else:
#                 messages.error(request,"Invalid username or password.")
#         else:
#             messages.error(request,"Invalid username or password.")
#     form = AuthenticationForm()
    # return render(request=request, template_name="login.html", context={"login_form":form})



# Restaurent Side

@login_required
def restaurant_home(request):
    context={}
    
    print(f'check: {request.user}')
    if request.user.is_authenticated:
        context['list_product'] = Product.objects.filter(user=request.user)
        orders = Order.objects.filter(r_id=request.user)
        order_list =[]

        for order in orders:
            order_list.append(Order_items.objects.filter(o_id = order.id))
            

        context['list_order'] = order_list
        print(f"context['list_order'] : {order_list}") 
        return render(request, 'restauranthome.html', context);
    else:
        return redirect('login:login')


@login_required
def add_product(request):

    if request.method == 'POST':
        form = ProductForm(request.POST or None, request.FILES)
        print (form.errors)
        
        if form.is_valid():
            event = form.save(commit=False)
            event.user = request.user
            event.save()
            messages.success(request, "Registration successful." )
            return redirect('login:RestaurantHome')

        messages.error(request, "Invalid information.")
        print ('Product')
    form = ProductForm()
    return render(request, 'addproduct.html', {'form': form});

# @login_required
# def list_products(request):
#     print(f"Current User: {request.user}")
#     list_product = Product.objects.get(user_id = request.user)
#     print(list_product)
#     return render(request, 'restauranthome.html', {'list': list_product});


@login_required
def remove_product(request, id):
    obj = get_object_or_404(Product, id = id)
    print (f"id:{id}")
    # if request.method =="POST":
        # delete object
    obj.delete()

    return redirect('login:RestaurantHome')


@login_required
def complete_order(request, id):
    obj = get_object_or_404(Order_items, id = id)
    #add order in complete state
    obj.delete()
    return redirect('login:RestaurantHome')