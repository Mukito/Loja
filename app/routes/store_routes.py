import io
import json
import re

import qrcode
from flask import Blueprint, abort, current_app, flash, redirect, render_template, request, send_file, session, url_for
from qrcode.image.svg import SvgPathImage

from app.database import get_connection
from app.pix import build_pix_payload
from app.repositories.user_repository import UserRepository
from app.store import PRODUCTS, format_brl

store_bp = Blueprint('store', __name__)


def _user_id():
    return session.get('usuario_id')


def _pix_configured():
    return bool(
        current_app.config.get('PIX_KEY')
        and current_app.config.get('PIX_MERCHANT_NAME')
        and current_app.config.get('PIX_MERCHANT_CITY')
    )


@store_bp.route('/checkout', methods=['GET', 'POST'])
def checkout():
    usuario_id = _user_id()
    if not usuario_id:
        flash('Entre na sua conta para finalizar o pedido.', 'error')
        return redirect(url_for('auth.index', abrir='entrar', next=url_for('store.checkout')))

    if request.method == 'GET':
        usuario = UserRepository.get_session_user()
        pix_pronto = _pix_configured()
        return render_template(
            'checkout.html',
            usuario=usuario,
            pix_pronto=pix_pronto,
            shipping_fee=current_app.config['SHIPPING_FEE_CENTS'],
            free_shipping_from=current_app.config['FREE_SHIPPING_FROM_CENTS'],
            free_shipping_text=format_brl(current_app.config['FREE_SHIPPING_FROM_CENTS']),
            produtos=PRODUCTS,
        )

    if not _pix_configured():
        flash('O recebimento Pix ainda não foi configurado pela loja.', 'error')
        return redirect(url_for('store.checkout'))

    try:
        itens_recebidos = json.loads(request.form.get('itens', '[]'))
        if not isinstance(itens_recebidos, list) or not itens_recebidos:
            raise ValueError

        itens = []
        total_produtos = 0
        for entrada in itens_recebidos:
            produto_id = str(entrada.get('id', ''))
            quantidade = int(entrada.get('quantidade', 0))
            produto = PRODUCTS.get(produto_id)
            if not produto or quantidade < 1 or quantidade > 20:
                raise ValueError
            item = {**produto, 'quantidade': quantidade}
            itens.append(item)
            total_produtos += produto['price'] * quantidade
    except (ValueError, TypeError, AttributeError, json.JSONDecodeError):
        flash('Sua sacola está vazia ou contém itens inválidos. Confira e tente novamente.', 'error')
        return redirect(url_for('auth.index'))

    endereco = {
        'cep': request.form.get('cep', '').strip(),
        'rua': request.form.get('rua', '').strip(),
        'numero': request.form.get('numero', '').strip(),
        'complemento': request.form.get('complemento', '').strip(),
        'bairro': request.form.get('bairro', '').strip(),
        'cidade': request.form.get('cidade', '').strip(),
        'uf': request.form.get('uf', '').strip().upper(),
    }
    if not all(endereco[campo] for campo in ('cep', 'rua', 'numero', 'bairro', 'cidade', 'uf')):
        flash('Preencha o endereço de entrega para continuar.', 'error')
        return redirect(url_for('store.checkout'))
    if not re.fullmatch(r'\d{5}-?\d{3}', endereco['cep']) or not re.fullmatch(r'[A-Z]{2}', endereco['uf']):
        flash('Confira o CEP e a UF informados.', 'error')
        return redirect(url_for('store.checkout'))

    frete = 0 if total_produtos >= current_app.config['FREE_SHIPPING_FROM_CENTS'] else current_app.config['SHIPPING_FEE_CENTS']
    total = total_produtos + frete

    try:
        with get_connection() as conn:
            cursor = conn.execute(
                '''INSERT INTO PEDIDOS (usuario_id, total_centavos, endereco, pix_payload)
                   VALUES (?, ?, ?, ?)''',
                (usuario_id, total, json.dumps(endereco, ensure_ascii=False), ''),
            )
            pedido_id = cursor.lastrowid
            txid = f'CN{pedido_id:08d}'
            payload = build_pix_payload(
                current_app.config['PIX_KEY'],
                current_app.config['PIX_MERCHANT_NAME'],
                current_app.config['PIX_MERCHANT_CITY'],
                total,
                txid,
            )
            conn.execute('UPDATE PEDIDOS SET pix_payload = ? WHERE id = ?', (payload, pedido_id))
            conn.executemany(
                '''INSERT INTO ITENS_PEDIDO (pedido_id, produto_id, nome_produto, quantidade, preco_centavos)
                   VALUES (?, ?, ?, ?, ?)''',
                [(pedido_id, item['id'], item['name'], item['quantidade'], item['price']) for item in itens],
            )
            conn.commit()
    except (ValueError, OSError):
        flash('Não foi possível gerar o Pix. Confira os dados de recebimento da loja.', 'error')
        return redirect(url_for('store.checkout'))

    return redirect(url_for('store.pedido', pedido_id=pedido_id))


@store_bp.route('/pedido/<int:pedido_id>')
def pedido(pedido_id):
    usuario_id = _user_id()
    if not usuario_id:
        return redirect(url_for('auth.index', abrir='entrar'))
    with get_connection() as conn:
        pedido = conn.execute(
            'SELECT * FROM PEDIDOS WHERE id = ? AND usuario_id = ?', (pedido_id, usuario_id)
        ).fetchone()
        if not pedido:
            abort(404)
        itens = conn.execute(
            'SELECT * FROM ITENS_PEDIDO WHERE pedido_id = ? ORDER BY id', (pedido_id,)
        ).fetchall()
    return render_template(
        'pedido_pix.html',
        usuario=UserRepository.get_session_user(),
        pedido=pedido,
        itens=itens,
        endereco=json.loads(pedido['endereco']),
        total=format_brl(pedido['total_centavos']),
    )


@store_bp.route('/pedido/<int:pedido_id>/qrcode.svg')
def pedido_qrcode(pedido_id):
    usuario_id = _user_id()
    if not usuario_id:
        abort(404)
    with get_connection() as conn:
        pedido = conn.execute(
            'SELECT pix_payload FROM PEDIDOS WHERE id = ? AND usuario_id = ?', (pedido_id, usuario_id)
        ).fetchone()
    if not pedido or not pedido['pix_payload']:
        abort(404)
    image = qrcode.make(pedido['pix_payload'], image_factory=SvgPathImage, box_size=8, border=4)
    output = io.BytesIO()
    image.save(output)
    output.seek(0)
    return send_file(output, mimetype='image/svg+xml', max_age=0)
