import re
import sqlite3

from werkzeug.security import check_password_hash, generate_password_hash

from app.database import get_connection


def _normalizar_cpf(cpf: str) -> str:
    return re.sub(r'\D', '', cpf or '')


class UserRepository:
    @staticmethod
    def create(nome: str, sobrenome: str, telefone: str, cpf: str, email: str, senha_plana: str):
        """Cria um usuário, guardando somente o hash da senha."""
        cpf = _normalizar_cpf(cpf)
        senha_hash = generate_password_hash(senha_plana)

        try:
            with get_connection() as conn:
                conn.execute(
                    '''
                    INSERT INTO CADASTRO (nome, sobrenome, telefone, cpf, email, password)
                    VALUES (?, ?, ?, ?, ?, ?)
                    ''',
                    (nome, sobrenome, telefone, cpf, email, senha_hash),
                )
                conn.commit()
            return True, 'Usuário criado com sucesso.'
        except sqlite3.IntegrityError as err:
            if 'UNIQUE constraint failed: CADASTRO.cpf' in str(err):
                return False, 'Este CPF já está cadastrado. Entre na sua conta.'
            return False, 'Não foi possível criar o cadastro.'
        except sqlite3.Error:
            return False, 'Ocorreu um erro ao acessar o banco de dados.'

    @staticmethod
    def get_by_cpf(cpf: str):
        cpf = _normalizar_cpf(cpf)
        with get_connection() as conn:
            return conn.execute(
                '''
                SELECT id, nome, sobrenome, telefone, cpf, email, password
                FROM CADASTRO
                WHERE replace(replace(replace(cpf, '.', ''), '-', ''), ' ', '') = ?
                LIMIT 1
                ''',
                (cpf,),
            ).fetchone()

    @staticmethod
    def authenticate(cpf: str, senha: str):
        usuario = UserRepository.get_by_cpf(cpf)
        if usuario and check_password_hash(usuario['password'], senha):
            return usuario
        return None

    @staticmethod
    def get_session_user():
        from flask import session

        usuario_id = session.get('usuario_id')
        if not usuario_id:
            return None
        with get_connection() as conn:
            return conn.execute(
                'SELECT id, nome, sobrenome, email FROM CADASTRO WHERE id = ?',
                (usuario_id,),
            ).fetchone()
