# ...existing imports...
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
# auth helpers
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.models import User
# from django.contrib.auth.forms import AuthenticationForm, UserCreationForm 
from django.contrib.auth.decorators import login_required
from .forms import ClientCreationForm, ClientUpdateForm, OrderCreateForm
from .models import Client, Dish, Order
from django.views import generic    
from django.urls import reverse_lazy

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


def cart_remove(request, dish_id):
    """Remove a dish from the session cart (or decrease quantity)."""
    cart = request.session.get('cart', {})
    key = str(dish_id)
    if key in cart:
        # remove the item entirely
        cart.pop(key, None)
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
    cart = request.session.get('cart', {})
    print('\n[DEBUG] order_create start, cart:', cart)
    if not cart:
        print('[DEBUG] cart empty -> redirect to cart_detail')
        return redirect('rest_app:cart_detail')

    # use the OrderCreateForm for data
    if request.method == 'POST':
        print('\n[DEBUG] order_create POST received')
        print('POST data:', request.POST)
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data

            # build items snapshot and total
            items_list = []
            total = 0
            for d_id, qty in cart.items():
                try:
                    dish = Dish.objects.get(id=int(d_id))
                    item_total = float(dish.price) * int(qty)
                    items_list.append(f"{dish.name} x{qty} = {item_total}")
                    total += item_total
                except Dish.DoesNotExist:
                    continue

            # link client if possible; if auth User exists but no Client record, create one so orders are tied
            client_obj = None
            if request.user.is_authenticated:
                client_obj = Client.objects.filter(username=request.user.username).first()
                if not client_obj:
                    # create a minimal Client record so orders are associated
                    try:
                        client_obj = Client.objects.create(
                            username=request.user.username,
                            email=getattr(request.user, 'email', '') or '' ,
                            password=''
                        )
                    except Exception:
                        client_obj = None

            order = Order.objects.create(
                client=client_obj,
                full_name=cd.get('full_name') or (request.user.username if request.user.is_authenticated else 'Guest'),
                phone=cd.get('phone'),
                address=cd.get('address'),
                comment=cd.get('comment', ''),
                items='\n'.join(items_list),
                total_price=total
            )

            print('[DEBUG] created order id=', order.id)
            messages.success(request, f'Замовлення #{order.id} створено')
            # clear the cart after successful order and redirect to order history
            request.session['cart'] = {}
            return redirect('rest_app:order_history')
        else:
            print('[DEBUG] order_create form invalid. errors:', form.errors)
            # Re-render the form with errors so the user can correct input;
            # keep the cart in session so nothing is lost.
            cart_items = []
            total = 0
            for d_id, qty in cart.items():
                if Dish.objects.filter(id=int(d_id)).exists():
                    dish = Dish.objects.get(id=int(d_id))
                    item_total = dish.price * qty
                    cart_items.append({'dish': dish, 'quantity': qty, 'total': item_total})
                    total += item_total

            template = 'order_create2.html' if request.user.is_authenticated else 'order_create.html'
            return render(request, template, {
                'form': form,
                'cart_items': cart_items,
                'total_price': total
            })
    else:
        form = OrderCreateForm()

    template = 'order_create2.html' if request.user.is_authenticated else 'order_create.html'
    return render(request, template, {
        'form': form,
        'cart_items': [{'dish': Dish.objects.get(id=int(d_id)), 'quantity': qty, 'total': (Dish.objects.get(id=int(d_id)).price * qty)} for d_id, qty in cart.items() if Dish.objects.filter(id=int(d_id)).exists()],
        'total_price': sum([Dish.objects.get(id=int(d_id)).price * qty for d_id, qty in cart.items() if Dish.objects.filter(id=int(d_id)).exists()])
    })
 
def order_history(request):
    template = 'order_history2.html' if request.user.is_authenticated else 'order_history.html'
    orders = None
    if request.user.is_authenticated:
        # try to find a Client record matching this username and show their orders
        client_obj = Client.objects.filter(username=request.user.username).first()
        if not client_obj:
            # try to create a minimal Client to attach to existing/future orders
            try:
                client_obj = Client.objects.create(
                    username=request.user.username,
                    email=getattr(request.user, 'email', '') or '',
                    password=''
                )
            except Exception:
                client_obj = None

        if client_obj:
            orders = Order.objects.filter(client=client_obj)

    return render(request, template, {'orders': orders})


def order_delete(request, order_id):
    # Only allow POST to delete
    if request.method != 'POST':
        return redirect('rest_app:order_history')

    order = get_object_or_404(Order, id=order_id)

    # Only owner client or staff can delete
    allowed = False
    if request.user.is_staff:
        allowed = True
    else:
        client_obj = Client.objects.filter(username=request.user.username).first() if request.user.is_authenticated else None
        if client_obj and order.client_id == client_obj.id:
            allowed = True

    if not allowed:
        messages.error(request, 'Ви не маєте права видаляти це замовлення')
        return redirect('rest_app:order_history')

    order.delete()
    messages.success(request, f'Замовлення #{order_id} видалено')
    return redirect('rest_app:order_history')
 
# ====================== Авторизація ======================
# def user_login(request):
#     if request.user.is_authenticated:
#         return redirect('home.html')  # вже в акаунті — йди на головну
 
#     if request.method == 'POST':
#         form = AuthenticationForm(data=request.POST)
#         if form.is_valid():
#             user = form.get_user()
#             login(request, user)
#             return redirect('home.html')  #  РЕДІРЕКТ після входу
#     else:
#         form = AuthenticationForm()
 
#     return render(request, 'log.html', {'form': form})
 
 
# def user_register(request):
#     if request.user.is_authenticated:
#         return redirect('rest_app:home')  # вже в акаунті — йди на головну
 
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             return redirect('rest_app:home')  # РЕДІРЕКТ після реєстрації
#     else:
#         form = UserCreationForm()
 
#     return render(request, 'reg.html', {'form': form})
 
 
# def user_logout(request):
def user_logout(request):
    """Log out the current user and redirect to home."""
    logout(request)
    return redirect('rest_app:home')



class ClientDetailView(generic.DetailView):
    model = Client
    context_object_name = 'client'
    queryset = Client.objects.all()

class ClientCreateView(generic.CreateView):
    model = Client
    form_class = ClientCreationForm
    # redirect to named home after successful creation
    success_url = reverse_lazy('rest_app:home')
    template_name = 'rest_app/client_form.html'
    
    def form_valid(self, form):
        # Preserve session cart across login (login() may rotate session)
        saved_cart = self.request.session.get('cart', {})

        # Save Client (our simple model)
        client = form.save()
        
        # Create a corresponding Django auth User so we can use built-in auth/login
        username = form.cleaned_data.get('username')
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password1')
        
        # Create user if not exists
        user, created = User.objects.get_or_create(username=username, defaults={'email': email})
        if created:
            user.set_password(password)
            user.email = email or ''
            user.save()
        else:
            # If a User exists, ensure password is valid (replace it)
            user.set_password(password)
            user.email = email or ''
            user.save()
        
        # Log in the created/updated auth user
        login(self.request, user)

        # restore cart into the new session
        if saved_cart:
            self.request.session['cart'] = saved_cart
        
        return super().form_valid(form)
    
class ClientUpdateView(generic.UpdateView):
    model = Client
    form_class = ClientUpdateForm
    success_url = reverse_lazy('rest_app:home')
    template_name = 'rest_app/client_form.html'





