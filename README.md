# Casa Nativa

Loja virtual demonstrativa feita com Flask e SQLite. A página inicial apresenta a vitrine e permite criar conta ou entrar usando CPF e senha. A sacola persiste no navegador, o checkout salva o pedido no banco e gera QR Code e código Pix Copia e Cola. O cadastro e as tabelas de pedidos criam a base `database.db` automaticamente na primeira execução.

## Executar localmente

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python run.py
```

Depois, acesse http://127.0.0.1:5000.

## Configurar recebimentos Pix

Antes de aceitar pedidos, configure a chave Pix registrada no banco, o nome do recebedor e a cidade da conta. Não coloque esses dados no código nem os envie ao GitHub.

```powershell
$env:PIX_KEY = "sua-chave-pix"
$env:PIX_MERCHANT_NAME = "NOME DO RECEBEDOR"
$env:PIX_MERCHANT_CITY = "SUA CIDADE"
python run.py
```

O fluxo gera uma cobrança Pix estática com valor e identificador do pedido. O pedido fica como `aguardando_pagamento`; a confirmação do recebimento é manual no banco da loja. Não há integração de webhook ou confirmação automática. O frete padrão é R$ 19,90 e fica grátis a partir de R$ 299,00; os valores podem ser ajustados pelas variáveis `SHIPPING_FEE_CENTS` e `FREE_SHIPPING_FROM_CENTS`.

Para sessões persistentes em produção, configure a variável de ambiente `SECRET_KEY` com um valor aleatório e mantenha o banco de dados fora do controle de versão. A base local e o ambiente virtual são ignorados pelo Git.

## Estrutura

```text
app/
├── repositories/       # Acesso aos dados de usuários
├── routes/             # Cadastro, login, logout e página da loja
├── static/             # CSS
└── templates/          # Interface HTML
database.db             # Criado automaticamente na primeira execução
run.py                  # Inicialização do servidor Flask
requirements.txt        # Dependências
```
