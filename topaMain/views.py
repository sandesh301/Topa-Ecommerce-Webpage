from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import EmailMessage, send_mail
from Topa import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth import authenticate, login, logout
from admin_panel.models import ProductSize
from topa_payment.models import Cart

from admin_panel.models import Product, ProductCollection
from . tokens import generate_token
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404


def home(request):
    products = Product.objects.all()
    return render(request, 'topaMain/index.html', {'products': products})


def shop(request, product_id=None):
    products = Product.objects.all()
    selected_product = None

    if product_id:
        selected_product = get_object_or_404(Product, id=product_id)

    context = {
        'products': products,
        'selected_product': selected_product
    }

    return render(request, 'topaMain/shop.html', context)


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    products = Product.objects.all()
    context = {'product': product, 'products': products}
    return render(request, 'topaMain/product_detail.html', context)


def collection(request, collection_id=None):
    collections = ProductCollection.objects.all()
    selected_collection = None
    products = Product.objects.all()

    if collection_id:
        selected_collection = get_object_or_404(
            ProductCollection, id=collection_id)
        products = products.filter(collection=selected_collection)

    context = {
        'collections': collections,
        'selected_collection': selected_collection,
        'products': products,
    }
    return render(request, 'topaMain/collection.html', context)


def get_sizes(request):
    sizes = ProductSize.objects.all().values('id', 'name')
    return JsonResponse({'sizes': list(sizes)})


def get_products_by_size(request, size_id):
    products = Product.objects.filter(sizes__id=size_id)

    # Create a list of dictionaries containing product details
    products_list = []
    for product in products:
        products_list.append({
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'image_url': product.image.url,
            # Add more attributes as needed
        })

    return JsonResponse({'products': products_list})


def about_us(request):
    return render(request, 'topaMain/about.html')


def about1(request):
    return render(request, 'topaMain/about1.html')


def learn(request):
    return render(request, 'topaMain/learn.html')


def privacy(request):
    return render(request, 'topaMain/privacy.html')


def sustainability(request):
    return render(request, 'topaMain/sustainability.html')


def terms(request):
    return render(request, 'topaMain/terms.html')


def values(request):
    return render(request, 'topaMain/values.html')


# This decorator will redirect users to the login page if not logged in
@login_required(login_url='/login/')
def user_home(request):
    return redirect(request, '/home')  # Redirect to your e-commerce home page


def register(request):
    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        phone = request.POST['phone']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if User.objects.filter(username=username):
            messages.error(
                request, "Username already exist! Please try some other username.")
            return redirect('/register')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email Already Registered!!")
            return redirect('/register')

        if len(username) > 20:
            messages.error(request, "Username must be under 20 charcters!!")
            return redirect('/register')

        if pass1 != pass2:
            messages.error(request, "Passwords didn't matched!!")
            return redirect('/register')

        if not username.isalnum():
            messages.error(request, "Username must be Alpha-Numeric!!")
            return redirect('/register')

        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        # myuser.is_active = False
        myuser.is_active = False
        myuser.save()

        # Welcome Email
        subject = "Welcome to GFG- Django Login!!"
        message = "Hello " + myuser.first_name + "!! \n" + \
            "Welcome to GFG!! \nThank you for visiting our website\n. We have also sent you a confirmation email, please confirm your email address. \n\nThanking You\nAnubhav Madhav"
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)

        # Email Address Confirmation Email
        current_site = get_current_site(request)
        email_subject = "Confirm your Email @ GFG - Django Login!!"
        message2 = render_to_string('topaMain/email_confirmation.html', {

            'name': myuser.first_name,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
            'token': generate_token.make_token(myuser)
        })
        email = EmailMessage(
            email_subject,
            message2,
            settings.EMAIL_HOST_USER,
            [myuser.email],
        )
        email.fail_silently = True
        email.send()
        return redirect('/login')

    return render(request, 'topaMain/register.html')


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        myuser = None

    if myuser is not None and generate_token.check_token(myuser, token):
        myuser.is_active = True
        # user.profile.signup_confirmation = True
        myuser.save()
        login(request, myuser)
        messages.success(request, "Your Account has been activated!!")
        return redirect('/login')
    else:
        return render(request, 'activation_failed.html')


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']

        user = authenticate(username=username, password=pass1)

        if user is not None:
            login(request, user)
            return redirect('/home')
        else:
            messages.error(request, "Bad Credentials!!")
            return redirect('/login')

    return render(request, 'topaMain/login.html')


def user_logout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully!!")
    return redirect(request, 'topaMain/home.htnl')


def check_authentication(request):
    data = {
        'is_authenticated': request.user.is_authenticated
    }
    return JsonResponse(data)
