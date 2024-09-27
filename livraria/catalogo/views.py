import requests
from django.shortcuts import render, redirect, get_object_or_404
from .models import Carrinho, ItemCarrinho, Pedido
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegistroUsuarioForm
from django.contrib import messages
from django.http import HttpResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa

# livro
def buscar_livros(request):
    query = request.GET.get('query', '')
    filtro = request.GET.get('filtro', 'titulo')  

    
    if not query:
        return render(request, 'catalogo/lista_livros.html', {'livros': [], 'query': query})

   
    if filtro == 'categoria':
        url = f'https://www.googleapis.com/books/v1/volumes?q=subject:{query}'
    elif filtro == 'autor':
        url = f'https://www.googleapis.com/books/v1/volumes?q=inauthor:{query}'
    else: 
        url = f'https://www.googleapis.com/books/v1/volumes?q=intitle:{query}'

    response = requests.get(url)
    dados = response.json()
    livros = dados.get('items', [])

    return render(request, 'catalogo/lista_livros.html', {'livros': livros, 'query': query})

def detalhes_livro(request, livro_id):
    url = f'https://www.googleapis.com/books/v1/volumes/{livro_id}'
    response = requests.get(url)
    livro = response.json().get('volumeInfo', {})
    
    detalhes = {
        'titulo': livro.get('title', 'Título não disponível'),
        'autores': livro.get('authors', []),
        'categorias': livro.get('categories', []),
        'data_publicacao': livro.get('publishedDate', 'Data não disponível'),
        'descricao': livro.get('description', 'Descrição não disponível'),
        'paginas': livro.get('pageCount', 'N/A'),
        'publicadora': livro.get('publisher', 'Publicadora não disponível'),
        'capa': livro.get('imageLinks', {}).get('thumbnail', ''),
    }
    
    return render(request, 'catalogo/detalhes_livro.html', {'detalhes': detalhes})



# carrinho
def adicionar_ao_carrinho(request, livro_id):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, "Você precisa estar logado para adicionar itens ao carrinho.")
            return redirect('login')
        
        titulo = request.POST.get('titulo')
        quantidade = int(request.POST.get('quantidade', 1))  

        carrinho, criado = Carrinho.objects.get_or_create(usuario=request.user)

        
        item_existente = ItemCarrinho.objects.filter(livro_id=livro_id, usuario=request.user).first()
        if item_existente:
            item_existente.quantidade += quantidade
            item_existente.save()
        else:
           
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

#finalizar compra
@login_required
def finalizar_compra(request):
    carrinho = Carrinho.objects.filter(usuario=request.user).first()
    if carrinho and carrinho.itens.exists():
       
        pedido = Pedido.objects.create(usuario=request.user)
        for item in carrinho.itens.all():
            pedido.itens.add(item)
        
        
        carrinho.itens.clear()
        messages.success(request, 'Compra realizada com sucesso! Obrigado por comprar conosco.')
    else:
        messages.error(request, 'Seu carrinho está vazio.')
    
    return redirect('buscar_livros')

#historico compras
@login_required
def historico_compras(request):
    pedidos = Pedido.objects.filter(usuario=request.user).order_by('-data_pedido')
    return render(request, 'catalogo/historico_compras.html', {'pedidos': pedidos})

@login_required
def exportar_historico_pdf(request):
    pedidos = Pedido.objects.filter(usuario=request.user).order_by('-data_pedido')
    template_path = 'catalogo/historico_pdf.html'
    context = {'pedidos': pedidos}
    
    
    html = render_to_string(template_path, context)
    
   
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="historico_compras.pdf"'
    
  
    pisa_status = pisa.CreatePDF(html, dest=response)
    
   
    if pisa_status.err:
        return HttpResponse('Erro ao gerar o PDF', status=400)
    
    return response

# autenticação
def registro(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Bem-vindo, {user.username}! Sua conta foi criada com sucesso.')
            return redirect('buscar_livros')
    else:
        form = RegistroUsuarioForm()
    return render(request, 'catalogo/registro.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f'Você está logado como {username}.')
                return redirect('buscar_livros')
            else:
                messages.error(request, 'Usuário ou senha incorretos.')
        else:
            messages.error(request, 'Erro no formulário. Verifique os dados e tente novamente.')
    else:
        form = AuthenticationForm()
    return render(request, 'catalogo/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, 'Você saiu do sistema.')
    return redirect('buscar_livros')