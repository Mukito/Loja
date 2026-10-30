import sqlite3
from flask import current_app

def get_connection():
    """Abre uma nova conexão com o banco de dados."""
    
    conn = sqlite3.connect(current_app.config['DATABASE_PATH'])
    conn.row_factory = sqlite3.Row  # Para retornar resultados como dicionários
    return conn

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
        conn.commit()
    