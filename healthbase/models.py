from django.db import models

class Conta(models.Model):
    userID = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=32)
    cpf = models.PositiveIntegerField(unique=True)
    email = models.EmailField(unique=True)
    senha = models.CharField(max_length=48)
    numCartao = models.PositiveIntegerField()
    nomeCartao = models.CharField(max_length=32)
    cvv = models.PositiveSmallIntegerField()
    val_cartao = models.DateField()
    aceite = models.BooleanField()
    valor_plano = models.IntegerField()


class Billing(models.Model):
    transactionID = models.AutoField(primary_key=True)
    userID = models.IntegerField()
    produto = models.CharField(max_length=32)
    numCartao = models.DecimalField(max_digits=16, decimal_places=0, null=False)
    preco = models.FloatField(null=False)
    data_compra = models.DateField() 
    hora_compra = models.TimeField() 


class Encomenda(models.Model):
    id = models.AutoField(primary_key=True)
    userID = models.IntegerField()
    descricao = models.CharField(max_length=1000)

class Meupainel(models.Model):
    id = models.IntegerField(primary_key=True)
    indicador1 = models.IntegerField()
    indicador2 = models.IntegerField()
    indicador3 = models.IntegerField()