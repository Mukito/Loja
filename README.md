# Casa Nativa

Loja virtual demonstrativa feita com Flask e SQLite. A página inicial apresenta a vitrine e permite criar conta ou entrar usando CPF e senha. O cadastro cria a base `database.db` automaticamente na primeira execução.

## Executar localmente

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python run.py
```

Depois, acesse http://127.0.0.1:5000.

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
