from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views import View
from admin_panel.models import BlogPost, SubCategory
from shop.models import Cart, CustomUser, Contact
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q

def index(request):
    posts = BlogPost.objects.all()
    return render(request, 'index.html', {'posts': posts})

def login_view(request):
    return render(request, 'login.html')

def signup_view(request):
    return render(request, 'signup.html')

def view_cart(request):
    return render(request, "cart.html")

def view_contact(request):
    return render(request, "contact.html")
    
def contact(request):
    thank = False
    if request.method=="POST":
        fname = request.POST.get('fname', '')
        lname = request.POST.get('lname', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        desc = request.POST.get('desc', '')
        contact = Contact(fname=fname, lname=lname, email=email, phone=phone, desc=desc)
        contact.save()
        thank = True
    
    posts = BlogPost.objects.all()
    return render(request, 'contact.html', {'thank': thank, 'posts': posts})

@csrf_exempt
@login_required
def modify_cart(request, operation):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        cart_item = get_object_or_404(Cart, product=prod_id, user=request.user)

        if operation == 'plus':
            cart_item.quantity += 1
        elif operation == 'minus':
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
            else:
                cart_item.delete()
                return JsonResponse({'deleted': True})

        cart_item.save()

        cart_products = Cart.objects.filter(user=request.user)
        amount = sum(p.quantity * p.product.discounted_price for p in cart_products)
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
        cart_item = get_object_or_404(Cart, product=prod_id, user=request.user)
        cart_item.delete()

        # Recalculate amount and total amount
        cart_products = Cart.objects.filter(user=request.user)
        amount = sum(p.quantity * p.product.discounted_price for p in cart_products)
        total_amount = amount + 70.0  # Assuming shipping cost is constant

        data = {
            'amount': amount,
            'totalamount': total_amount
        }
        return JsonResponse(data)
    else:
        return HttpResponseBadRequest("Invalid Request Method")

def get_subcategories(request):
    category_id = request.GET.get('category_id')
    subcategories = SubCategory.objects.filter(category_id=category_id)
    data = {
        'subcategories': [{'id': sub.id, 'name': sub.name} for sub in subcategories]
    }
    return JsonResponse(data)

def blog_base(request):
    posts = BlogPost.objects.all()
    return render(request, 'base.html', {'posts': posts})

def about(request):
    posts = BlogPost.objects.all()
    return render(request, "about.html", {'posts': posts})