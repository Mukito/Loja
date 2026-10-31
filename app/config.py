import os
from pathlib import Path
from dotenv import load_dotenv

# BASE_DIR aponta para a pasta raiz do projeto: C:\Users\Master\Documents\Projetos\python\Internet
#BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / '.env')

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'chave-secreta-padrao-dev')  # Defina SECRET_KEY no ambiente em produção.
    DATABASE_PATH = str(BASE_DIR / 'database.db')  # Caminho para o banco de dados SQLite
    PIX_KEY = os.environ.get('PIX_KEY', '').strip()
    PIX_MERCHANT_NAME = os.environ.get('PIX_MERCHANT_NAME', 'CASA NATIVA').strip()
    PIX_MERCHANT_CITY = os.environ.get('PIX_MERCHANT_CITY', '').strip()
    SHIPPING_FEE_CENTS = int(os.environ.get('SHIPPING_FEE_CENTS', '1990'))
    FREE_SHIPPING_FROM_CENTS = int(os.environ.get('FREE_SHIPPING_FROM_CENTS', '29900'))
    
