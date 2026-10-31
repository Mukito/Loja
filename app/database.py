import sqlite3
from contextlib import contextmanager
from flask import current_app

@contextmanager
def get_connection():
    """Abre e fecha uma conexão SQLite por operação."""
    conn = sqlite3.connect(current_app.config['DATABASE_PATH'])
    conn.row_factory = sqlite3.Row  # Para retornar resultados como dicionários
    conn.execute('PRAGMA foreign_keys = ON')
    try:
        yield conn
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

def init_db():
    """Cria a tabela CADASTRO automaticamente se ela não existir."""

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS CADASTRO (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                sobrenome TEXT NOT NULL,
                telefone TEXT NOT NULL,
                cpf TEXT NOT NULL UNIQUE,
                email TEXT NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS PEDIDOS (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER NOT NULL,
                total_centavos INTEGER NOT NULL,
                status TEXT NOT NULL DEFAULT 'aguardando_pagamento',
                endereco TEXT NOT NULL,
                pix_payload TEXT NOT NULL,
                criado_em TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (usuario_id) REFERENCES CADASTRO(id)
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ITENS_PEDIDO (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pedido_id INTEGER NOT NULL,
                produto_id TEXT NOT NULL,
                nome_produto TEXT NOT NULL,
                quantidade INTEGER NOT NULL,
                preco_centavos INTEGER NOT NULL,
                FOREIGN KEY (pedido_id) REFERENCES PEDIDOS(id)
            )
        ''')
        conn.commit()

