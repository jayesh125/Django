from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from admin_panel.models import BlogPost, SubCategory, Category
from admin_panel.forms import BlogPostForm, OrderForm
from shop.forms import ProductForm
from shop.models import Customer, OrderPlaced, Product, CustomUser
from django.db.models import Count, Sum

from django.utils.timezone import now
from datetime import timedelta

def dashboard(request):
    total_orders = OrderPlaced.objects.count()
    pending_orders = OrderPlaced.objects.filter(status='Accepted').count()

    # Calculate total sales
    total_sales = sum(order.total_cost for order in OrderPlaced.objects.all())

    # Process the orders to calculate total sales and ordered dates
    orders = OrderPlaced.objects.all()

    ordered_dates = []
    total_cost = []
    for order in orders:
        ordered_dates.append(order.ordered_date.strftime('%Y-%m-%d'))
        total_cost.append(order.total_cost)

    # Get the top 3 most bought products
    top_products = Product.objects.annotate(num_orders=Count('orderplaced')).order_by('-num_orders')[:3]

    # Get the count of orders for each product
    all_products = Product.objects.annotate(num_orders=Count('orderplaced')).order_by('-num_orders')

    # Calculate customer growth over the last 6 months
    customer_growth = []
    labels = []
    for i in range(6, -1, -1):
        start_date = now() - timedelta(days=i*30)
        end_date = start_date + timedelta(days=30)
        customer_count = Customer.objects.filter(created_at__range=(start_date, end_date)).count()
        labels.append(start_date.strftime('%B %Y'))
        customer_growth.append(customer_count)

    context = {
        'total_orders': total_orders, 
        'total_sales': total_sales,
        'orders': orders, 
        'labels': ordered_dates, 
        'sales': total_cost,
        'top_products': top_products,
        'all_products': all_products,
        'customer_growth': customer_growth,
        'customer_labels': labels
    }
    return render(request, 'dashboard.html', context)

def products(request):
    products = Product.objects.all()
    
    context = {'products': products}
    return render(request, 'products.html', context)


def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            if 'save' in request.POST:
                return redirect('products')  # Redirect to product list
            elif 'save_and_add_another' in request.POST:
                return redirect('add_product')  # Redirect to the same page with an empty form
            elif 'save_and_continue' in request.POST:
                return redirect('edit_product', pk=product.pk)  # Redirect to the edit page
    else:
        form = ProductForm()

    context = {'form': form}
    return render(request, 'add_product.html', context)

def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            if 'save' in request.POST:
                return redirect('products')
            elif 'save_and_add_another' in request.POST:
                return redirect('add_product')
            elif 'save_and_continue' in request.POST:
                return redirect('edit_product', pk=pk)
    else:
        form = ProductForm(instance=product)
    
    context = {'form': form, 'product': product}
    return render(request, 'edit_product.html', context)

# View to list all orders
def orders_admin(request):
    orders = OrderPlaced.objects.all()
    return render(request, 'orders_admin.html', {'orders': orders})

# View to edit a specific order
def admin_edit_order(request, pk):
    order = get_object_or_404(OrderPlaced, pk=pk)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('orders_admin')
    else:
        form = OrderForm(instance=order)
    
    return render(request, 'edit_orders_admin.html', {'form': form, 'order': order})

def admin_analytics(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    category_id = request.GET.get('category')
    
    categories = Category.objects.all()

    # Filter data based on user input
    orders = OrderPlaced.objects.all()
    if start_date and end_date:
        orders = orders.filter(ordered_date__range=[start_date, end_date])
    if category_id:
        orders = orders.filter(product__category_id=category_id)
    
    # Prepare data for charts
    sales_data = {
        'labels': [],
        'datasets': [{
            'label': 'Sales',
            'data': []
        }]
    }
    user_data = {
        'labels': ['New Users', 'Active Users'],
        'datasets': [{
            'label': 'Users',
            'data': [
                CustomUser.objects.filter(date_joined__range=[start_date, end_date]).count(),
                CustomUser.objects.filter(last_login__range=[start_date, end_date]).count()
            ]
        }]
    }
    product_data = {
        'labels': [],
        'datasets': [{
            'label': 'Products',
            'data': []
        }]
    }

    # Aggregate sales data by date
    sales_by_date = orders.values('ordered_date__date').annotate(total_sales=Sum('product__discounted_price'))
    for entry in sales_by_date:
        sales_data['labels'].append(entry['ordered_date__date'].strftime('%Y-%m-%d'))
        sales_data['datasets'][0]['data'].append(entry['total_sales'])

    # Aggregate product data
    products = Product.objects.all()
    for product in products:
        product_data['labels'].append(product.title)
        product_data['datasets'][0]['data'].append(orders.filter(product=product).count())

    context = {
        'categories': categories,
        'sales_data': sales_data,
        'user_data': user_data,
        'product_data': product_data
    }
    return render(request, 'admin_analytics.html', context)

def blog(request):
    posts = BlogPost.objects.all()
    return render(request, 'blog.html', {'posts': posts})

def blog_list(request):
    posts = BlogPost.objects.all()
    return render(request, 'blog_list.html', {'posts': posts})

def blog_detail(request, id):
    post = get_object_or_404(BlogPost, id=id)
    return render(request, 'blog_detail.html', {'post': post})

def blog_create(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('blog_list')
    else:
        form = BlogPostForm()
    return render(request, 'blog_form.html', {'form': form, 'title': 'Create Blog'})

def blog_edit(request, id):
    post = get_object_or_404(BlogPost, id=id)
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('blog_detail', id=post.id)
    else:
        form = BlogPostForm(instance=post)
    return render(request, 'blog_form.html', {'form': form, 'title': 'Edit Blog'})