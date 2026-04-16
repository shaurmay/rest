from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Dish
 
# ====================== Основні сторінки ======================
def home(request):
    dishes = Dish.objects.all()[:6]
    return render(request, 'home2.html' if request.user.is_authenticated else 'home.html', {'dishes': dishes})
 
def dish_list(request):
    dishes = Dish.objects.all()
    template = 'list2.html' if request.user.is_authenticated else 'list.html'
    return render(request, template, {'dishes': dishes})
 
def dish_detail(request, dish_id):
    dish = get_object_or_404(Dish, id=dish_id)
    template = 'dish_detail2.html' if request.user.is_authenticated else 'dish_detail.html'
    return render(request, template, {'dish': dish})
 
# ====================== Кошик ======================
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
 
    template = 'cart_detail2.html' if request.user.is_authenticated else 'cart_detail.html'
    return render(request, template, {
        'cart_items': cart_items,
        'total_price': total
    })
 
# ====================== Замовлення ======================
def order_create(request):
    template = 'order_create2.html' if request.user.is_authenticated else 'order_create.html'
    return render(request, template)
 
def order_history(request):
    template = 'order_history2.html' if request.user.is_authenticated else 'order_history.html'
    return render(request, template)
 
# ====================== Авторизація ======================
def user_login(request):
    if request.user.is_authenticated:
        return redirect('home.html')  # вже в акаунті — йди на головну
 
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home.html')  #  РЕДІРЕКТ після входу
    else:
        form = AuthenticationForm()
 
    return render(request, 'log.html', {'form': form})
 
 
def user_register(request):
    if request.user.is_authenticated:
        return redirect('rest_app:home')  # вже в акаунті — йди на головну
 
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('rest_app:home')  # РЕДІРЕКТ після реєстрації
    else:
        form = UserCreationForm()
 
    return render(request, 'reg.html', {'form': form})
 
 
def user_logout(request):
    logout(request)
    return redirect('rest_app:home')
 