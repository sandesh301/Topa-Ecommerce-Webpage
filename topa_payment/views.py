
from klarna import klarna  # Import Klarna API
from .models import Cart
from django.shortcuts import redirect
from django.shortcuts import render
from klarna import klarna
from django.conf import settings
import stripe
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from rest_framework import generics
from .serializers import DeliveryAddressAPIView
from .models import Cart, CartItem, Product, Wishlist, DeliveryAddress


# CART VIEW
def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.cart_items.all()

    subtotal = sum(cart_item.product.original_price *
                   cart_item.quantity for cart_item in cart_items)

    # Calculate delivery charge
    delivery_charge = 0 if subtotal >= 150 else 40

    total = subtotal + delivery_charge

    for cart_item in cart_items:
        cart_item.product_price = cart_item.product.original_price * cart_item.quantity

    context = {'cart_items': cart_items, 'cart': cart, 'subtotal': subtotal,
               'total': total, 'delivery_charge': delivery_charge}
    return render(request, 'TopaMain/cart.html', context)


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    selected_size = request.POST.get('size')
    selected_quantity = int(request.POST.get('quantity'))

    cart, created = Cart.objects.get_or_create(user=request.user)

    cart_item = CartItem.objects.filter(
        cart=cart, product=product, size=selected_size).first()

    print(f"Selected Quantity: {selected_quantity}")
    print(f"Selected Size: {selected_size}")

    if cart_item:
        print(
            f"Existing Cart Item Quantity Before Update: {cart_item.quantity}")
        cart_item.quantity += selected_quantity
        cart_item.save()
        print(
            f"Existing Cart Item Quantity After Update: {cart_item.quantity}")
    else:
        # Create a new cart item with the cart relationship
        cart_item = CartItem.objects.create(
            cart=cart, product=product, size=selected_size, quantity=selected_quantity)

    # Update the product quantity
    product_to_update = Product.objects.get(pk=product_id)
    if product_to_update.Product_quantity >= selected_quantity:
        product_to_update.Product_quantity -= selected_quantity
        product_to_update.save()
        print("Product quantity updated.")
    else:
        print("Insufficient product quantity for the cart.")

    return redirect('cart_view')


def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    product = cart_item.product
    product_quantity_to_add = cart_item.quantity

    # Increase the product quantity in Product table
    product.Product_quantity += product_quantity_to_add
    product.save()

    # Delete the cart item
    cart_item.delete()

    return redirect('cart_view')


def update_quantity(request, cart_item_id):
    if request.method == 'POST':
        cart_item = get_object_or_404(CartItem, id=cart_item_id)
        new_quantity = int(request.POST.get('quantity', 1))

        # Calculate the quantity change
        quantity_change = new_quantity - cart_item.quantity

        # Update the product's quantity in the database
        product = cart_item.product
        if product.Product_quantity >= quantity_change:
            product.Product_quantity -= quantity_change
            product.save()

            # Update the cart item's quantity
            cart_item.quantity = new_quantity
            cart_item.save()

            return JsonResponse({'message': 'Quantity updated successfully'}, status=200)
        else:
            return JsonResponse({'message': 'Insufficient product quantity'}, status=400)

# Checkout view


def checkout(request):
    cart = Cart.objects.get(user=request.user)
    cart_items = cart.cart_items.all()

    subtotal = sum(cart_item.product.original_price *
                   cart_item.quantity for cart_item in cart_items)
    delivery_charge = 0 if subtotal >= 150 else 40
    total = subtotal + delivery_charge

    context = {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'total': total,
        'delivery_charge': delivery_charge,
    }
    return render(request, 'topaMain/checkout.html', context)


def delivery_form(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        country = request.POST.get('country')
        city = request.POST.get('city')
        address = request.POST.get('address')
        zip_postalcode = request.POST.get('zip_postalcode')

        delivery_address = DeliveryAddress.objects.create(
            full_name=full_name,
            email=email,
            phone=phone,
            country=country,
            city=city,
            address=address,
            zip_postalcode=zip_postalcode,
        )

        return JsonResponse({'message': 'Form submitted successfully'})

    return JsonResponse({'message': 'Invalid request method'}, status=400)


class DeliveryAddressAPI(generics.ListCreateAPIView):
    queryset = DeliveryAddress.objects.all()
    serializer_class = DeliveryAddressAPIView

# WISHLIST VIEW


def wishlist(request):
    wishlist = Wishlist.objects.get(user=request.user)

    context = {
        'wishlist': wishlist,
    }

    return render(request, 'topaMain/wishlist.html', context)


def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    wishlist.products.add(product)
    return redirect('wishlist')  # Replace with the appropriate URL name


def remove_from_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist = Wishlist.objects.get(user=request.user)
    wishlist.products.remove(product)
    return redirect('wishlist')  # Replace with the appropriate URL name


# STRIPE PAYMENT

stripe.api_key = settings.STRIPE_SECRET_KEY


def process_payment(request):
    if request.method == 'POST':
        # Get the Stripe token from the POST data
        token = request.POST.get('token')
        total_amount = request.POST.get('total_amount')
        if not token:
            return JsonResponse({'status': 'failure', 'message': 'Token is missing'})

        if token:
            # Retrieve the user's cart
            try:
                cart = Cart.objects.get(user=request.user)
            except Cart.DoesNotExist:
                # Handle the case where the user has no cart
                return JsonResponse({'status': 'failure', 'message': 'User has no cart.'})

            # Get all cart items associated with the cart
            cart_items = cart.cart_items.all()

            # Calculate the total amount
            subtotal = sum(cart_item.product.original_price *
                           cart_item.quantity for cart_item in cart_items)
            delivery_charge = 0 if subtotal >= 150 else 40
            total_amount = subtotal + delivery_charge

            # Create a charge using the Stripe token
            try:
                charge = stripe.Charge.create(
                    amount=int(total_amount * 100),  # Amount in cents
                    currency='usd',
                    source=token,  # Use the token as the source
                    description='Example charge'
                )

                # Check if the charge was successful
                if charge.paid:
                    # Update order status or perform other tasks
                    # For example, mark the products as purchased
                    for cart_item in cart_items:
                        product = cart_item.product
                        product.Product_quantity -= cart_item.quantity
                        product.save()

                    # Clear the cart
                    cart.cart_items.all().delete()

                    # Return a JsonResponse indicating success
                    return JsonResponse({'status': 'success'})
            except stripe.error.StripeError as e:
                # Handle Stripe errors, e.g., card declined
                return JsonResponse({'status': 'failure', 'message': str(e)})

        else:
            # 'token' is missing in form data
            return JsonResponse({'status': 'failure', 'message': 'Token is missing'})

    # Payment failed or request method is not POST
    return JsonResponse({'status': 'failure', 'message': 'Form is not valid or request method is not POST'})


def payment_success(request):
    return render(request, 'TopaMain/payment_success.html')


def payment_failure(request):
    return render(request, 'TopaMain/payment_failure.html')

# KLARNA PAYMENT

def klarna_checkout(request):
    try:
        # Retrieve the user's cart
        cart = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
        # Handle the case where the user has no cart
        return JsonResponse({'status': 'failure', 'message': 'User has no cart.'})

    # Get all cart items associated with the cart
    cart_items = cart.cart_items.all()

    # Calculate the total amount
    subtotal = sum(cart_item.product.original_price *
                   cart_item.quantity for cart_item in cart_items)
    delivery_charge = 0 if subtotal >= 150 else 40
    total_amount = subtotal + delivery_charge

    try:
        # Initialize the Klarna client
        client = klarna.Client(
            settings.KLARNA_MERCHANT_ID, settings.KLARNA_SECRET, klarna.USA)
    except Exception as e:
        return JsonResponse({'status': 'failure', 'message': f'Klarna Client Initialization Error: {str(e)}'})

    try:
        # Create a Klarna order
        order = client.create_order()
    except Exception as e:
        return JsonResponse({'status': 'failure', 'message': f'Klarna Order Creation Error: {str(e)}'})

    # Add items to the Klarna order
    for cart_item in cart_items:
        product = cart_item.product
        order.add_article(
            # Unique identifier for the product
            article_number=str(product.id),
            title=product.Product_name,  # Product name
            quantity=cart_item.quantity,  # Quantity
            price=int(product.get_discounted_price() * 100),  # Price in cents
            tax_rate=0  # Tax rate (0% in this example)
        )

    try:
        # Set the customer's shipping and billing information
        order.set_shipping_info(
            # Get full name from the delivery form
            given_name=request.POST.get('full_name', ''),
            family_name='',
            # Get email from the delivery form
            email=request.POST.get('email', ''),
            # Get phone from the delivery form
            phone=request.POST.get('phone', '')
        )
    except Exception as e:
        return JsonResponse({'status': 'failure', 'message': f'Error setting shipping info: {str(e)}'})

    try:
        # Create a Klarna session
        session = order.create_session()
    except Exception as e:
        return JsonResponse({'status': 'failure', 'message': f'Error creating Klarna session: {str(e)}'})

    try:
        # Get the Klarna checkout URL
        checkout_url = session.get_checkout_url()
    except Exception as e:
        return JsonResponse({'status': 'failure', 'message': f'Error getting checkout URL: {str(e)}'})

    context = {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'total': total_amount,
        'delivery_charge': delivery_charge,
        'checkout_url': checkout_url
    }

    return render(request, 'topaMain/klarna_checkout.html', context)
