from django.urls import path
from . import views

urlpatterns = [
    path('buscar/', views.buscar_livros, name='buscar_livros'),
    path('carrinho/adicionar/<str:livro_id>/', views.adicionar_ao_carrinho, name='adicionar_ao_carrinho'),
    path('carrinho/', views.ver_carrinho, name='ver_carrinho'),
    path('carrinho/remover/<int:item_id>/', views.remover_item, name='remover_item'),
    path('registro/', views.registro, name='registro'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('finalizar-compra/', views.finalizar_compra, name='finalizar_compra'),
    path('historico-compras/', views.historico_compras, name='historico_compras'),
    path('historico-compras/pdf/', views.exportar_historico_pdf, name='exportar_historico_pdf'),
]
