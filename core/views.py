
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect
import hashlib
from core.models import Lanche, UsuarioAdmin, UsuarioSimple, Pedido, Transacao
from decimal import Decimal
from django.core.files.storage import FileSystemStorage
import os
from django.http import JsonResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login
from  core.api import lanchesreturn, _produtoSearchID_, _searchUserId, extractcep, enviar_email, enviar_mail_djangoFatec, searchPedidos, get_ip_address, validipCount, getNumberVisualizacao, getvaluepedidos, _getAllUsers_, __GetALLTransacao__
import json
from datetime import datetime
from django.utils import timezone
import webbrowser
from core.payments import gerar_link_pagamento
HttpResponse


def index(request):
    validipCount()
    lanches = Lanche.objects.all()  # Buscar todos os lanches
    lanches_picture = ['img/lanche3.jpg', 'img/lanche2.jpg']
    lanches_data = lanchesreturn()
    # Retornar os dados dos lanches como um dicionário Python
    logado = request.session.get('logadoSimple', False)
    if logado:
        infouser = request.session.get('infouser')
        return render(request, 'index.html', {'lanches': lanches_data, 'lanches_picture': lanches_picture, 'infouser':infouser})
    else:
        return render(request, 'index.html', {'lanches': lanches_data, 'lanches_picture': lanches_picture})




def shop(request):
    lanches_data = lanchesreturn()
    logado = request.session.get('logadoSimple', False)
    if logado:
        infouser = request.session['infouser']
        return render(request, 'shop.html', {'lanches': lanches_data, 'infouser': infouser})
    else:
        return render(request, 'shop.html', {'lanches': lanches_data})



def shopdetail(request):
    return render(request, 'shop-detail.html')


def cart(request):
     return render(request, 'cart.html')



def admin(request):
    logs = False
    try:
       logs = request.session['logado'] 
    except Exception as erro:
        logs = False

    if logs:
        lanches_data = lanchesreturn()
        numVisu = getNumberVisualizacao()
        numPedido =getvaluepedidos()
        users = _getAllUsers_()
        transacao = __GetALLTransacao__()

        return render(request, 'admin.html', {'lanches': lanches_data, 'numVisu': numVisu, 'numpedido': numPedido, 'users': users, 'transacao': transacao})  # Redireciona para a página inicial
    return render(request, 'login.html')
    
@csrf_protect
def validar_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password') 
        
        try:
            # Assume-se que o modelo UsuarioAdmin tem um campo 'email_cifrado'
            usuario = UsuarioAdmin.objects.get(email_cifrado=username)
        except UsuarioAdmin.DoesNotExist:
            usuario = None

        if usuario:
            # Verifica se a senha fornecida corresponde à senha armazenada no banco de dados
            if usuario.check_password(password):
                # Autenticar o usuário e criar a sessão
                login(request, usuario)
                # Armazenar o estado de login na sessão
                request.session['logado'] = True
                lanches_data = lanchesreturn()

                return render(request, 'admin.html', {'lanches': lanches_data})  # Redireciona para a página inicial
            else:
                error_message = 'Credenciais inválidas.'
                request.session['logado'] = False
                return render(request, 'login.html', {'error_message': error_message})  # Retorna o template com a mensagem de erro incluída
        else:
            error_message = 'Usuário não encontrado.'
            return render(request, 'login.html', {'error_message': error_message})  # Retorna o template com a mensagem de erro incluída
    else:
        return HttpResponse('Método não permitido!')
    



@csrf_protect
def create_item(request):
    if request.method == 'POST':
        logado = request.session.get('logado', False)
        if logado:
            # Se o usuário está logado, prossiga com a criação do item
            nome_lanche = request.POST.get('nomeLanche')
            preco = request.POST.get('preco')
            descricao = request.POST.get('descricao')
            quantidade = request.POST.get('quantidade')
            fotos = request.FILES.getlist('fotos')

            # Remova o símbolo de moeda e formatação
            preco_valor = Decimal(preco.replace("R$", "").replace(",", "."))
            if fotos:
                foto = fotos[0]  # Pegar a primeira foto

                # Salvar a foto no diretório core/static/img
                fs = FileSystemStorage(location='core/static/img')
                nome_arquivo = fs.save(foto.name, foto)

                # Obter o caminho completo para o arquivo salvo
                caminho_arquivo = os.path.join('core/static/img', nome_arquivo)
            
            # Criar um novo objeto de lanche e salvar no banco de dados
            lanche = Lanche(
                nome=nome_lanche,
                preco=float(preco_valor),
                descricao=descricao,
                quantidade=quantidade,
                fotos=caminho_arquivo # Supondo que você queira salvar apenas o nome da foto
            )
            lanche.save()

            return admin(request)        
        else:
            # Se o usuário não está logado, redirecione para a página de login
            return render(request, 'login.html')

    

def views_produtos(request, id):
    lanche = _produtoSearchID_(id)
    if lanche:
        totallanches = lanchesreturn()
        infouser = request.session.get('infouser')
        if infouser:
            if len(totallanches) >=1:
                return render(request, 'shop-detail.html', {'lanche': lanche, 'totallanches': totallanches, 'infouser': infouser})
            else:
                return render(request, 'shop-detail.html', {'lanche': lanche, 'totallanches': False, 'infouser': infouser})
        else:
            if len(totallanches)>=1:
                return render(request, 'shop-detail.html', {'lanche': lanche, 'totallanches': totallanches})
            else:
                return render(request, 'shop-detail.html', {'lanche': lanche})


       
            
    else:
        return render(request, 'shop-detail.html', {'error_message': 'Produto não encontrado'})



def accountCliente(request):
    log =None
    try:
        log = request.session['logadoSimple']
    except Exception as e:
        request.session['logadoSimple'] = None

    if log:
        infouser = request.session.get('infouser')
        pedidos = searchPedidos(infouser['id'])
        if len(pedidos) >0:
            return render(request, 'profile.html', {'infouser':infouser, 'pedidos': pedidos})
        else:
            return render(request, 'profile.html', {'infouser':infouser, 'pedidosnone': True})
        
    else:
        return render(request, 'account.html')




def accoutCreate(request):
    if request.method == 'POST':
        name = request.POST.get('name_create')
        razao_social = request.POST.get('razãoSocial_create')
        email = request.POST.get('email_create')
        password = request.POST.get('password_create')
        endereco = request.POST.get('endereco_create')
        cep = request.POST.get('cep_create')
        telefone =  request.POST.get('telefone_create')

        try:
            # Verifica se o email já existe no banco de dados
            UsuarioSimple.objects.get(email_cifrado=email)
            return render(request, 'account.html', {'mensagem': 'Erro, Este email já foi cadastrado. Por favor, tente novamente com outro email.'})
        except UsuarioSimple.DoesNotExist:
            # Hash da senha usando SHA-256
            hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()

            # Criar um novo objeto UsuarioSimple e salvá-lo no banco de dados
            UsuarioSimple.objects.create(
                name=name,
                razao_social=razao_social,
                email_cifrado=email,
                senha_hash=hashed_password,
                endereco=endereco,
                cep=cep,
                telefone =telefone
            )

            return render(request, 'account.html', {'mensagem': 'Usuário criado com sucesso!'})
    else:
        return render(request, 'account.html', {'mensagem': 'Método não permitido!'})


@csrf_protect
def loginAccount(request):
    if request.method == 'POST':
        email = request.POST.get('email_login')
        password = request.POST.get('password_login')

        # Filtrar usuários com o email fornecido
        users = UsuarioSimple.objects.filter(email_cifrado=email)

        if users.exists():  # Verifica se há usuários com esse email
            # Se houver mais de um usuário com o mesmo email, apenas pegue o primeiro
            login = users.first()

            # Verifica se a senha fornecida corresponde à senha armazenada no banco de dados
            if login.check_password(password):
                infouser = _searchUserId(login.id)
                request.session['logadoSimple'] = True
                request.session['infouser'] =infouser 
                return redirect('indexreturn')
            # Redireciona para a página inicial
            else:
                error_message = 'Email ou Senha Incorretos.'
                request.session['logadoSimple'] = False
                
                return render(request, 'account.html', {'login_message': error_message})  # Retorna o template com a mensagem de erro incluída
        else:
            error_message = 'Email ou Senha Incorretos.'
            request.session['logadoSimple'] = False
            return render(request, 'account.html', {'login_message': error_message})  # Retorna o template com a mensagem de erro incluída



@csrf_exempt
def authenticate_user_modal_admin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            usuario = UsuarioAdmin.objects.get(email_cifrado=username)
        except UsuarioAdmin.DoesNotExist:
            usuario = None

        if usuario and usuario.check_password(password):
            return JsonResponse({'authenticated': True})
        else:
            return JsonResponse({'authenticated': False})
    else:
        return JsonResponse({'error': 'Método não permitido'}, status=405)
    


@csrf_exempt
def deleteAdmin(request):
    if request.method == 'POST':
        logado = request.session.get('logado', False)
        if logado:
            cliente_id = request.POST.get('cliente_id')
            if cliente_id:
                try:
                    cliente_id = int(cliente_id)  # Convertendo o ID para inteiro
                    Lanche.objects.filter(id=cliente_id).delete()
                    return JsonResponse({'success': True})
                except Lanche.DoesNotExist:
                    return JsonResponse({'error': 'Lanche não encontrado'}, status=404)
                except ValueError:
                    return JsonResponse({'error': 'ID do cliente não é um número inteiro'}, status=400)
            else:
                return JsonResponse({'error': 'ID do cliente não fornecido'}, status=400)
        else:
            return render(request, 'login.html')
        
        
    else:
        return JsonResponse({'error': 'Método não permitido'}, status=405)


@csrf_protect
def succeedDelete(request):
    logado = request.session.get('logado', False)
    if logado == True:
        return admin(request)
    else:
        return render(request, 'login.html')



@csrf_exempt
def updatetable(request):
    if request.method == 'POST':
        lanches = Lanche.objects.all().values()
        return JsonResponse(list(lanches), safe=False)
    else:
        return JsonResponse({'error': 'Método não permitido'}, status=405)
    


    
@csrf_exempt
def validateProduct(request):
    if request.method == 'POST':
        logado = request.session.get('logadoSimple', False)
        if logado:
            user = request.session.get('infouser')
            infouser = extractcep(user)
            cart_items_json = request.POST.get('cartItems', '[]')
            if cart_items_json:  
                # Verifies if there are data in the JSON before decoding it
                cart_items = json.loads(cart_items_json)
                if len(cart_items) >0:
                    request.session['LanchesPedidos'] = cart_items 
                    total_price = 0.0  # Initialize total price variable

                    for item in cart_items:
                        # Ensure that 'preco' is present in the item dictionary and convert it to float
                        if 'preco' in item:
                            item_price = float(item['preco'])
                            # Add the item price to the total price
                            total_price += item_price

                            
                    return render(request, 'chackout.html', {'infouser': infouser, 'items': cart_items, 'total': total_price})
                else:
                    return render(request, 'cart.html', {'mensageerro': "Não existe nenhum item no seu carrinho"})

            else:
                return render(request, 'chackout.html', {'Mensagem': "error, não ha itens no carrinho"})
        else:
            return render(request, 'account.html', {'mensagem': 'Faça login para prosseguirmos'})
    else:
        return JsonResponse({'error': 'Método não permitido'}, status=405)
    
    
        




# def checout(request):
#     # Aqui você pode adicionar a lógica para manipular os itens do carrinho
  
#         # Obter os itens do carrinho do localStorage, se disponível
#         cart_items_json = request.POST.get('cartItems', '[]')
#         cart_items = json.loads(cart_items_json)
#         # Faça algo com os itens do carrinho, como salvar no banco de dados ou processar um pedido
#         return render(request, 'chackout.html', {'items':cart_items})


def loggout(request):
       logado = request.session.get('logadoSimple', False)
       if logado == True:
           request.session['logadoSimple'] = False
           return redirect('indexreturn')
           
       

def profile(request):
    logado = request.session.get('logadoSimple', False)
    if logado == True:
        infouser = request.session.get('infouser')
        pedidos = searchPedidos(infouser['id'])

        if len(pedidos) >0:
            return render(request, 'profile.html', {'infouser':infouser, 'pedidos': pedidos})
        else:
            return render(request, 'profile.html', {'infouser':infouser, 'pedidosnone': True} )
    else:
        return render(request, 'account.html')
    


# def  checout(request):
#     return render(request, 'chackout.html')


def checkin(request):
        logado = request.session.get('logadoSimple', False)
        pedidos_info = request.session.get('LanchesPedidos')
        if logado:
            if len(pedidos_info) >=1:
                link = gerar_link_pagamento(pedidos_info)
                return redirect(link)
            else:
                return render(request, 'chackout.html', {'PedidoCadastrado': "não a items no carrinho!"})
        else:
            render(request, 'account.html')





def error_404(request, exception):
    return render(request, '404.html', {})



def extractPedidos(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        pedidos = searchPedidos(user_id)
        return JsonResponse({'status': 'success', 'pedidos': pedidos})
    else:
        return JsonResponse({'status': 'error', 'message': 'Método não permitido'}, status=405)
    

def Aproved(request):
    collection_id = request.GET.get('collection_id')
    collection_status = request.GET.get('collection_status')
    payment_id = request.GET.get('payment_id')
    status = request.GET.get('status')
    external_reference = request.GET.get('external_reference')
    payment_type = request.GET.get('payment_type')
    merchant_order_id = request.GET.get('merchant_order_id')
    preference_id = request.GET.get('preference_id')
    site_id = request.GET.get('site_id')
    processing_mode = request.GET.get('processing_mode')
    merchant_account_id = request.GET.get('merchant_account_id')


    #obtendo response retorno api mercado pago, extraindo pelo request.get.get('nome do chave presente no json response retorno mercado pago')
    response_data = {
            'collection_id': collection_id,
            'collection_status': collection_status,
            'payment_id': payment_id,
            'status': status,
            'external_reference': external_reference,
            'payment_type': payment_type,
            'merchant_order_id': merchant_order_id,
            'preference_id': preference_id,
            'site_id': site_id,
            'processing_mode': processing_mode,
            'merchant_account_id': merchant_account_id
        }

    #adicionando essas values no banco de dados
    Transacao.objects.create(
        collection_id =response_data['collection_id'],
        collection_status = response_data['collection_status'],
        payment_id = response_data['payment_id'],
        status = response_data['status'],
        external_reference = response_data['external_reference'],
        payment_type = response_data['payment_type'],
        merchant_order_id = response_data['merchant_order_id'],
        preference_id =response_data['preference_id'],
        site_id =response_data['site_id'],
        processing_mode =response_data['processing_mode'],
        merchant_account_id = response_data['merchant_account_id'],

    )


    user_id = request.session.get('infouser').get('id')  # Obtém o ID do usuário
    pedidos_info = request.session.get('LanchesPedidos') #obtendo os lanches comprados
    # Obtém o usuário correspondente ao ID
    usuario = UsuarioSimple.objects.get(id=user_id) #obtendo informações sobre o usuario que realizou a compra, consultando o banco UsuarioSimple

    preço_total = 0
    # Itera sobre a lista de pedidos e cria um objeto Pedido para cada item
    for pedido_info in pedidos_info:
        preço_total += float(pedido_info.get('preco'))

    pedido = Pedido.objects.create(
        usuario=usuario,
        data_pedido=datetime.now(),  # Data atual
        descricao=pedidos_info, 
        valor_total=preço_total 
    )

    ultimo_pedido = Pedido.objects.filter(usuario=usuario).order_by('-data_pedido').first()

    # Verificar se o pedido foi criado recentemente (por exemplo, nos últimos 5 minutos)
    if ultimo_pedido and (timezone.now() - ultimo_pedido.data_pedido).total_seconds() < 300:
        # Faça algo com o último pedido
        enviar_email(pedidos_info, request.session.get('infouser'), preço_total, ultimo_pedido.id)

    
    #caso a versão do django seja inferior, geralmente esse erro ocorre na fatec. utilize essa function.
    #enviar_mail_djangoFatec(pedidos_info, request.session.get('infouser'), preço_total)
    
    request.session['LanchesPedidos'] = None 
    return render(request, 'chackout.html', {'PedidoCadastrado': "Pedido cadastrado com sucesso!"})















    

