# Casa Nativa

Loja virtual demonstrativa feita com Flask e SQLite. A página inicial apresenta a vitrine e permite criar conta ou entrar usando CPF e senha. O cadastro cria a base `database.db` automaticamente na primeira execução.

<img width="1907" height="907" alt="image" src="https://github.com/user-attachments/assets/268c4cce-88c8-4535-ab59-008aa454bb9f" />
<img width="1898" height="824" alt="image" src="https://github.com/user-attachments/assets/f55bcb04-03a9-4fd6-8848-c2dfb38b7606" />



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
