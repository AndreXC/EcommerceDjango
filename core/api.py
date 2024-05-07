from core.models import *
import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText    
from django.core.mail import send_mail
from django.conf import settings
from core.body_html import _email_Body, htmlFatec
import socket

def lanchesreturn():
    lanches = Lanche.objects.all()  # Buscar todos os lanches

    lanches_data = {}  # Dicionário para armazenar os dados dos lanches

    for lanche in lanches:
        lanches_data[lanche.nome] = {  # Usando o nome do lanche como chave
            'id': lanche.id,
            'nome': lanche.nome,
            'preco': lanche.preco,
            'descricao': lanche.descricao,
            'quantidade': lanche.quantidade,
            'fotos': lanche.fotos
        }
    return lanches_data



def _produtoSearchID_(id):
    try:
        lanche = Lanche.objects.get(id=id)
        return {
            'id': lanche.id,
            'nome': lanche.nome,
            'preco': lanche.preco,
            'descricao': lanche.descricao,
            'quantidade': lanche.quantidade,
            'fotos': lanche.fotos
        }
    except Lanche.DoesNotExist:
        return None
    


def _searchUserId(id): 
    User = UsuarioSimple.objects.get(id=id)
    return {
            'id': User.id,
            'nome': User.name,
            'email': User.email_cifrado,
            'endereco': User.endereco,
            'razaosocial': User.razao_social, 
            "cep": User.cep,
            "telefone": User.telefone
        }
    



def _getAllUsers_():
        User = UsuarioSimple.objects.all()
        userdata = {}  # Dicionário para armazenar os dados dos lanches

        for user in User:
            userdata[user.name] = {
                'id': user.id,
                'nome': user.name,
                'email': user.email_cifrado,
                'endereco': user.endereco,
                'razaosocial': user.razao_social, 
                "cep": user.cep,
                "telefone": user.telefone,
                "senha": user.senha_hash
            }
        return userdata
    

def extractcep(user):
    cep = user['cep']
    # Certifique-se de usar aspas duplas externas para a f-string para evitar conflito com as aspas simples dentro
    response = requests.get(f"https://viacep.com.br/ws/{cep}/json/")
    
    if response.status_code == 200:
        dados = response.json()
        cidade = dados.get('localidade', 'Cidade não encontrada')
        user['cidade']= cidade
        return user
    else:
        user['cidade']= 'Erro ao consultar o CEP' 

        return user
    




def searchPedidos(idcompra):
    pedidos = Pedido.objects.filter(usuario_id=idcompra)
    pedidos_data = []
    for pedido in pedidos:
        try:
            # Avalia a string como uma expressão Python, convertendo-a em uma lista de dicionários
            descricao = eval(pedido.descricao)
            if not isinstance(descricao, list):
                raise ValueError('A descrição não é uma lista')
        except (SyntaxError, ValueError):
            # Se a descrição não puder ser avaliada como uma lista de dicionários, defina como uma lista vazia
            descricao = []

        pedidos_data.append({
            'id_user': pedido.usuario.id,
            'id_compra': pedido.id,
            'data': pedido.data_pedido,
            'descricao': descricao,
            'valortotal': pedido.valor_total,
        })

    return pedidos_data





def enviar_email(infoPedidos, infouser, preçoTotal, id):
    # Configurações do e-mail
    recipient = infouser['email']
    subject = f'E-commerce'
    message = _email_Body(infoPedidos, preçoTotal, infouser, id)  # Obtém o conteúdo HTML do e-mail

    # Envia o e-mail
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,  # E-mail remetente configurado em settings.py
        [recipient],  # Lista de destinatários
        html_message=message  # Especifica que a mensagem é HTML
    )




def enviar_mail_djangoFatec(infoPedidos, infouser, preçoTotal):
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText

    # Configurações do servidor SMTP do Outlook
    smtp_server = 'smtp.office365.com'
    smtp_port = 587  # Porta SMTP do servidor
    smtp_username = 'krlanches2020@outlook.com'
    smtp_password = 'Teste2020#'


    # Crie o objeto MIMEMultipart
    msg = MIMEMultipart()

    # Configurações do email
    msg['From'] = 'krlanches2020@outlook.com'
    msg['To'] = f"{infouser['email']}"
    msg['Subject'] = 'Seus pedidos no E-commerce'

    body = MIMEText(htmlFatec(infoPedidos, infouser, preçoTotal), 'html')

    # Adiciona o conteúdo HTML ao email
    msg.attach(body)

    # Conexão com o servidor SMTP
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()  # Inicia a conexão TLS (opcional)
    server.login(smtp_username, smtp_password)  # Login no servidor SMTP

    # Envio do email
    server.sendmail(smtp_username, f"{infouser['email']}", msg.as_string())

    # Encerra a conexão com o servidor SMTP
    server.quit()




def get_ip_address():
    hostname = socket.gethostname()    
    ip_address = socket.gethostbyname(hostname)
    return ip_address




def validipCount():
    ip =  get_ip_address()
    # Verifica se o IP está no banco de dados
    ip_obj, created = IP.objects.get_or_create(endereco=ip)
    
    # Se o IP já existir no banco de dados, incrementa o número de visualizações
    if created:
        visualizacao = Visualizacao.objects.first()  # Supondo que você queira sempre atualizar a mesma entrada de visualização
        if visualizacao is None:
            visualizacao = Visualizacao.objects.create(num_visualizacoes=0)  # Cria uma nova entrada de visualização se não existir
        visualizacao.adicionar_visualizacao()  
        visualizacao.__str__()


def getNumberVisualizacao():
    num =  Visualizacao.objects.first() 
    return num




def getvaluepedidos():
    pedidosall = Pedido.objects.all()
    contNumbers = 0

    for pedido in pedidosall:
        try:
            # Avalia a string como uma expressão Python, convertendo-a em uma lista de dicionários
            descricao = eval(pedido.descricao)
            if not isinstance(descricao, list):
                pass
        except (SyntaxError, ValueError):
            # Se a descrição não puder ser avaliada como uma lista de dicionários, defina como uma lista vazia
            descricao = []

        if len(descricao) == 0:
            pass
        else:
            for dictPedido in descricao:
                contNumbers += float(dictPedido['preco'])

        

    return round(contNumbers,2)


def __GetALLTransacao__():
    transacoes = []
    for transacao in Transacao.objects.all():
        transacao_dict = {
            'collection_id': transacao.collection_id,
            'collection_status': transacao.collection_status,
            'payment_id': transacao.payment_id,
            'status': transacao.status,
            'external_reference': transacao.external_reference,
            'payment_type': transacao.payment_type,
            'merchant_order_id': transacao.merchant_order_id,
            'preference_id': transacao.preference_id,
            'site_id': transacao.site_id,
            'processing_mode': transacao.processing_mode,
            'merchant_account_id': transacao.merchant_account_id,
            'created_at': transacao.created_at
        }
        transacoes.append(transacao_dict)
    return transacoes

        
            
    







