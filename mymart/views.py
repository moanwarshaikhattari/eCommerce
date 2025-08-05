from django.shortcuts import render, redirect, get_object_or_404
from .models import Category,Product,Review, ShippingDetails, Add_To_Cart
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User


def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        con_password = request.POST['con_password']
        
        errors=[]
        if password != con_password:
            errors.append("Passwords do not match.")
        if User.objects.filter(username=username).exists():
            errors.append("Username is already taken.")
        if User.objects.filter(email=email).exists():
            errors.append("Email is already registered")

        if errors:
            return render(request, 'signup.html', {'errors': errors})
        
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            )
        login(request, user)
        return redirect('login_view')
    return render(request, 'signup.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error':True})
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('home')

def profile(request):

    return render(request, 'profile.html')

def delete_cart_item(request, item_id):
    item = get_object_or_404(Add_To_Cart, id=item_id, user=request.user)
    item.delete()
    return redirect('view_cart') 

def view_cart(request):
    if request.user.is_authenticated:
        cart_items = Add_To_Cart.objects.filter(user=request.user) #use for count tof cart item
    else:
        cart_items = []
    # del_product = Add_To_Cart.objects.delete()
    total_amount = sum(item.total_price() for item in cart_items)
    return render(request, 'cart.html', {'products': cart_items, 'total': total_amount})


# def cart(request, product_id): #add_to_ cart
#     product=Product.objects.get(id=product_id)
#     Add_To_Cart.objects.create(user=request.user, product=product)
#     cart_items = Add_To_Cart.objects.filter(user=request.user)
    
#     #cart_items = Add_To_Cart.objects.all()

#     data = {
#         'products': cart_items
#     }
#     return render(request, 'cart.html', data)

def cart(request, product_id=None):
    if product_id:
        product = Product.objects.get(id=product_id)
        cart_item, created = Add_To_Cart.objects.get_or_create(user=request.user, product=product)
        if not created:
            cart_item.quantity += 1
            cart_item.save()

    cart_items = Add_To_Cart.objects.filter(user=request.user)
    total_amount = sum(item.total_price() for item in cart_items)

    return render(request, 'cart.html', {'products': cart_items, 'total': total_amount})

def update_quantity(request, item_id, action):
    item = Add_To_Cart.objects.get(id=item_id, user=request.user)

    if action == 'increase':
        if item.quantity < 3:  # Don't go above 3
            item.quantity += 1
    elif action == 'decrease':
        if item.quantity > 1:  # Don't go below 1
            item.quantity -= 1

    item.save()
    return redirect('view_cart')

def home(request):
   
    category_id = request.GET.get('category')
    myproduct = Product.objects.all()
    categories = Category.objects.all()

    if category_id:
        myproduct = Product.objects.filter(prd_category=category_id)
    
    if request.user.is_authenticated: #use for count to cart item
        cart_items = Add_To_Cart.objects.filter(user=request.user) 
    else:
        cart_items = []
    data = {
        'products':cart_items,
        'categories':categories,
        'myproduct':myproduct,
        'selected_category': int(category_id) if category_id else None
    }
    return render(request, 'home.html', data)

def details(request,slug):
   
    productDetails = Product.objects.get(product_slug=slug)
    relatedproduct = Product.objects.filter(prd_category=productDetails.prd_category)
    
    # allreview = Review.objects.all().order_by('-id')[0:6]
    allreview = Review.objects.filter(product_review=productDetails).order_by('-id')
    cat=Category.objects.all()

    if request.user.is_authenticated: #use for count tof cart item
        cart_items = Add_To_Cart.objects.filter(user=request.user) 
    else:
        cart_items = []

    message = None
    
    if request.method == "POST":
        # reviewername = request.POST.get('rusername')
        # revieweremail = request.POST.get('ruseremail')
        reviewercomment = request.POST.get('comment')
        rating = request.POST.get('rating') or 0
        
        # Review.objects.create(reviewer_name=reviewername, reviewer_email=revieweremail, review=reviewercomment,rating=int(rating))
        Review.objects.create(
            user=request.user,  
            product_review=productDetails,
            review=reviewercomment,
            rating=int(rating)
            )
        message = "We appreciate your feedback! Your review was submitted successfully."
        
    data = {
        'products':cart_items,
        'productDetails':productDetails,
        'relatedproduct':relatedproduct,
        'allreview':allreview,
        'message':message,
        "names":cat
    }
    return render(request, 'product-details.html',data)

def chackout_dtails(request):
    if request.method == "POST":
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zipcode = request.POST.get('zipcode')
        mobile = request.POST.get('phone')

        ShippingDetails.objects.create(
            ship_username = request.user,
            ship_email = request.user.email,
            ship_address = address,
            ship_city = city,
            ship_state = state,
            ship_zipcode = zipcode,
            ship_mobile = mobile
        )

    if request.user.is_authenticated:
        cart_items = Add_To_Cart.objects.filter(user=request.user) #use for count tof cart item
    else:
        cart_items = []

    total_amount = sum(item.total_price() for item in cart_items)

    data = {
        'products':cart_items,
        'total':total_amount,
    }
    return render(request, 'chackout.html', data)