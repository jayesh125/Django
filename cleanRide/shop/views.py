from django.urls import reverse
from django.db.models import F, Sum

from admin_panel.models import BlogPost, Category, SubCategory
from .forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib.auth import get_user_model
import logging
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import CustomUser, Customer, Product, Cart, OrderPlaced
from django.views import View
from django.http import HttpResponseBadRequest, HttpResponseNotAllowed, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_list_or_404, get_object_or_404, render, redirect, HttpResponse
from django.contrib import messages
from django.db.models import Q
from django.utils.decorators import method_decorator
from math import ceil
from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout

# Create your views here.

def shopindex(request):
    allProds = []
    catprods = Product.objects.values('category', 'id', 'subcategory')
    cats = {item['category'] for item in catprods}

    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        product_sets = [prod[i:i+4] for i in range(0, n, 4)]  # Split products into sets of 4
        allProds.append([product_sets, range(1, nSlides), nSlides])
    
    posts = BlogPost.objects.all()

    params = {'allProds': allProds, 'posts': posts}

    return render(request, "shop.html", params)

def prodview(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    # Pass the product details to the template
    posts = BlogPost.objects.all()

    return render(request, 'prodview.html', {'product': product, 'posts': posts})

class ProductDetailView(View):
    def get(self, request, pk):
        totalitem = 0
        product = Product.objects.get(pk=pk)
        item_already_in_cart = False
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            item_already_in_cart = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
        return render(request, 'prodView.html', {'product': product, 'item_already_in_cart': item_already_in_cart, 'totalitem': totalitem})

@login_required
def buy_now(request):
    user = request.user
    add = Customer.objects.filter(user=user)
    if request.method == 'GET':
        user = request.user
        product_id = request.GET.get('prod_id')
        item_already_in_cart = Cart.objects.filter(Q(product=product_id) & Q(user=user)).exists()
        cart = Cart.objects.filter(user=user)
        
        if not item_already_in_cart:
            product = Product.objects.get(id=product_id)
            Cart.objects.create(user=user, product=product, quantity=1)
        
        return render(request, 'checkout.html', {'cart_items': cart, 'add': add})
    else:
        # Handle other HTTP methods if needed
        return HttpResponseNotAllowed(['GET'])
    
@login_required
def checkout(request):
    user = request.user
    add = Customer.objects.filter(user=user)
    cart_items = Cart.objects.filter(user=request.user)
    amount = 0.0
    shipping_amount = 70.0
    total_amount = 0.0
    cart_product = Cart.objects.filter(user=request.user)

    if cart_product:
        for p in cart_product:
            temp_amount = p.quantity * p.product.discounted_price
            amount += temp_amount
            p.total_price = temp_amount  # Store the total price in the Cart object
        total_amount = amount + shipping_amount
    return render(request, 'checkout.html', {'add': add, 'cart_items': cart_items, 'total_amount': total_amount})
    
@login_required()
def add_to_cart(request):
    user = request.user
    item_already_in_cart1 = False
    product = request.GET.get('prod_id')
    item_already_in_cart1 = Cart.objects.filter(Q(product=product) & Q(user=request.user)).exists()
    if not item_already_in_cart1:
        product_title = Product.objects.get(id=product)
        Cart(user=user, product=product_title).save()
        messages.success(request, 'Product Added to Cart Successfully !!' )
    return redirect('showcart')

def emptycart(request):
    return render(request, "emptycart.html")
    
@login_required
def show_cart(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0.0
        shipping_amount = 70.0
        totalamount = 0.0
        cart_product = Cart.objects.filter(user=request.user)
        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity * p.product.discounted_price)
                amount += tempamount
            totalamount = amount + shipping_amount
            return render(request, 'cart.html', {'carts': cart, 'amount': amount, 'totalamount': totalamount, 'totalitem': totalitem})
        else:
            # If cart is empty, redirect to the empty cart page
            return HttpResponseRedirect(reverse('emptycart'))  # Replace 'empty_cart' with the name of your empty cart page URL
    else:
        return render(request, 'emptycart.html', {'totalitem': totalitem})

@csrf_exempt
@login_required
def modify_cart(request, operation):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        cart_item = get_object_or_404(Cart, product=prod_id, user=request.user)

        if operation == 'plus':
            cart_item.quantity = F('quantity') + 1
        elif operation == 'minus':
            if cart_item.quantity > 1:
                cart_item.quantity = F('quantity') - 1
            else:
                cart_item.delete()
                # Recalculate the total amount after deleting the item
                cart_products = Cart.objects.filter(user=request.user)
                amount = cart_products.aggregate(total_amount=Sum(F('quantity') * F('product__discounted_price')))['total_amount'] or 0
                total_amount = amount + 70.0  # Assuming shipping cost is constant
                messages.success(request, 'Product Removed from Cart Successfully !!')
                return JsonResponse({'deleted': True, 'amount': amount, 'totalamount': total_amount})

        cart_item.save()

        cart_products = Cart.objects.filter(user=request.user)
        amount = cart_products.aggregate(total_amount=Sum(F('quantity') * F('product__discounted_price')))['total_amount'] or 0
        total_amount = amount + 70.0  # Assuming shipping cost is constant

        data = {
            'quantity': cart_item.quantity,
            'amount': amount,
            'totalamount': total_amount
        }
        return JsonResponse(data)
    else:
        return HttpResponseBadRequest("Invalid Request Method")
        
@login_required
def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        try:
            c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
            c.delete()

            cart_products = Cart.objects.filter(user=request.user)
            amount = sum(p.quantity * p.product.discounted_price for p in cart_products)
            total_amount = amount + 70.0  # Assuming shipping cost is constant
            messages.success(request, 'Product Removed from Cart Successfully !!' ) 

            data = {
                'amount': amount,
                'totalamount': total_amount
            }
        except Cart.DoesNotExist:
            # If the item does not exist in the cart, return the current amount and totalamount
            cart_products = Cart.objects.filter(user=request.user)
            amount = sum(p.quantity * p.product.discounted_price for p in cart_products)
            total_amount = amount + 70.0  # Assuming shipping cost is constant

            data = {
                'amount': amount,
                'totalamount': total_amount
            }
        return JsonResponse(data)
    else:
        return JsonResponse({'error': 'Invalid Request Method'})

@login_required
def payment_done(request):
    custid = request.GET.get('custid')
    print(custid)
    user = request.user
    cartid = Cart.objects.filter(user=user)
    customer = Customer.objects.get(id=custid)
    for cid in cartid:
        OrderPlaced(user=user, customer=customer, product=cid.product, quantity=cid.quantity).save()
        cid.delete()

    return redirect("orders")

@login_required
def orders(request):
    op = OrderPlaced.objects.filter(user=request.user)
    return render(request, 'orders.html', {'order_placed': op})

@login_required
def address(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    add = Customer.objects.filter(user=request.user)
    return render(request, 'address.html', {'add': add, 'active': 'btn-primary', 'totalitem': totalitem})

class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, 'signup.html', {'form': form})
    
    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Congratulations!! Registered Successfully.')
            form.save()
            # Redirect to the login page after successful registration
            return redirect('login')  # Replace 'login' with the actual URL name of your login page
        return render(request, 'signup.html', {'form': form})


@method_decorator(login_required, name='dispatch')
class ProfileView(View):
	def get(self, request):
		totalitem = 0
		if request.user.is_authenticated:
			totalitem = len(Cart.objects.filter(user=request.user))
		form = CustomerProfileForm()
		return render(request, 'profile.html', {'form':form, 'active':'btn-primary', 'totalitem':totalitem})
		
	def post(self, request):
		totalitem = 0
		if request.user.is_authenticated:
			totalitem = len(Cart.objects.filter(user=request.user))
		form = CustomerProfileForm(request.POST)
		if form.is_valid():
			usr = request.user
			name  = form.cleaned_data['name']
			locality = form.cleaned_data['locality']
			city = form.cleaned_data['city']
			state = form.cleaned_data['state']
			zipcode = form.cleaned_data['zipcode']
			reg = Customer(user=usr, name=name, locality=locality, city=city, state=state, zipcode=zipcode)
			reg.save()
			messages.success(request, 'Congratulations!! Profile Updated Successfully.')
		return render(request, 'profile.html', {'form':form, 'active':'btn-primary', 'totalitem':totalitem})    

def product_catalog(request):
    category_id = request.GET.get('category')
    subcategory_id = request.GET.get('subcategory')
    products = Product.objects.all()

    if category_id:
        products = products.filter(category_id=category_id)
    if subcategory_id:
        products = products.filter(subcategory_id=subcategory_id)

    categories = Category.objects.all()
    subcategories = SubCategory.objects.all()

    return render(request, 'prodcatalog.html', {
        'products': products,
        'categories': categories,
        'subcategories': subcategories
    })

    return render(request, 'prodcatalog.html', {'grouped_products': grouped_products})

def logout_view(request):
    logout(request)
    return redirect('login')

def fetch_subcategories(request):
    category_id = request.GET.get('category_id')
    subcategories = SubCategory.objects.filter(category_id=category_id).values('id', 'name')
    return JsonResponse(list(subcategories), safe=False)

