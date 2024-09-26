from django.contrib import admin
from .models import Livro, Carrinho, ItemCarrinho

admin.site.register(Livro)
admin.site.register(Carrinho)
admin.site.register(ItemCarrinho)