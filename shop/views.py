from django.shortcuts import render, redirect
from .models import Product, UserCart
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def home(request):
    return render(request, 'index.html')

@csrf_exempt
@login_required(login_url='/')
def escolha_entrega(request):
    if request.method == 'GET':
        return render(request, 'escolha_entrega.html')
    return JsonResponse({'error': 'Método não permitido.'})

@csrf_exempt
@login_required(login_url='/')
def endereco(request):
    if request.method == 'GET':
        return render(request, 'endereco.html')
    return JsonResponse({'error': 'Método não permitido.'})

@csrf_exempt
@login_required(login_url='/')
def pagamento(request):
    if request.method == 'GET':
        return render(request, 'pagamento.html')
    return JsonResponse({'error': 'Método não permitido.'})

@csrf_exempt
def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        senha = request.POST['senha']
        user = authenticate(request, username=email, password=senha)
        if user is not None:
            auth_login(request, user)
            return JsonResponse({'message': f'Login realizado com sucesso! Bem-vindo, {user.first_name}!'})
        else:
            return JsonResponse({'error': 'E-mail ou senha incorretos.'})
    return JsonResponse({'error': 'Método não permitido.'})

@csrf_exempt
@login_required(login_url='/')
def add_carrinho(request):
    if request.method == 'POST':
        user = request.user
        print("Memory: ", request.body)
        product_id = json.loads(request.body)['product_id']
        try:
            product = Product.objects.get(id=product_id)
            cart, created = UserCart.objects.get_or_create(user=user, defaults={'total': 0})
            cart.products.add(product)
            cart.total += product.price
            cart.save()
            return JsonResponse({'message': 'Produto adicionado ao carrinho!'})
        except Product.DoesNotExist:
            return JsonResponse({'error': 'Produto não encontrado.'})
    return JsonResponse({'error': 'Método não permitido.'})

@csrf_exempt
@login_required(login_url='/')
def remove_carrinho(request):
    if request.method == 'POST':
        user = request.user
        print("Memory: ", request.body)
        product_id = json.loads(request.body)['product_id']
        try:
            product = Product.objects.get(id=product_id)
            cart = UserCart.objects.get(user=user)
            cart.products.remove(product)
            cart.total -= product.price
            cart.save()
            return JsonResponse({'message': 'Produto removido do carrinho!'})
        except Product.DoesNotExist:
            return JsonResponse({'error': 'Produto não encontrado.'})
        except UserCart.DoesNotExist:
            return JsonResponse({'error': 'Carrinho não encontrado.'})
    return JsonResponse({'error': 'Método não permitido.'})

@csrf_exempt
@login_required(login_url='/')
def clear_carrinho(request):
    if request.method == 'POST':
        user = request.user
        try:
            cart = UserCart.objects.get(user=user)
            cart.products.clear()
            cart.total = 0
            cart.save()
            return JsonResponse({'message': 'Carrinho limpo!'})
        except UserCart.DoesNotExist:
            return JsonResponse({'error': 'Carrinho não encontrado.'})
    return JsonResponse({'error': 'Método não permitido.'})

@csrf_exempt
def register(request):
    if request.method == 'POST':
        nome = request.POST['nome']
        email = request.POST['email']
        senha = request.POST['senha']
        if User.objects.filter(username=email).exists():
            return JsonResponse({'error': 'Este e-mail já está cadastrado!'})
        user = User.objects.create_user(username=email, password=senha, first_name=nome)
        user.save()
        auth_login(request, user)
        return JsonResponse({'message': f'Cadastro realizado com sucesso! Bem-vindo, {user.first_name}!'})
    return JsonResponse({'error': 'Método não permitido.'})

@login_required(login_url='/')
def compras(request):
    user = request.user
    products = Product.objects.all()
    print(f"Logged in user: {user.username}")
    return render(request, 'compras.html', {'products': products, 'user': user})

@csrf_exempt
@login_required(login_url='/')
def carrinho(request):
    user = request.user
    try:
        cart = UserCart.objects.get(user=user)
        products = cart.products.all()
        products_list = [{'id': product.id, 'name': product.name, 'price': product.price} for product in products]
        return JsonResponse({'user': user.username, 'products': products_list, 'total': cart.total})
    except UserCart.DoesNotExist:
        return JsonResponse({'error': 'Carrinho não encontrado.'})
