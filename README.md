# Casa Nativa

Loja virtual demonstrativa feita com Flask e SQLite. A página inicial apresenta a vitrine e permite criar conta ou entrar usando CPF e senha. A sacola persiste no navegador, o checkout salva o pedido no banco e gera QR Code e código Pix Copia e Cola. O cadastro e as tabelas de pedidos criam a base `database.db` automaticamente na primeira execução.

<img width="1907" height="907" alt="image" src="https://github.com/user-attachments/assets/268c4cce-88c8-4535-ab59-008aa454bb9f" />
<img width="1898" height="824" alt="image" src="https://github.com/user-attachments/assets/f55bcb04-03a9-4fd6-8848-c2dfb38b7606" />
<img width="1353" height="876" alt="image" src="https://github.com/user-attachments/assets/88fb607f-bfc9-4b30-a85d-00cbbb16312a" />
<img width="1595" height="840" alt="image" src="https://github.com/user-attachments/assets/1eaffc90-d825-4bbf-8a7a-c5a0d8533b0c" />



<img width="776" height="911" alt="image" src="https://github.com/user-attachments/assets/7b2ad559-b229-4b4e-ba73-a05adea72e3b" />
<img width="751" height="911" alt="image" src="https://github.com/user-attachments/assets/6ce72eae-5c0d-4b0f-bd6e-66d3a4a5aaec" />





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
