from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse, HttpResponseRedirect
from django import template, templatetags
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.template.loader import render_to_string

#from .tokens import account_activation_token
from .models import Application, Category, Driver, Product, AllUsers, SponsorOrg, Point, Point_Update, Order, OrderItem
from .forms import Create_Account_Form, User_Login_Form, Edit_User_Info_Form, Address_Form
from .cart import Cart

# Create your views here.

# Home View
@login_required(login_url='/login/')
def home(request):
    user=request.user
    
    user_sponsor_info = []
    user_point_info = []

    if user.is_driver:
        applied_to = Application.objects.all().filter(applying = user.driver_account)
        for i in applied_to:
         if i.accepted == True:
            update_sponsor = SponsorOrg.objects.get(id = i.apply_to_id)
            user.driver_account.sponsor.add(update_sponsor)
            user_points = Point.objects.get_or_create(user = user.driver_account, sponsor_org = update_sponsor)
            user_sponsor_info.append(update_sponsor.sponsor_org)
            user_point_info = Point.objects.filter(user = user.driver_account)
         if i.accepted == False and i.is_active == False:
            update_sponsor = SponsorOrg.objects.get(id = i.apply_to_id)
            try:
                Point.objects.get(user=user.driver_account, sponsor_org = update_sponsor).delete()
                user.driver_account.sponsor.remove(update_sponsor)
            except Point.DoesNotExist:
                pass

        point_updates = Point_Update.objects.filter(user = user.driver_account, is_active = True)   
        for updates in point_updates:
            which_point = Point.objects.get(user = user.driver_account, sponsor_org = updates.organization)
            which_point.point_total += updates.point_change
            Point.objects.filter(user = user.driver_account, sponsor_org = updates.organization).update(point_total =  which_point.point_total)
            which_point.point_total = which_point.point_total * updates.organization.point_value
            Point.objects.filter(user = user.driver_account, sponsor_org = updates.organization).update(monetary_value =  which_point.point_total)
            Point_Update.objects.filter(user = user.driver_account, organization = updates.organization, is_active = True).update(is_active = False) 
            user.save()

        some_updates = Point_Update.objects.filter(user = user.driver_account)[0:3]
        
    return render(request, 'catalog/home.html', {'user_sponsor_info': user_sponsor_info, 'user_point_info':user_point_info,'some_updates':some_updates})

@login_required(login_url='/login/')
def all_updates(request):
    all_point_updates = Point_Update.objects.filter(user = request.user.driver_account) 
    return render(request, 'catalog/all_updates.html', {'all_point_updates': all_point_updates})

# Create Account View
def create_account(request):

    if request.method == 'POST':
        register = Create_Account_Form(request.POST)
        if register.is_valid():
            user = register.save(commit=False)
            user.email = register.cleaned_data['email']
            user.set_password(register.cleaned_data['password2'])
            user.is_active = True
            user.is_driver = True
            user.is_sponsor = False
            user.save()
            driver = Driver.objects.get_or_create(user=user)
             
            current_site = get_current_site(request)
            subject = 'Welcome!'
            message = render_to_string('catalog/welcome_email.html', {
                'user': user,
                'domain': current_site.domain,
            })
            user.email_user(subject=subject, message=message)
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect("home")
            
    else:
        register=Create_Account_Form()

    context = {
        'form': register,
    }

    return render(request, 'catalog/create_account.html', context)

def search_etsy(request):

    return render(request, 'catalog/search_etsy.html')

# Login View
class login_view(LoginView):
    authentication_form = User_Login_Form

def application_request(applying, apply_to):
    try:
        return Application.objects.get(applying=applying, apply_to=apply_to)
    except Application.DoesNotExist:
        return False           
        
def application(request):
    user = request.user
    applied_to = Application.objects.all().filter(applying = user.driver_account)
    not_applied_to = []  
    for x in SponsorOrg.objects.all():
        status = application_request(user.driver_account, x)
        if status == False:
            not_applied_to.append(x)
       
    return render(request, 'catalog/apply.html', {'all_orgs': SponsorOrg.objects.all(), 'applied_to':applied_to, 'not_applied_to': not_applied_to})

def send_application_request(request):
    user = request.user
    if request.method == 'POST':
        applying_to_id = request.POST.get("org_id")
        applying_to = SponsorOrg.objects.get(id = applying_to_id)
        send_request = Application.objects.get_or_create(applying = user.driver_account, apply_to = applying_to, is_active = True)
        user.save()
    return render(request, 'catalog/apply.html')


# Profile View
@login_required(login_url='/login/')
def profile(request):
    return render(request, 'catalog/profile.html')

@login_required(login_url='login')
def edit_profile(request):
    if request.method == 'POST':
        edit_form = Edit_User_Info_Form(request.POST, instance=request.user)
        edit_addy_form = Address_Form(request.POST, instance=request.user.driver_account)
        
        if edit_form.is_valid() and edit_addy_form.is_valid():
            edit_form.save()
            edit_addy_form.save()
            return redirect("profile")
    else:
        edit_form = Edit_User_Info_Form(instance=request.user)
        edit_addy_form = Address_Form(instance=request.user.driver_account)

    return render(request, 'catalog/edit_profile.html', {'edit_form': edit_form , 'edit_addy_form': edit_addy_form})
    

# All Categories View
def categories(request):
    return{'categories': Category.objects.all()}

# Individual Category plus Correlating Products
def category(request, category_slug):
    individual_category = get_object_or_404(Category, slug=category_slug)
    category_products = Product.objects.filter(category = individual_category)
    return render(request, 'catalog/category.html', {'category': individual_category, 'products': category_products})

# All Active Products View
def products(request):
    user = request.user
    user_sponsor = user.driver_account.sponsor.all() 
    products = Product.products.all()
   
    return render(request, 'catalog/products.html', {'products': products, 'user_sponsor': user_sponsor})

# Individual Product plus Info View
def product(request, slug):
    individual_product = get_object_or_404(Product, slug=slug, in_stock=True)
    return render(request, 'catalog/product.html', {'product':individual_product})


@login_required
def wishlist(request):
    products = Product.objects.filter(users_wishlist=request.user.driver_account)
    return render(request, "catalog/likes.html", {"wishlist": products})

@login_required
def add_to_wishlist(request, id):
    product = get_object_or_404(Product, id=id)
    if product.users_wishlist.filter(user_id=request.user.driver_account).exists():
        product.users_wishlist.remove(request.user.driver_account)
        messages.success(request, product.title + " has been removed from your WishList")
    else:
        product.users_wishlist.add(request.user.driver_account)
        messages.success(request, "Added " + product.title + " to your WishList")
    return HttpResponseRedirect(request.META["HTTP_REFERER"])

def place_order(request):
    cart = Cart(request)
    
    user = request.user
    order_total = cart.total() 
    spons_total = 0
    all_sponsors = user.driver_account.sponsor.all()
    for i in all_sponsors:
        for item in cart:
            if i.sponsor_org == item['product'].sponsored_by:   
                 spons_total += item['product'].price
                 user_total = Point.objects.get(user=user.driver_account, sponsor_org = i.sponsor_org)
            if spons_total != 0 and spons_total <= user_total.monetary_value:         
             order = Order.objects.create(user = user.driver_account, first_name = user.driver_account.first_name,last_name = user.driver_account.last_name, email = user.driver_account.email, address1=user.driver_account.street_address,
                        address2=user.driver_account.address_line, city=user.driver_account.city, state=user.driver_account.state, zip_code=user.driver_account.zip_cde, order_total=order_total, org_total_paid= spons_total, sponsor_org = i.sponsor_org, order_status = True)
             orderid = order.pk 
             for item in cart:
                OrderItem.objects.get_or_create(order_id=orderid, product=item['product'], price=item['price'], quantity=item['qty'])
   
    return render(request, "catalog/checkout.html", {"spons_total": spons_total})

# Cart Session View
def cart_session(request):
    return{'cart': Cart(request)}

# Cart View
def cart(request):
    cart = Cart(request)
    return render(request, 'catalog/cart.html',{'cart':cart} )

# Add to Cart View
def add_to_cart(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        product_qty = int(request.POST.get('productqty'))
        product = get_object_or_404(Product, id = product_id)
        cart.add(product=product, qty=product_qty)
        cartqty = cart.__len__()
        response = JsonResponse({'qty':cartqty})
        return response

def remove_from_cart(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        cart.remove(product=product_id)
        cartqty = cart.__len__()
        response = JsonResponse({'qty':cartqty})
        return response


def update_cart(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        product_qty = int(request.POST.get('productqty'))
        cart.update(product=product_id, qty=product_qty)

        cartqty = cart.__len__()
        carttotal = cart.total()
        response = JsonResponse({'qty': cartqty, 'subtotal': carttotal})
        return response

@login_required
def checkout(request):
    cart = Cart(request)
    total_price = cart.total()
    return render(request, 'catalog/checkout.html', {'total_price':total_price, 'cart':cart})
  
             
def user_orders(request):
    user = request.user
    orders = Order.objects.filter(user = user.driver_account).filter(billing_status=True)
    return orders