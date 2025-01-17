from django.shortcuts import render,redirect
from .models import *
# Create your views here.

def homepage(request):
   banners = Banner.objects.filter(ativo=True)
   context = {"banners": banners}
   return render(request, 'homepage.html', context)

def loja(request, nome_categoria=None):
   produtos = Produto.objects.filter(ativo=True)
   if nome_categoria:
      produtos = produtos.filter(categoria__nome=nome_categoria)
   context = {"produtos": produtos}
   return render(request, 'loja.html', context)

def ver_produto(request, id_produto, id_cor=None):
   tem_estoque = False
   cores = {}
   tamanhos = {}
   cor = None
   cor_selecionada = None
   if id_cor:
      cor_selecionada = Cor.objects.get(id=id_cor)
   produto = Produto.objects.get(id=id_produto)
   itens_estoque = ItemEstoque.objects.filter(produto=produto, quantidade__gt=0) #django-queryset
   if len(itens_estoque) > 0:
      tem_estoque = True
      cores = {item.cor for item in itens_estoque}
      if id_cor:
         itens_estoque = ItemEstoque.objects.filter(produto=produto, quantidade__gt=0, cor__id=id_cor)
         tamanhos = {item.tamanho for item in itens_estoque}
   context = {"produto": produto, "tem_estoque": tem_estoque, "cores": cores, "tamanhos": tamanhos,
              "nome_cor_selecionada": cor_selecionada}
   return render(request,"ver_produto.html", context)


def adicionar_carrinho(request, id_produto):
    if request.method == "POST" and id_produto:
        dados = request.POST.dict()
        tamanho = dados.get("tamanho")
        id_cor = dados.get("cor")
        if not tamanho:
            return redirect('loja')
        resposta = redirect('carrinho')
        # pegar o cliente
        if request.user.is_authenticated:
            cliente = request.user.cliente
        else:
            return redirect('loja')
        pedido, criado = Pedido.objects.get_or_create(cliente=cliente, finalizado=False)
        item_estoque = ItemEstoque.objects.get(
            produto__id=id_produto, tamanho=tamanho, cor__id=id_cor)
        item_pedido, criado = ItemPedido.objects.get_or_create(item_estoque=item_estoque, pedido=pedido)
        item_pedido.quantidade += 1
        item_pedido.save()
        return redirect('carrinho')
    else:
        return redirect('loja')

def remover_carrinho(request):
   return redirect('carrinho')


def carrinho(request):
   if request.user.is_authenticated:
      cliente = request.user.cliente
   pedido, criado = Pedido.objects.get_or_create(cliente=cliente, finalizado=False)
   itens_pedido = ItemPedido.objects.filter(pedido=pedido)
   context = {"itens_pedido": itens_pedido, "pedido": pedido}
   return render(request, 'carrinho.html', context)

def checkout(request):
   return render(request, 'checkout.html')

def minha_conta(request):
   return render(request, 'usuario/minha_conta.html')

def login(request):
   return render(request, 'usuario/login.html')

# TODO sempre que o usuario criar uma conta no nosso site a gente vai criar um cliente para ele