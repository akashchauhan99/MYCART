from django.contrib.auth import authenticate, login
from django.http.response import JsonResponse
from django.db.models import Q
from django.shortcuts import redirect, render
from django.views import View
from .models import Customer, OrderPlaced, Product, Cart
from .forms import CustomerRegisterationForm, CustomerProfileForm
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

class ProductView(View):
    def get(self, request):
        topwears = Product.objects.filter(category='TW')
        bottomwears = Product.objects.filter(category='BW')
        mobiles = Product.objects.filter(category='M')
        laptops = Product.objects.filter(category='L')
        totalitems = 0

        if request.user.is_authenticated:
            totalitems = len(Cart.objects.filter(user=request.user))

        print("top",topwears)
        print(bottomwears)
        context = {
            'topwears':topwears,
            'bottomwears':bottomwears,
            'mobiles':mobiles,
            'laptops':laptops,
            'totalitems':totalitems,
        }
        return render(request, 'app/home.html', context)

class ProductDetailView(View):
    def get(self, request, *args, **kwargs):
        product = Product.objects.get(id=kwargs['pk'])
        item_alerady_in_cart = False
        totalitems = 0

        if request.user.is_authenticated:
            item_alerady_in_cart = Cart.objects.filter(Q(product=product.id) 
            & Q(user=request.user)).exists()
            totalitems = len(Cart.objects.filter(user=request.user))

        context = {
            'product': product,
            'item_alerady_in_cart':item_alerady_in_cart,
            'totalitems':totalitems
        }
        return render(request, 'app/productdetail.html', context)

@login_required
def add_to_cart(request, **kwargs):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    # print(user)
    # print(product_id)
    Cart(user=user, product=product).save()
    return redirect('/cart')

@login_required
def showCart(request):
    totalitems = 0
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user)
        totalitems = len(Cart.objects.filter(user=user))
        # print(cart)
        amount = 0.0
        shipping_amount = 50.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        print(cart_product)
        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity * p.product.discounted_price)
                amount += tempamount
                total_amount = amount+shipping_amount
        
            context = {
                'carts':cart,
                'totalamount':total_amount,
                'amount':amount,
                'shippingamount':shipping_amount,
                'totalitems':totalitems,
            }
            return render(request, 'app/addtocart.html', context)
        else:
            return render(request, 'app/emptycart.html')

def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        print(prod_id)
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        print(c)
        c.quantity += 1
        c.save()
        amount = 0.0
        shipping_amount = 50.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        print(cart_product)
        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity * p.product.discounted_price)
                amount += tempamount
                
            total_amount = amount+shipping_amount

            data = {
                'quantity':c.quantity,
                'totalamount':total_amount,
                'amount':amount,                    
                'shippingamount':shipping_amount,
            }
            return JsonResponse(data)

def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        print(prod_id)
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        print(c)
        c.quantity -= 1
        c.save()
        amount = 0.0
        shipping_amount = 50.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        print(cart_product)
        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity * p.product.discounted_price)
                amount += tempamount

            total_amount = amount+shipping_amount

            data = {
                'quantity':c.quantity,
                'totalamount':total_amount,
                'amount':amount,                    
                'shippingamount':shipping_amount,
            }
            return JsonResponse(data)        

def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        print(prod_id)
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        print(c)
        c.delete()
        amount = 0.0
        shipping_amount = 50.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        print(cart_product)
        # if cart_product:
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
        
        total_amount = amount+shipping_amount

        data = {
            'quantity':c.quantity,
            'totalamount':total_amount,
            'amount':amount,                    
            'shippingamount':shipping_amount,
        }
        return JsonResponse(data)     

def buy_now(request, **kwargs):
    user = request.user
    product_id = request.GET.get('prod_id_buynow')
    product = Product.objects.get(id=product_id)
    # print(user)
    # print(product_id)
    cart_save = Cart(user=user, product=product)
    cart_save.save()
    return redirect('/showbuy')

def show_buy(request):
    user = request.user
    add = Customer.objects.filter(user=user)
    cart_items = Cart.objects.filter(user=user)
    amount = 0.0
    shipping_amount = 50.0
    total_amount = 0.0
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]
    # print(cart_product)

    totalitem = 0
    if request.user.is_authenticated:
        totalitems = len(Cart.objects.filter(user=request.user))

    if cart_product:
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
        
        total_amount = amount+shipping_amount

        context = {
            'cart_items':cart_items,
            'add':add,
            'totalamount':total_amount,
            'totalitems':totalitems,
        }
        return render(request, 'app/checkout.html', context)
    # return render(request, 'app/buynow.html')

@method_decorator(login_required, name='dispatch')
class AddressView(View):
    def get(self, request):
        add = Customer.objects.filter(user=request.user)
        totalitem = 0
        if request.user.is_authenticated:
            totalitems = len(Cart.objects.filter(user=request.user))
            
        context = {
            'add':add,
            'active':'btn-primary',
            'totalitems':totalitems,
        }
        return render(request, 'app/address.html', context)

@login_required
def orders(request):
    user = request.user
    order_placed = OrderPlaced.objects.filter(user=user)
    totalitems = len(Cart.objects.filter(user=request.user))
    # print(customer)
    context = {
        'user':user,
        'order_placed':order_placed,
        'totalitems':totalitems,
    }
    return render(request, 'app/orders.html', context)

def mobileView(request, data= None):
    if data == None:
        mobiles = Product.objects.filter(category='M')
    elif data == 'Redmi' or data == 'Samsung':
        mobiles = Product.objects.filter(category='M').filter(brand=data)
    elif data == 'below':
        mobiles = Product.objects.filter(category='M').filter(discounted_price__lte=15000)
    elif data == 'above':
        mobiles = Product.objects.filter(category='M').filter(discounted_price__gte=15000)

    totalitem = 0
    if request.user.is_authenticated:
        totalitems = len(Cart.objects.filter(user=request.user))

    context = {
        'mobiles':mobiles,
        'totalitems':totalitems,
    }
    return render(request, 'app/mobile.html', context)

def topwearView(request, data = None):
    if data == None:
        topwears = Product.objects.filter(category='TW')
    elif data == 'below':
        topwears = Product.objects.filter(category='TW').filter(discounted_price__lte=400)
    elif data == 'above':
        topwears = Product.objects.filter(category='TW').filter(discounted_price__gte=400)
    
    totalitem = 0
    if request.user.is_authenticated:
        totalitems = len(Cart.objects.filter(user=request.user))

    context = {
        'topwears':topwears,
        'totalitems':totalitems,
    }
    return render(request, 'app/topwear.html', context)

def bottomwearView(request, data = None):
    if data == None:
        bottomwears = Product.objects.filter(category='BW')
    elif data == 'below':
        bottomwears = Product.objects.filter(category='BW').filter(discounted_price__lte=650)
    elif data == 'above':
        bottomwears = Product.objects.filter(category='BW').filter(discounted_price__gte=650)

    totalitem = 0
    if request.user.is_authenticated:
        totalitems = len(Cart.objects.filter(user=request.user))

    context = {
        'bottomwears':bottomwears,
        'totalitems':totalitems,
    }
    return render(request, 'app/bottomwear.html', context)

class CustomerLoginView(View):
    def get(self, request):
        print("Yes")
        return render(request, 'app/login.html')

    def post(self, request):
        username = request.POST['email']
        password = request.POST['password']

        user = authenticate(email=username, password=password)

        if user is not None:
            login(request, user)
            print("Logged in")
            messages.info(request, 'Username or Password is incorrect')
        return render(request, 'app/login.html')

class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegisterationForm()
        # print("get form", form)
        context = {'form':form}
        return render(request, 'app/customerregistration.html', context)
    
    def post(self, request):
        form = CustomerRegisterationForm(request.POST)
        if form.is_valid():
            # print("post form", form)
            form.save()
            messages.success(request, 'Congratulations!! Registered Successfully')
        context = {'form':form}
        return render(request, 'app/customerregistration.html', context)

@login_required
def checkout(request):
    user = request.user
    add = Customer.objects.filter(user=user)
    cart_items = Cart.objects.filter(user=user)
    amount = 0.0
    shipping_amount = 50.0
    total_amount = 0.0
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]
    # print(cart_product)

    totalitem = 0
    if request.user.is_authenticated:
        totalitems = len(Cart.objects.filter(user=request.user))

    if cart_product:
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
        
        total_amount = amount+shipping_amount

        context = {
            'cart_items':cart_items,
            'add':add,
            'totalamount':total_amount,
            'totalitems':totalitems,
        }
        return render(request, 'app/checkout.html', context)

@login_required
def payment_done(request):
    user = request.user
    custid = request.GET.get('custid')
    customer = Customer.objects.get(id=custid)

    cart = Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user, customer=customer, 
        product=c.product , quantity=c.quantity).save()
        c.delete()
    return redirect("orders")

@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        # user = request.user
        # print('user', user)
        totalitem = 0
        if request.user.is_authenticated:
            totalitems = len(Cart.objects.filter(user=request.user))
        context = {
            'form':form,
            'active':'btn-primary',
            'totalitems':totalitems,
        }
        return render(request, 'app/profile.html', context)

    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            zipcode = form.cleaned_data['zipcode']
            state = form.cleaned_data['state']

            reg = Customer(user=user, name=name, locality=locality, city=city, zipcode=zipcode, state=state)
            reg.save()

            messages.success(request, 'Congratulations!! Profile Updated Succesfully')
        context = {
            'form':form,
            'active':'btn-primary',
        }
        return render(request, 'app/profile.html', context)
    
