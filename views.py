from django.shortcuts import render
from .models import Conta, Billing
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages  # Importe o módulo messages
from django.contrib.auth import authenticate, login
from django.utils import timezone
from django.contrib.auth import logout

def home(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        try:
            # Tente obter o usuário com o email fornecido
            user = Conta.objects.get(email=email)

            # Verifique se a senha está correta
            if user.senha == senha:
                # O usuário foi autenticado com sucesso
                # Armazenar o userID na sessão
                request.session['userID'] = user.userID
                request.session['nome'] = user.nome
                return redirect('menu') 
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


        # Salvar os dados no banco de dados
        assinante = Conta(nome=nome, cpf=cpf, email=email, senha=senha,
                              numCartao=num_cartao, nomeCartao=nome_cartao, cvv=cvv, val_cartao=val_cartao)
        assinante.save()

        # Redirecionar para outra página ou exibir uma mensagem de sucesso
        return render(request, 'sucesso.html')

    # Se o método for GET, renderize o formulário vazio
    return render(request, 'registro.html')

def menu(request):    
    if request.method == 'POST':
        # Recupere o userID da sessão
        user_id = request.session.get('userID')
        nome = request.session.get('nome')
        message = request.GET.get('message') 
        # Recupere o numCartao da Conta associada ao userID
        conta = Conta.objects.get(userID=user_id)
        num_cartao = conta.numCartao

        # Recupere o produto e o preço do formulário
        produto = request.POST.get('produto')
        preco = float(request.POST.get('preco'))

        # Insira os dados na tabela healthbase_billing
        billing = Billing(userID=user_id, produto=produto, numCartao=num_cartao, preco=preco)
        billing.save()
        # Redirecione para a página do menu com uma mensagem de sucesso
        return render(request, 'menu.html', {'user_id': user_id, 'nome': nome, 'message': message})
    else:
        # Se não for uma requisição POST, redirecione para a página do menu
        user_id = request.session.get('userID')
        nome = request.session.get('nome')        
        return render(request, 'menu.html', {'user_id': user_id, 'nome': nome})

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
        # Adicione outros campos conforme necessário
    }
        context = {
            'nome': conta.nome,
            'cpf': conta.cpf,
            'email': conta.email,
            'numCartao': conta.numCartao,
            'cvv': conta.cvv,
            'val_cartao': conta.val_cartao,
        # Adicione outros campos conforme necessário
        }
        # Redireciona para alguma página de sucesso (você pode personalizar isso)
        return render(request, 'conta.html', context)

    # Caso o método HTTP não seja POST, renderize o template com o formulário
    return render(request, 'modificarcartao.html')

def logout_view(request):
    logout(request)
    return redirect('home') 