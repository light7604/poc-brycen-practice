from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import *
import json
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.paginator import Paginator

# Create your views here.
alter_size = (3, 5, 20)
alter_sort = ('name','price')

def shopSearch(request):
    screenName = "shop_search"
    products_search = ''
    search_name = ''
    search_category = ''
    sort = 'name'
    size = 3
    search_flag = False

    # Get Category
    categories = Category.objects.filter(is_sub = False)
    # active_category = request.GET.get('category','')

    # Get Product all
    products_all = Product.objects.all()

    # Get search Product
    # if request.method =='POST': 
    #     products_search = request.POST['searched']

    # Get Product search
    products_search = products_all
    if 'search' in request.GET:
        search_name = request.GET.get('search','')
        products_search = products_search.filter(name__contains = search_name)

    if 'category' in request.GET:
        search_category = request.GET.get('category','')
        if len(search_category) > 0:
            products_search = products_search.filter(category__slug = search_category)

    # Get order by Product
    products_sort =  products_search.order_by(sort)
    if 'sort' in request.GET:
        sort = request.GET.get('sort','')
        if len(sort) > 0:
            if (sort in alter_sort):
                products_sort =  products_search.order_by(sort)

    # Set up Pagination
    if 'size' in request.GET:
        getSize = request.GET.get('size','')
        if len(getSize) > 0:
            if (int(getSize) in alter_size):
                size = int(getSize)

    p = Paginator(products_sort, size)
    page = request.GET.get('page')
    products_pagi = p.get_page(page)            # Pagination Product data
    nums_pagi = 'a' * products_pagi.paginator.num_pages
    upper_limit = int(products_pagi.number) + 1 
    lower_limit = int(products_pagi.number) - 1

    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer = customer, complete = False)
        items = order.orderitem_set.all
        cartItems = order.get_cart_items
        # user_not_login = 'hidden'
        # user_login = 'show'
    else:
        # return redirect('login')
        order = {'get_cart_items': 0, 'get_cart_total':0}
        cartItems = order['get_cart_items']
        # user_not_login = 'show'
        # user_login = 'hidden'

    if len(search_name) > 0: 
        search_flag = True
    
    context = {
        'screenName':screenName,
        'categories':categories,
        # 'active_category':active_category,
        'products': products_all, 
        'items': items, 
        'order': order, 
        'cartItems': cartItems,
        'products_pagi': products_pagi,
        'nums_pagi': nums_pagi,
        'upper_limit': upper_limit,
        'lower_limit': lower_limit,
        'search_flag': search_flag,
        'search_name': search_name,
        'products_count': products_sort.count,
        'size': size,
        'sort': sort,
    }
    return render(request,'app/shop_grid.html', context)

def shopDetail(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer = customer, complete = False)
        items = order.orderitem_set.all
        cartItems = order.get_cart_items
        user_not_login = 'hidden'
        user_login = 'show'
    else:
        items = []
        order = {'get_cart_items': 0, 'get_cart_total':0}
        cartItems = order['get_cart_items']
        user_not_login = 'show'
        user_login = 'hidden'
    id = request.GET.get('id','')
    if id == '': return redirect('shop_grid')
    products = Product.objects.filter(id=id)
    categories = Category.objects.filter(is_sub = False)
    context = {
        'products':products, 
        'categories':categories, 
        'items': items, 
        'order': order, 
        'cartItems': cartItems,
        'user_not_login':user_not_login,
        'user_login':user_login
    }
    return render(request,'app/shop_detail.html', context)

def shopCategory(request):
    categories = Category.objects.filter(is_sub = False)
    active_category = request.GET.get('category','')
    if active_category:
        products = Product.objects.filter(category__slug = active_category)
   
    if request.user.is_authenticated:
        user_not_login = 'hidden'
        user_login = 'show'
    else:
        user_not_login = 'show'
        user_login = 'hidden'
    context = {
        'categories':categories,
        'products': products, 
        'active_category': active_category,
        'user_not_login':user_not_login,
        'user_login':user_login
    }
    return render(request,'app/shop_category.html', context)  

# def shopSearch(request):
#     if request.method =="POST":
#         searched = request.POST['searched']
#         keys = Product.objects.filter(name__contains = searched)
#     if request.user.is_authenticated:
#         customer = request.user
#         order, created = Order.objects.get_or_create(customer = customer, complete = False)
#         # items = order.orderitem_set.all
#         cartItems = order.get_cart_items
#         user_not_login = 'hidden'
#         user_login = 'show'
#     else:
#         # items = []
#         order = {'get_cart_items': 0, 'get_cart_total':0}
#         cartItems = order['get_cart_items']
#         user_not_login = 'show'
#         user_login = 'hidden'
#     categories = Category.objects.filter(is_sub = False)
#     active_category = request.GET.get('category','')
#     products = Product.objects.all()
#     context = {
#         'categories':categories,
#         'active_category':active_category, 
#         'searched':searched,
#         'keys': keys, 
#         'products': products, 
#         'cartItems': cartItems,
#         'user_not_login':user_not_login,
#         'user_login':user_login
#     }
#     return render(request,'app/shop_search.html', context)

def home(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer = customer, complete = False)
        # items = order.orderitem_set.all
        cartItems = order.get_cart_items
        user_not_login = 'hidden'
        user_login = 'show'
    else:
        # items = []
        order = {'get_cart_items': 0, 'get_cart_total':0}
        cartItems = order['get_cart_items']
        user_not_login = 'show'
        user_login = 'hidden'
    categories = Category.objects.filter(is_sub = False)
    active_category = request.GET.get('category','')
    products = Product.objects.all()
    context = {
        'categories':categories,
        'active_category':active_category, 
        'products': products, 
        'cartItems': cartItems,
        'user_not_login':user_not_login,
        'user_login':user_login
    }
    return render(request,'app/base.html', context)

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method =="POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'User or password not correct!')
    context = {}
    return render(request,'app/login.html', context)

def register(request):
    form = CreateUserForm()
    
    if request.method =="POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    context = {
        'form': form,
    }
    return render(request,'app/register.html', context)

def logoutPage(request):
    logout(request)
    return redirect('login')

def shopCart(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer = customer, complete = False)
        items = order.orderitem_set.all
        cartItems = order.get_cart_items
        user_not_login = 'hidden'
        user_login = 'show'
    else:
        # items = []
        # order = {'get_cart_items': 0, 'get_cart_total':0}
        # cartItems = order['get_cart_items']
        # user_not_login = 'show'
        # user_login = 'hidden'
        return redirect('login')
    categories = Category.objects.filter(is_sub = False)
    context = {
        'categories':categories, 
        'items': items, 
        'order': order, 
        'cartItems': cartItems,
        'user_not_login':user_not_login,
        'user_login':user_login
    }
    return render(request,'app/shoping_cart.html', context)

def cart(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer = customer, complete = False)
        items = order.orderitem_set.all
        cartItems = order.get_cart_items
        user_not_login = 'hidden'
        user_login = 'show'
    else:
        # items = []
        # order = {'get_cart_items': 0, 'get_cart_total':0}
        # cartItems = order['get_cart_items']
        # user_not_login = 'show'
        # user_login = 'hidden'
        return redirect('login')
    categories = Category.objects.filter(is_sub = False)
    context = {
        'categories':categories, 
        'items': items, 
        'order': order, 
        'cartItems': cartItems,
        'user_not_login':user_not_login,
        'user_login':user_login
    }
    return render(request,'app/cart.html', context)

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer = customer, complete = False)
        items = order.orderitem_set.all
        cartItems = order.get_cart_items
        user_not_login = 'hidden'
        user_login = 'show'
    else:
        # items = []
        # order = {'get_cart_items': 0, 'get_cart_total':0}
        # cartItems = order['get_cart_items']
        # user_not_login = 'show'
        # user_login = 'hidden'
        return redirect('login')
    categories = Category.objects.filter(is_sub = False)
    context = {
        'categories':categories,
        'items': items, 
        'order': order,
        'cartItems': cartItems,
        'user_not_login':user_not_login,
        'user_login':user_login
    }
    return render(request,'app/checkout.html', context)

def updateItem(request):
    data = json.loads(request.body)
    producId = data['producId']
    action = data['action']
    customer = request.user
    product = Product.objects.get(id = producId)
    order, created = Order.objects.get_or_create(customer = customer, complete = False)
    orderItem, created = OrderItem.objects.get_or_create(order = order, product = product)
    if action == 'add':
        orderItem.quantity += 1
    elif action == 'remove':
        orderItem.quantity -= 1
    elif action == 'add2':
        value = data['value']
        orderItem.quantity += value
    orderItem.save()
    if orderItem.quantity <= 0:
        orderItem.delete()
    return JsonResponse('added', safe=False)

def contact(request):
    return render(request,'app/contact.html')
