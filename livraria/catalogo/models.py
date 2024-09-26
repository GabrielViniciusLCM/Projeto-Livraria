from django.db import models
from django.contrib.auth.models import User

class Livro(models.Model):
    titulo = models.CharField(max_length=255)
    autor = models.CharField(max_length=255)
    categoria = models.CharField(max_length=255)
    sinopse = models.TextField()
    numero_paginas = models.IntegerField()
    publicadora = models.CharField(max_length=255)
    data_publicacao = models.DateField()
    capa = models.URLField()

    def __str__(self):
        return self.titulo
    
# Modelo representando um item no carrinho
class ItemCarrinho(models.Model):
    livro_id = models.CharField(max_length=255)  # Armazena o ID do livro vindo da API
    titulo = models.CharField(max_length=255)  # Título do livro
    quantidade = models.PositiveIntegerField(default=1)  # Quantidade do livro no carrinho
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)  # Relaciona com o usuário

    def __str__(self):
        return f'{self.quantidade} x {self.titulo}'

# Modelo representando o carrinho do usuário
class Carrinho(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)  # Cada usuário tem um único carrinho
    itens = models.ManyToManyField(ItemCarrinho)  # Carrinho tem vários itens

    def __str__(self):
        return f'Carrinho de {self.usuario.username}'
