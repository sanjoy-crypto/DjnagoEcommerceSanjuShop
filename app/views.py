from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from .models import *
from .forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q


def home(request):
    mobiles = Product.objects.filter(category='M')
    laptops = Product.objects.filter(category='L')
    headphones = Product.objects.filter(category='H')
    televisions = Product.objects.filter(category='T')

    context = {'mobiles': mobiles, 'laptops': laptops,
               'headphones': headphones, 'televisions': televisions}
    return render(request, 'app/home.html', context)


def product_detail(request, id):
    product = Product.objects.get(id=id)
    context = {'product': product}
    return render(request, 'app/productdetail.html', context)


def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    # print(product_id)
    product = Product.objects.get(id=product_id)
    Cart(user=user, product=product).save()
    return redirect('/cart')


def show_cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user)
        # print(cart)

        amount = 0
        shipping = 100
        total_amount = 0
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        # print(cart_product)
        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity * p.product.discounted_price)
                amount += tempamount
                totalamount = amount + shipping

            context = {'carts': cart,
                       'totalamount': totalamount,
                       'amount': amount}
            return render(request, 'app/addtocart.html', context)
        else:
            return render(request, 'app/emptycart.html')


def plus_cart(request):
    if request.method == 'GET':
        user = request.user
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity += 1
        c.save()

        amount = 0.0
        shipping_amount = 70.00
        totalamount = 0.0

        cart_product = [p for p in Cart.objects.all() if p.user == user]

        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity * p.product.discount_price)
                amount += tempamount

            data = {
                'quantity': c.quantity,
                'amount': amount,
                'totalamount': amount + shipping_amount
            }

            return JsonResponse(data)


def buy_now(request):
    return render(request, 'app/buynow.html')


def address(request):
    info = Customer.objects.filter(user=request.user)

    context = {'info': info, 'active': 'btn-dark'}
    return render(request, 'app/address.html', context)


def orders(request):
    return render(request, 'app/orders.html')


def mobile(request, data=None):
    if data == None:
        mobiles = Product.objects.filter(category='M')
    elif data == 'Xiaomi' or data == 'Samsung' or data == 'Sony' or data == 'Asus':
        mobiles = Product.objects.filter(category='M').filter(brand=data)
    elif data == 'below':
        mobiles = Product.objects.filter(
            category='M').filter(discounted_price__lt=20000)
    elif data == 'above':
        mobiles = Product.objects.filter(
            category='M').filter(discounted_price__gt=20000)

    context = {'mobiles': mobiles}
    return render(request, 'app/mobile.html', context)


def laptop(request, data=None):
    if data == None:
        laptops = Product.objects.filter(category='L')
    elif data == 'HP' or data == 'Asus':
        laptops = Product.objects.filter(category='L').filter(brand=data)
    elif data == 'below':
        laptops = Product.objects.filter(
            category='L').filter(discounted_price__lt=80000)
    elif data == 'above':
        laptops = Product.objects.filter(
            category='L').filter(discounted_price__gt=80000)

    context = {'laptops': laptops}
    return render(request, 'app/laptop.html', context)


def headphone(request, data=None):
    if data == None:
        headphones = Product.objects.filter(category='H')
    elif data == 'JBL' or data == 'Sony' or data == 'Awei':
        headphones = Product.objects.filter(category='H').filter(brand=data)
    elif data == 'below':
        headphones = Product.objects.filter(
            category='H').filter(discounted_price__lt=2000)
    elif data == 'above':
        headphones = Product.objects.filter(
            category='H').filter(discounted_price__gt=2000)

    context = {'headphones': headphones}
    return render(request, 'app/headphone.html', context)


def television(request, data=None):
    if data == None:
        televisions = Product.objects.filter(category='T')
    elif data == 'Samsung' or data == 'Sony' or data == 'HP':
        televisions = Product.objects.filter(category='T').filter(brand=data)
    elif data == 'below':
        televisions = Product.objects.filter(
            category='T').filter(discounted_price__lt=50000)
    elif data == 'above':
        televisions = Product.objects.filter(
            category='T').filter(discounted_price__gt=50000)

    context = {'televisions': televisions}
    return render(request, 'app/television.html', context)


# def loginPage(request):
#     if request.method == 'POST':
#         username=request.POST.get('username')
#         password=request.POST.get('password')

#         user = authenticate(request,username=username,password=password)

#         if user is not None:
#             login(request,user)
#             return redirect('/')
#         else:
#             messages.warning(request, 'Username or Password is incorrect. Try again!!!')

#     return render(request, 'app/login.html')

# def logoutUser(request):
#     logout(request)
#     return redirect('login')

def customerregistration(request):
    form = CustomerRegistrationForm()

    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(
                request, 'Congratulations!! Registered Successfully')
            form.save()
            return redirect('/login')

    context = {'form': form}
    return render(request, 'app/customerregistration.html', context)


# def profile(request):

#  return render(request, 'app/profile.html')

class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()

        context = {'form': form, 'active': 'btn-dark'}
        return render(request, 'app/profile.html', context)

    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            current_user = request.user
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            zipcode = form.cleaned_data['zipcode']

            reg = Customer(user=current_user, name=name, email=email,
                           phone=phone, locality=locality, city=city, zipcode=zipcode)

            reg.save()
            messages.success(
                request, 'Congratulations!!!  Your Profile Updated Successfully.')

        context = {'form': form, 'active': 'btn-dark'}
        return render(request, 'app/profile.html', context)


def checkout(request):
    return render(request, 'app/checkout.html')
