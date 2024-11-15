from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from rest_framework import generics
from .models import Watch, Cart, Order
from .forms import CartForm, CheckoutForm
from .serializers import WatchSerializer
from .utils import send_order_confirmation_email

# Homepage view (no login required)
def homepage(request):
    featured_watches = Watch.objects.all()[:6]
    return render(request, 'homepage.html', {'featured_watches': featured_watches})

# Product list view (no login required)
def product_list(request):
    category = request.GET.get('category')
    if category:
        watches = Watch.objects.filter(category=category)
    else:
        watches = Watch.objects.all()
    return render(request, 'product_list.html', {'watches': watches})

# Product detail view (no login required)
def product_detail(request, watch_id):
    watch = get_object_or_404(Watch, pk=watch_id)
    return render(request, 'product_detail.html', {'watch': watch})

# Cart view (login required)
@login_required
def cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.watch.price * item.quantity for item in cart_items)
    if request.method == 'POST':
        for item in cart_items:
            form = CartForm(request.POST, instance=item)
            if form.is_valid():
                form.save()
        return redirect('watches:cart')  # Reload the cart page after updating
    return render(request, 'cart.html', {'cart': cart_items, 'total_price': total_price, 'form': CartForm()})

# Add to cart view (login required)
@login_required
def add_to_cart(request, watch_id):
    watch = get_object_or_404(Watch, pk=watch_id)  # Ensure watch exists
    quantity = int(request.POST.get('quantity', 1))  # Get quantity from the form, default to 1
    
    # Check if the watch is already in the user's cart
    cart_item, created = Cart.objects.get_or_create(user=request.user, watch=watch)
    
    if not created:
        # If the item already exists, update the quantity
        cart_item.quantity += quantity
    else:
        # Otherwise, set the quantity for the new item
        cart_item.quantity = quantity
        
    cart_item.save()
    return redirect('watches:cart')


# Remove from cart view (login required)
@login_required
def remove_from_cart(request, cart_item_id):
    if request.method == 'POST':
        cart_item = get_object_or_404(Cart, pk=cart_item_id)  # Get the cart item by its ID
        cart_item.delete()  # Remove the item from the cart
        return redirect('watches:cart')

# Checkout view (login required)
@login_required
def checkout(request):
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            # Process order and checkout logic
            order = Order.objects.create(
                user=request.user, 
                address=form.cleaned_data['address'], 
                total_price=calculate_total(request.user)
            )
            # Add items to the order and clear the cart
            cart_items = Cart.objects.filter(user=request.user)
            for item in cart_items:
                order.items.add(item.watch)
                item.delete()  # Clear item from the cart after adding to order
            order.save()

            # Send confirmation email
            send_order_confirmation_email(order)

            # Redirect to order confirmation page
            return redirect('watches:order_confirmation', order_id=order.id)
    else:
        form = CheckoutForm()

    return render(request, 'checkout.html', {'form': form})

# Order confirmation view (login required)
@login_required
def order_confirmation(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    return render(request, 'order_confirmation.html', {'order': order})

class WatchListCreateView(generics.ListCreateAPIView):
    queryset = Watch.objects.all()
    serializer_class = WatchSerializer

class WatchDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Watch.objects.all()
    serializer_class = WatchSerializer
