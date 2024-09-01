from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from .models import *
import json 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
# Create your views here.

def detail(request):
  if request.user.is_authenticated:
    customer = request.user
    order,created = Order.objects.get_or_create(customer=customer,complete = False)
    items  = order.orderitem_set.all()
    cartItems = order.get_cart_items
    user_not_login = "none"
    user_login = "block"
  else:
    # khi người dùng chưa đăng nhập
    items = []
    order = {'get_cart_items':0,'get_cart_total': 0}
    cartItems = order['get_cart_items']
    user_not_login = "block"
    user_login = "none"
  id = request.GET.get('id','')
  products = Product.objects.filter(id = id)
  categories = Category.objects.filter(is_sub=False)
  context={'items':items,'order':order,'cartItems':cartItems,'user_not_login':user_not_login,'user_login':user_login,'categories':categories ,'products':products}
  return render(request,'app/detail.html',context)


def category(request):
  #  giỏ hàng
  if request.user.is_authenticated:
  # tắt số lượng trên giỏ hàng
    customer = request.user
    order,created = Order.objects.get_or_create(customer=customer,complete = False)
    items  = order.orderitem_set.all()
    cartItems = order.get_cart_items
    user_not_login = "none"
    user_login = "block"
  else:
    # hiển thị số lượng trên giỏ hàng
    items = []
    order = {'get_cart_items':0,'get_cart_total': 0}
    cartItems = order['get_cart_items']
    user_not_login = "block"
    user_login = "none"
  # END  giỏ hàng
  categories = Category.objects.filter(is_sub=False)
  active_category = request.GET.get('category','')
  if active_category:
    products = Product.objects.filter(category__slug = active_category)
  context = {'categories':categories,'products':products,'active_category':active_category,'user_not_login':user_not_login,'user_login':user_login,'cartItems':cartItems}
  return render(request,'app/category.html',context)


def search(request):
  #  giỏ hàng
  if request.user.is_authenticated:
    customer = request.user
    order,created = Order.objects.get_or_create(customer=customer,complete = False)
    items  = order.orderitem_set.all()
    cartItems = order.get_cart_items
    user_not_login = "none"
    user_login = "block"
  else:
    # khi người dùng chưa đăng nhập
    items = []
    order = {'get_cart_items':0,'get_cart_total': 0}
    cartItems = order['get_cart_items']
    user_not_login = "block"
    user_login = "none"
  # END giỏ hàng
  products = Product.objects.all()
  categories = Category.objects.filter(is_sub=False)
  if request.method == "POST":
    searched = request.POST["searched"]
    keys = Product.objects.filter(name__contains = searched)
  context = {"searched":searched,"keys":keys,'products':products,'cartItems':cartItems,'user_not_login':user_not_login,'user_login':user_login,'categories':categories }
  return render(request,'app/search.html',context)

def register(request):
  categories = Category.objects.filter(is_sub=False)
  user_not_login = "block"
  user_login = "none"
  form = CreateUserForm()
  if request.method == "POST":
    form = CreateUserForm(request.POST)
    if form.is_valid():
      form.save()
      return redirect('login')
  context={'form':form,'user_not_login':user_not_login,'user_login':user_login ,'categories':categories }
  return render(request,'app/register.html',context)



def loginPage(request):
  if request.user.is_authenticated:
    return redirect('home')
  user_not_login = "block"
  user_login = "none"
  categories = Category.objects.filter(is_sub=False)
  if request.method == "POST":
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(request,username = username,password=password)
    if user is not None:
      login(request,user)
      return redirect('home')
    else: messages.info(request,'user or password not correct!')
  context={'user_not_login':user_not_login,'user_login':user_login,'categories':categories }
  return render(request,'app/login.html',context)


def logoutPage(request):
  logout(request)
  return redirect('login')


def home(request):
  if request.user.is_authenticated:
    customer = request.user
    order,created = Order.objects.get_or_create(customer=customer,complete = False)
    items  = order.orderitem_set.all()
    cartItems = order.get_cart_items
    user_not_login = "none"
    user_login = "block"
  else:
    # khi người dùng chưa đăng nhập
    items = []
    order = {'get_cart_items':0,'get_cart_total': 0}
    cartItems = order['get_cart_items']
    user_not_login = "block"
    user_login = "none"
  categories = Category.objects.filter(is_sub=False)
  products = Product.objects.all()
  context={'categories':categories,'products':products,'cartItems':cartItems,'user_not_login':user_not_login,'user_login':user_login }
  return render(request,'app/home.html',context)


def cart(request):
  if request.user.is_authenticated:
    customer = request.user
    order,created = Order.objects.get_or_create(customer=customer,complete = False)
    items  = order.orderitem_set.all()
    cartItems = order.get_cart_items
    user_not_login = "none"
    user_login = "block"
  else:
    # khi người dùng chưa đăng nhập
    items = []
    order = {'get_cart_items':0,'get_cart_total': 0}
    cartItems = order['get_cart_items']
    user_not_login = "block"
    user_login = "none"
  categories = Category.objects.filter(is_sub=False)
  context={'items':items,'order':order,'cartItems':cartItems,'user_not_login':user_not_login,'user_login':user_login,'categories':categories }
  return render(request,'app/cart.html',context)

def checkout(request):
  if request.user.is_authenticated:
    customer = request.user
    order,created = Order.objects.get_or_create(customer=customer,complete = False)
    items  = order.orderitem_set.all()
    cartItems = order.get_cart_items
    user_not_login = "none"
    user_login = "block"
  else:
    # khi người dùng chưa đăng nhập
    items = []
    order = {'get_cart_items':0,'get_cart_total': 0}
    cartItems = order['get_cart_items']
    user_not_login = "block"
    user_login = "none"

  context={'items':items,'order':order,'cartItems':cartItems,'user_not_login':user_not_login,'user_login':user_login }
  return render(request,'app/checkout.html',context)

def updateItem(request):
  data = json.loads(request.body)
  productId = data['productId']
  action = data['action']
  customer  = request.user
  product = Product.objects.get(id=productId)
  order,created = Order.objects.get_or_create(customer=customer,complete = False)
  orderItem,created = OrderItem.objects.get_or_create(order=order,product = product)
  if action == 'add':
    orderItem.quantity += 1
  elif action == 'remove':
    orderItem.quantity -= 1

  orderItem .save()
  
  if orderItem.quantity <= 0:
    orderItem .delete()
  return JsonResponse('add',safe=False)