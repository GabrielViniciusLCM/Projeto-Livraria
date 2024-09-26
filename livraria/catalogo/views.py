import requests
from django.shortcuts import render

def buscar_livros(request):
    query = request.GET.get('query', '')
    url = f'https://www.googleapis.com/books/v1/volumes?q={query}'
    response = requests.get(url)
    dados = response.json()
    livros = dados.get('items', [])

    return render(request, 'catalogo/lista_livros.html', {'livros': livros})
