# Livraria Gabriel

Nesse projeto de livraria é possível buscar livros, adicioná-los a um carrinho de compras, finalizar pedidos e ver o histórico de pedidos. Também possui autenticação de usuários. Este projeto foi desenvolvido usando Django para o backend e HTML/CSS/JavaScript para o frontend.

## Pré-requisitos

Antes de executar o projeto, verifique se você tem os seguintes softwares instalados:

- [Python 3.x](https://www.python.org/downloads/)
- [pip](https://pip.pypa.io/en/stable/installation/)
- [PostgreSQL](https://www.postgresql.org/download/) ou [MySQL](https://dev.mysql.com/downloads/)

## Passo a Passo

1. Clone o repositório:

   ```bash
   git clone https://github.com/seu-usuario/livraria-gabriel.git
   cd livraria-gabriel

2. Instale as dependências do projeto:
   ```bash   
   pip install -r requirements.txt

3. Configure o banco de dados:

Atualize as configurações do banco de dados no arquivo settings.py:

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',  # ou 'django.db.backends.mysql'
        'NAME': 'nome_do_banco',
        'USER': 'seu_usuario',
        'PASSWORD': 'sua_senha',
        'HOST': 'localhost',
        'PORT': '5432', ou 3306 para MySQL
    }
}

4. Migre o banco de dados:

   ```bash
   python manage.py migrate

5. Inicie o servidor de desenvolvimento:

   ```bash
   python manage.py runserver


## Funcionalidades
- Busca de livros pela API do Google Books.
- Adicionar livros ao carrinho de compras.
- Visualizar e remover itens do carrinho.
- Finalizar compras.
- Histórico de compras do usuário (possibilidade de gerar PDF).

## Tecnologias Usadas
- Django
- PostgreSQL / MySQL
- HTML / CSS / JavaScript
- Bootstrap
