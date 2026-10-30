from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from app.repositories.user_repository import UserRepository

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/', methods=['GET'])
def index():
    return render_template('index.html', usuario=UserRepository.get_session_user())


@auth_bp.route('/cadastro', methods=['POST'])
def cadastro():
    dados = {
        'nome': request.form.get('nome', '').strip(),
        'sobrenome': request.form.get('sobrenome', '').strip(),
        'telefone': request.form.get('telefone', '').strip(),
        'cpf': request.form.get('cpf', '').strip(),
        'email': request.form.get('email', '').strip(),
        'senha_plana': request.form.get('senha', ''),
    }

    if not all(dados.values()):
        flash('Preencha todos os campos para criar sua conta.', 'error')
        return redirect(url_for('auth.index', abrir='cadastro'))

    sucesso, mensagem = UserRepository.create(**dados)
    if sucesso:
        usuario = UserRepository.get_by_cpf(dados['cpf'])
        session['usuario_id'] = usuario['id']
        flash('Cadastro realizado. Você já está conectado à sua conta.', 'success')
    else:
        flash(mensagem, 'error')
    return redirect(url_for('auth.index', abrir=None if sucesso else 'cadastro'))


@auth_bp.route('/entrar', methods=['POST'])
def entrar():
    cpf = request.form.get('cpf', '').strip()
    senha = request.form.get('senha', '')
    usuario = UserRepository.authenticate(cpf, senha)

    if usuario is None:
        flash('CPF ou senha incorretos. Confira os dados e tente novamente.', 'error')
        return redirect(url_for('auth.index', abrir='entrar'))

    session.clear()
    session['usuario_id'] = usuario['id']
    flash(f'Olá, {usuario["nome"]}! Sessão iniciada com sucesso.', 'success')
    return redirect(url_for('auth.index'))


@auth_bp.route('/sair', methods=['POST'])
def sair():
    session.clear()
    flash('Você saiu da sua conta.', 'success')
    return redirect(url_for('auth.index'))
