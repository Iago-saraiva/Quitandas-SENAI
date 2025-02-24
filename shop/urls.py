from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('compras/', views.compras, name='compras'),
    path('carrinho/', views.carrinho, name='carrinho'),
    path('escolha_entrega/', views.escolha_entrega, name='escolha_entrega'),
    path('endereco/', views.endereco, name='endereco'),
    path('pagamento/', views.pagamento, name='pagamento'),
    path('add_carrinho/', views.add_carrinho, name='add_carrinho'),
    path('remove_carrinho/', views.remove_carrinho, name='remove_carrinho'),
    path('clear_carrinho/', views.clear_carrinho, name='clear_carrinho'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
