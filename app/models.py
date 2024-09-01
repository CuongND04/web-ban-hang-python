from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.utils.translation import gettext_lazy as _
# Create your models here.

#Category
class Category(models.Model):
  sub_category = models.ForeignKey('self',on_delete=models.CASCADE,related_name="sub_categories",null=True,blank=True)
  is_sub = models.BooleanField(default=False)
  name = models.CharField(max_length=200,null=True)
  slug = models.SlugField(max_length=200,unique=True)
  def __str__(self):
    return self.name

# Form register django
class CreateUserForm(UserCreationForm):
  # fix lỗi không thêm placeholder vào input password
  def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(attrs={'placeholder': _("Password")})
        self.fields['password2'].widget = forms.PasswordInput(attrs={'placeholder': _("Confirm Password")})
  class Meta(UserCreationForm):
    model  = User
    fields = ['username','email','first_name','last_name','password1','password2']
    # thêm placeholder
    widgets = {
        'username': forms.TextInput(attrs={'placeholder': 'Enter your username', 'autocomplete': 'off'}),
        'email': forms.EmailInput(attrs={'placeholder': 'Enter your email', 'autocomplete': 'off'}),
        'first_name': forms.TextInput(attrs={'placeholder': 'Enter your first name', 'autocomplete': 'off'}),
        'last_name': forms.TextInput(attrs={'placeholder': 'Enter your last name', 'autocomplete': 'off'}),
    }

class Product(models.Model):
  category = models.ManyToManyField(Category,related_name='product')
  name = models.CharField(max_length=200,null=True )
  price = models.FloatField()
  digital = models.BooleanField(default=False,null=True,blank=False)
  image = models.ImageField(null=True,blank=True)
  def __str__(self):
    return self.name
  @property
  def ImageUrl(self):
    try:
      url = self.image.url
    except:
      url = ""
    return url
      

class Order(models.Model):
  customer = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank = True)
  date_order = models.DateTimeField(auto_now_add=True)
  complete = models.BooleanField(default=False,null=True,blank=False)
  transaction_id = models.CharField(max_length=200,null=True)
  def __str__(self):
    return str(self.id)
  # hàm lấy tổng số item
  @property
  def get_cart_items(self):
    orderitems = self.orderitem_set.all()
    total = sum([item.quantity for item in orderitems])
    return total
  
  # hàm lấy tổng số tiền
  @property
  def get_cart_total(self):
    orderitems = self.orderitem_set.all()
    total = sum([item.get_total for item in orderitems])
    return total
  
class OrderItem(models.Model):
  product = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True,blank = True)
  order = models.ForeignKey(Order,on_delete=models.SET_NULL,null=True,blank = True)
  quantity = models.IntegerField(default=0,null=True,blank=True)
  date_added =  models.DateTimeField(auto_now_add=True)
  # hàm lấy số tiền
  @property
  def get_total(self):
    total = self.product.price*self.quantity
    return total

class ShippingAddress(models.Model):
  customer = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank = True)
  order = models.ForeignKey(Order,on_delete=models.SET_NULL,null=True,blank = True)
  address = models.CharField(max_length=200,null=True)
  city = models.CharField(max_length=200,null=True)
  state = models.CharField(max_length=200,null=True)
  mobile = models.CharField(max_length=10,null=True)
  date_added =  models.DateTimeField(auto_now_add=True)
  def __str__(self):
    return self.address