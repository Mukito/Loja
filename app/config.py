import os
from pathlib import Path

# BASE_DIR aponta para a pasta raiz do projeto: C:\Users\Master\Documents\Projetos\python\Internet
#BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
BASE_DIR = Path(__file__).resolve().parent.parent

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'chave-secreta-padrao-dev')  # Defina SECRET_KEY no ambiente em produção.
    DATABASE_PATH = str(BASE_DIR / 'database.db')  # Caminho para o banco de dados SQLite
    
