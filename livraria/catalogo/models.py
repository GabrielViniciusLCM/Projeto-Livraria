from django.db import models

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
