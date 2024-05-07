from django.db import models
import bcrypt
import hashlib
from datetime import datetime
# Create your models here.
class Lanche(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=255)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    descricao = models.TextField()
    quantidade = models.IntegerField()
    fotos = models.CharField(max_length=255)





class UsuarioAdmin(models.Model):
    id = models.AutoField(primary_key=True)
    email_cifrado = models.TextField()
    senha_hash = models.TextField()
    last_login = models.DateTimeField(default=datetime.now)

    def check_password(self, password):
        # Hash a senha fornecida usando SHA-256
        hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
        # Compare o hash gerado com o hash armazenado no banco de dados
        return hashed_password == self.senha_hash

    class Meta:
        db_table = 'useradmin'



class UsuarioSimple(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    razao_social = models.CharField(max_length=100)
    email_cifrado = models.EmailField()
    senha_hash = models.TextField()
    endereco = models.TextField()
    cep = models.CharField(max_length=20)
    telefone = models.CharField(max_length=20, blank=True, null=True) 

    def check_password(self, password):
        # Hash a senha fornecida usando SHA-256
        hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
        # Compare o hash gerado com o hash armazenado no banco de dados
        return hashed_password == self.senha_hash

    class Meta:
        db_table = 'usersimple'



class Pedido(models.Model):
    usuario = models.ForeignKey(UsuarioSimple, on_delete=models.CASCADE)
    data_pedido = models.DateTimeField(auto_now_add=True)
    descricao = models.TextField()
    valor_total = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'pedidos'




class Visualizacao(models.Model):
    num_visualizacoes = models.IntegerField(default=0)

    def adicionar_visualizacao(self):
        self.num_visualizacoes += 1
        self.save()

    def __str__(self):
        return str(self.num_visualizacoes)
    

class IP(models.Model):
    endereco = models.CharField(max_length=45, unique=True)

    def __str__(self):
        return self.endereco




class Transacao(models.Model):
    collection_id = models.CharField(max_length=100)
    collection_status = models.CharField(max_length=100)
    payment_id = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    external_reference = models.CharField(max_length=100, null=True, blank=True)
    payment_type = models.CharField(max_length=100)
    merchant_order_id = models.CharField(max_length=100)
    preference_id = models.CharField(max_length=100)
    site_id = models.CharField(max_length=100)
    processing_mode = models.CharField(max_length=100)
    merchant_account_id = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.collection_id