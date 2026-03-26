from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from .models import Dish

def home(request):
    return render(request, 'home.html')

def dish_list(request):
    dishes = Dish.objects.all()
    return render(request, 'list.html', {'dishes': dishes})

def dish_detail(request, dish_id):
    dish = get_object_or_404(Dish, id=dish_id)
    return render(request, 'dish_detail.html', {'dish': dish})

def cart_add(request, dish_id):
    cart = request.session.get('cart', {})
    cart[str(dish_id)] = cart.get(str(dish_id), 0) + 1
    request.session['cart'] = cart
    return redirect('rest_app:cart_detail')

def cart_detail(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0
    for d_id, qty in cart.items():
        try:
            dish = Dish.objects.get(id=int(d_id))
            item_total = dish.price * qty
            cart_items.append({
                'dish': dish,
                'quantity': qty,
                'total': item_total
            })
            total += item_total
        except:
            continue
    return render(request, 'cart_detail.html', {
        'cart_items': cart_items,
        'total_price': total
    })

def order_create(request):
    return render(request, 'order_create.html')

def order_history(request):
    return render(request, 'order_history.html')

def user_login(request):
    return render(request, 'login.html')

def user_register(request):
    return render(request, 'register.html')

def user_logout(request):
    logout(request)
    return redirect('rest_app:home')