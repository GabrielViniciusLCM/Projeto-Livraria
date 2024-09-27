from django.db import models
from django.contrib.auth.models import User, AbstractUser


class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=100)
    nome = models.CharField(max_length=100)
    endereco = models.CharField(max_length=255)
    email = models.CharField(max_length=255)

    def __str__(self):
        return self.nome

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
    

class ItemCarrinho(models.Model):
    livro_id = models.CharField(max_length=255) 
    titulo = models.CharField(max_length=255) 
    quantidade = models.PositiveIntegerField(default=1)  
    usuario = models.ForeignKey(User, on_delete=models.CASCADE) 

    def __str__(self):
        return f'{self.quantidade} x {self.titulo}'


class Carrinho(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)  
    itens = models.ManyToManyField(ItemCarrinho) 

    def __str__(self):
        return f'Carrinho de {self.usuario.username}'
    
class Pedido(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    itens = models.ManyToManyField(ItemCarrinho)
    data_pedido = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Pedido #{self.id} - {self.usuario.username} - {self.data_pedido}'
