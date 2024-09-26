import requests
from django.shortcuts import render, redirect, get_object_or_404
from .models import Carrinho, ItemCarrinho
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User

def buscar_livros(request):
    query = request.GET.get('query', '')
    url = f'https://www.googleapis.com/books/v1/volumes?q={query}'
    response = requests.get(url)
    dados = response.json()
    livros = dados.get('items', [])

    return render(request, 'catalogo/lista_livros.html', {'livros': livros})

def adicionar_ao_carrinho(request, livro_id):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, "Você precisa estar logado para adicionar itens ao carrinho.")
            return redirect('login')
        
        titulo = request.POST.get('titulo')
        quantidade = int(request.POST.get('quantidade', 1))  # Padrão é 1

        carrinho, criado = Carrinho.objects.get_or_create(usuario=request.user)

        # Verifica se o item já está no carrinho
        item_existente = ItemCarrinho.objects.filter(livro_id=livro_id, usuario=request.user).first()
        if item_existente:
            item_existente.quantidade += quantidade
            item_existente.save()
        else:
            # Cria um novo item no carrinho
            novo_item = ItemCarrinho.objects.create(
                livro_id=livro_id,
                titulo=titulo,
                quantidade=quantidade,
                usuario=request.user
            )
            carrinho.itens.add(novo_item)

        messages.success(request, f'O livro "{titulo}" foi adicionado ao seu carrinho!')
        return redirect('ver_carrinho')

@login_required
def ver_carrinho(request):
    carrinho = Carrinho.objects.filter(usuario=request.user).first()
    itens = carrinho.itens.all() if carrinho else []
    return render(request, 'catalogo/carrinho.html', {'itens': itens})

@login_required
def remover_item(request, item_id):
    item = get_object_or_404(ItemCarrinho, id=item_id, usuario=request.user)
    item.delete()
    messages.success(request, f'O livro "{item.titulo}" foi removido do seu carrinho.')
    return redirect('ver_carrinho')