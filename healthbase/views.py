from django.shortcuts import render
from .models import Conta, Billing, Encomenda, Meupainel
from datetime import datetime 
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages  # Importe o módulo messages
from django.contrib.auth import authenticate, login
from django.utils import timezone
from django.contrib.auth import logout
import webbrowser

def home(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        try:
            # Tente obter o usuário com o email fornecido
            user = Conta.objects.get(email=email)

            # Verifique se a senha está correta
            if user.senha == senha:
                 if user.aceite == True:
                    # O usuário foi autenticado com sucesso
                    # Armazenar o userID na sessão
                    request.session['userID'] = user.userID
                    request.session['nome'] = user.nome
                    return redirect('menu') 
                 if user.aceite == False:
                    return render(request, 'recusar.html') 
            else:
                # Senha incorreta
                return render(request, 'home.html', {'error_message': 'Senha incorreta'})

        except Conta.DoesNotExist:
            # Usuário não encontrado
            return render(request, 'home.html', {'error_message': 'Usuário não encontrado'})

    # Se o método não for POST, exiba o formulário de login
    return render(request, 'home.html')

def registro(request):
    if request.method == 'POST':
        # Processar os dados enviados pelo formulário
        nome = request.POST.get('nome')
        cpf = request.POST.get('cpf')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        num_cartao = request.POST.get('numCartao')
        nome_cartao = request.POST.get('nomeCartao')
        cvv = request.POST.get('cvv')
        val_cartao = request.POST.get('val_cartao')

        # Verificar o CPF
        if not cpf.isdigit() or len(cpf) != 11:
            return render(request, 'registro.html', {'error': 'CPF inválido'})

        # Verificar o número do cartão
        elif not num_cartao.isdigit() or len(num_cartao) != 16:
            return render(request, 'registro.html', {'error': 'Número do cartão inválido'})

        # Verificar o CVV
        elif not cvv.isdigit() or len(cvv) != 3:
            return render(request, 'registro.html', {'error': 'CVV inválido'})

        # Verificar se o cpf ou email já existem no banco de dados
        elif Conta.objects.filter(cpf=cpf).exists():
            return render(request, 'registro.html', {'error': 'Este CPF já existe em nossa base de dados'})
        elif Conta.objects.filter(email=email).exists():
            return render(request, 'registro.html', {'error': 'Email já existe em nossa base de dados'})

        # Definir o valor do campo "Aceite"
        aceitar = 1 if request.POST.get('aceitar') else 0

        # Salvar os dados no banco de dados
        assinante = Conta(nome=nome, cpf=cpf, email=email, senha=senha,
                          numCartao=num_cartao, nomeCartao=nome_cartao, cvv=cvv, val_cartao=val_cartao, aceite=aceitar)
        assinante.save()

        pegacpf= Conta.objects.get(cpf=cpf)
        sessaoid = pegacpf.userID

        meupainel = Meupainel(id=sessaoid, indicador1=0, indicador2=0, indicador3=0)
        meupainel.save()

        # Redirecionar para outra página ou exibir uma mensagem de sucesso
        return render(request, 'sucesso.html') if request.POST.get('aceitar') else render(request, 'recusar.html') 

    # Se o método for GET, renderize o formulário vazio
    return render(request, 'registro.html')

def menu(request):
    user_id = request.session.get('userID')
    nome = request.session.get('nome')
    indicador1 = Meupainel.objects.get(id=user_id).indicador1
    indicador2 = Meupainel.objects.get(id=user_id).indicador2
    indicador3 = Meupainel.objects.get(id=user_id).indicador3
    if request.POST.get('adicionar1'):
        Meupainel.objects.filter(id=user_id).update(indicador1=1)
        indicador1 = Meupainel.objects.get(id=user_id).indicador1
        return render(request, 'menu.html', {'user_id': user_id, 'nome': nome, 'indicador1': indicador1, 'indicador2': indicador2, 'indicador3': indicador3})
    elif request.POST.get('remover1'):   
        Meupainel.objects.filter(id=user_id).update(indicador1=0)
        indicador1 = Meupainel.objects.get(id=user_id).indicador1
        return render(request, 'menu.html', {'user_id': user_id, 'nome': nome, 'indicador1': indicador1, 'indicador2': indicador2, 'indicador3': indicador3})
    elif request.POST.get('adicionar2'):
        Meupainel.objects.filter(id=user_id).update(indicador2=1)
        indicador2 = Meupainel.objects.get(id=user_id).indicador2
        return render(request, 'menu.html', {'user_id': user_id, 'nome': nome, 'indicador1': indicador1, 'indicador2': indicador2, 'indicador3': indicador3})
    elif request.POST.get('remover2'):
        Meupainel.objects.filter(id=user_id).update(indicador2=0)
        indicador2 = Meupainel.objects.get(id=user_id).indicador2
        return render(request, 'menu.html', {'user_id': user_id, 'nome': nome, 'indicador1': indicador1, 'indicador2': indicador2, 'indicador3': indicador3})
    elif request.POST.get('adicionar3'):
        Meupainel.objects.filter(id=user_id).update(indicador3=1)
        indicador3 = Meupainel.objects.get(id=user_id).indicador3
        return render(request, 'menu.html', {'user_id': user_id, 'nome': nome, 'indicador1': indicador1, 'indicador2': indicador2, 'indicador3': indicador3})
    elif request.POST.get('remover3'):
        Meupainel.objects.filter(id=user_id).update(indicador3=0)
        indicador3 = Meupainel.objects.get(id=user_id).indicador3
        return render(request, 'menu.html', {'user_id': user_id, 'nome': nome, 'indicador1': indicador1, 'indicador2': indicador2, 'indicador3': indicador3})
    elif request.method == 'POST':
        conta = Conta.objects.get(userID=user_id)
        num_cartao = conta.numCartao

        # Recupere o produto e o preço do formulário
        produto = request.POST.get('produto')
        preco = float(request.POST.get('preco'))
        powerbi = request.POST.get('powerbi_url')
        data_billing = datetime.now().date()
        hora_compra = datetime.now().time()

        # Insira os dados na tabela Billing
        billing = Billing(
            userID=user_id,
            produto=produto,
            numCartao=num_cartao,
            preco=preco,
            data_compra=data_billing,
            hora_compra=hora_compra,
        )
        billing.save()

        # Redirecione para a página do menu com uma mensagem de sucesso
        webbrowser.open_new_tab(powerbi)
        indicador1 = Meupainel.objects.get(id=user_id).indicador1
        indicador2 = Meupainel.objects.get(id=user_id).indicador2
        indicador3 = Meupainel.objects.get(id=user_id).indicador3
        return render(request, 'menu.html', {'user_id': user_id, 'nome': nome, 'indicador1': indicador1, 'indicador2': indicador2, 'indicador3': indicador3})

    else:
        # Se não for uma requisição POST, redirecione para a página do menu
        user_id = request.session.get('userID')
        nome = request.session.get('nome')

        # Recupere os valores dos indicadores do modelo Meupainel
        indicador1 = Meupainel.objects.get(id=user_id).indicador1
        indicador2 = Meupainel.objects.get(id=user_id).indicador2
        indicador3 = Meupainel.objects.get(id=user_id).indicador3

        return render(request, 'menu.html', {'user_id': user_id, 'nome': nome, 'indicador1': indicador1, 'indicador2': indicador2, 'indicador3': indicador3})

def conta(request):
    # Recupere os dados da conta do usuário (substitua pelo seu método de autenticação)
    user_id = request.session.get('userID')
    conta = Conta.objects.get(userID=user_id)
    nome = request.session.get('nome')
    context = {
        'nome': conta.nome,
        'cpf': conta.cpf,
        'email': conta.email,
        'numCartao': conta.numCartao,
        'cvv': conta.cvv,
        'val_cartao': conta.val_cartao,
        # Adicione outros campos conforme necessário
    }

    return render(request, 'conta.html', context)

def visualizar_cobrancas(request):  
    if request.method == 'POST':
        user_id = request.session.get('userID')
        nome = request.session.get('nome')
        # Caso contrário, filtra as transações com base no user ID e na data
        data_filtro = request.POST.get('data_filtro')
        transacoes = Billing.objects.filter(userID=user_id, data_compra=data_filtro, )

        # Renderiza a página com os dados das transações
        return render(request, 'visualizar_cobrancas.html', {'user_id': user_id, 'nome': nome,'transacoes': transacoes})
    else:
        user_id = request.session.get('userID')
        nome = request.session.get('nome')
        transacoes = Billing.objects.filter(userID=user_id)       
        return render(request, 'visualizar_cobrancas.html', {'user_id': user_id, 'nome': nome, 'transacoes': transacoes})
    
def modificarcartao(request):
    """
    Atualiza os campos numCartao, cvv e val_cartao do modelo com base no userID da sessão.
    """
    user_id = request.session.get('userID')  # Obtém o userID da sessão
    conta = Conta.objects.get(userID=user_id)
    nome = request.session.get('nome')

    if request.method == 'POST':
        # Verifica o número do cartão
        num_cartao = request.POST.get('numCartao')
        if not num_cartao.isdigit() or len(num_cartao) != 16:
            return render(request, 'modificarcartao.html', {'error': 'Número do cartão inválido'})
        nome_cartao = request.POST.get('nomeCartao')
        # Verifica o CVV
        cvv = request.POST.get('cvv')
        if not cvv.isdigit() or len(cvv) != 3:
            return render(request, 'modificarcartao.html', {'error': 'CVV inválido'})

        # Atualiza os campos do modelo diretamente
        Conta.objects.filter(userID=user_id).update(numCartao=num_cartao, cvv=cvv, nomeCartao=nome_cartao, val_cartao=request.POST.get('val_cartao'))
         # Recupera os dados da conta do usuário
        conta = Conta.objects.get(userID=user_id)
        nome = request.session.get('nome')
        context = {
        'nome': nome,
        'numCartao': conta.numCartao,
        'cvv': conta.cvv,
        'val_cartao': conta.val_cartao,
        
    }
        context = {
            'nome': conta.nome,
            'cpf': conta.cpf,
            'email': conta.email,
            'numCartao': conta.numCartao,
            'cvv': conta.cvv,
            'val_cartao': conta.val_cartao,
        
        }
        
        return render(request, 'conta.html', context)

    # Caso o método HTTP não seja POST, renderizar o template com o formulário
    return render(request, 'modificarcartao.html')

def meupainel(request):
    # Suponha que você tenha obtido o valor dos indicadores do banco de dados
    # e armazenado em variáveis (indicador1, indicador2, indicador3)
    user_id = request.session.get('userID')
    indicador1 = Meupainel.objects.get(id=user_id).indicador1
    indicador2 = Meupainel.objects.get(id=user_id).indicador2
    indicador3 = Meupainel.objects.get(id=user_id).indicador3
    
    # Lógica para redirecionar com base nos valores dos indicadores
    if indicador1 == 1 and indicador2 == 0 and indicador3 == 0:
        redirect_url = "http://www.r7.com"
        Billing.objects.create(
            userID=user_id,
            produto="Indicador 1",
            numCartao=Conta.objects.get(userID=user_id).numCartao,
            preco=4.00,
            data_compra=datetime.now().date(),
            hora_compra=datetime.now().time()
        )
    elif indicador1 == 1 and indicador2 == 1 and indicador3 == 0:
        redirect_url = "http://www.uol.com.br"
        Billing.objects.create(
            userID=user_id,
            produto="Indicador 1",
            numCartao=Conta.objects.get(userID=user_id).numCartao,
            preco=4.00,
            data_compra=datetime.now().date(),
            hora_compra=datetime.now().time()
        )
        Billing.objects.create(
            userID=user_id,
            produto="Indicador 2",
            numCartao=Conta.objects.get(userID=user_id).numCartao,
            preco=8.00,
            data_compra=datetime.now().date(),
            hora_compra=datetime.now().time()
        )
    elif indicador1 == 1 and indicador2 == 0 and indicador3 == 1:
        redirect_url = "http://www.facebook.com"
        Billing.objects.create(
            userID=user_id,
            produto="Indicador 1",
            numCartao=Conta.objects.get(userID=user_id).numCartao,
            preco=4.00,
            data_compra=datetime.now().date(),
            hora_compra=datetime.now().time()
        )
        Billing.objects.create(
            userID=user_id,
            produto="Indicador 3",
            numCartao=Conta.objects.get(userID=user_id).numCartao,
            preco=16.00,
            data_compra=datetime.now().date(),
            hora_compra=datetime.now().time()
        )
    elif indicador1 == 1 and indicador2 == 1 and indicador3 == 1:
        redirect_url = "http://www.terra.com.br"
        Billing.objects.create(
            userID=user_id,
            produto="Indicador 1",
            numCartao=Conta.objects.get(userID=user_id).numCartao,
            preco=4.00,
            data_compra=datetime.now().date(),
            hora_compra=datetime.now().time()
        )
        Billing.objects.create(
            userID=user_id,
            produto="Indicador 2",
            numCartao=Conta.objects.get(userID=user_id).numCartao,
            preco=8.00,
            data_compra=datetime.now().date(),
            hora_compra=datetime.now().time()
        )
        Billing.objects.create(
            userID=user_id,
            produto="Indicador 3",
            numCartao=Conta.objects.get(userID=user_id).numCartao,
            preco=16.00,
            data_compra=datetime.now().date(),
            hora_compra=datetime.now().time()
        )
    elif indicador1 == 0 and indicador2 == 1 and indicador3 == 0:
        redirect_url = "http://www.msn.com"
        Billing.objects.create(
            userID=user_id,
            produto="Indicador 2",
            numCartao=Conta.objects.get(userID=user_id).numCartao,
            preco=8.00,
            data_compra=datetime.now().date(),
            hora_compra=datetime.now().time()
        )
    elif indicador1 == 0 and indicador2 == 1 and indicador3 == 1:
        redirect_url = "http://www.noticiasautomotivas.com.br"
        Billing.objects.create(
            userID=user_id,
            produto="Indicador 2",
            numCartao=Conta.objects.get(userID=user_id).numCartao,
            preco=8.00,
            data_compra=datetime.now().date(),
            hora_compra=datetime.now().time()
        )
        Billing.objects.create(
            userID=user_id,
            produto="Indicador 3",
            numCartao=Conta.objects.get(userID=user_id).numCartao,
            preco=16.00,
            data_compra=datetime.now().date(),
            hora_compra=datetime.now().time()
        )
    elif indicador1 == 0 and indicador2 == 0 and indicador3 == 1:
        redirect_url = "http://www.instagram.com"
        Billing.objects.create(
            userID=user_id,
            produto="Indicador 3",
            numCartao=Conta.objects.get(userID=user_id).numCartao,
            preco=16.00,
            data_compra=datetime.now().date(),
            hora_compra=datetime.now().time()
        )
    else:
        redirect_url = "http://www.ig.com.br"

    return redirect(redirect_url)

def encomendar_indicadores(request):
    if request.method == 'POST':
        # Obter o user_id da sessão
        user_id = request.session.get('userID')

        # Obter a descrição enviada pelo usuário
        descricao = request.POST.get('descricao')

        # Criar uma nova encomenda no banco de dados
        encomenda = Encomenda(userID=user_id, descricao=descricao)
        encomenda.save()

        return render(request, 'encomendar_sucesso.html')  

    # Se o método for GET, renderize o formulário vazio
    return render(request, 'encomendar_indicadores.html')

def encomendar_sucesso(request):
    return render(request, 'encomendar_sucesso.html')

def logout_view(request):
    logout(request)
    return redirect('home') 