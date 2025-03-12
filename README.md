# Sys_Inventory - Inventário de TI

&#x20;&#x20;

O Sys_Inventory é um sistema de gerenciamento de inventário de TI desenvolvido em Django. Ele permite o cadastro, controle e rastreamento de equipamentos, como computadores, telefones e outros dispositivos dentro de uma organização.

## Funcionalidades

- Cadastro e gerenciamento de equipamentos
- Associação de equipamentos a colaboradores
- Histórico de movimentação de equipamentos
- Geração de QR Codes para rastreamento
- Exportação e importação de dados (CSV e XLSX)
- Dashboard com gráficos de análise

## Tecnologias Utilizadas

- Django 4.x
- Python 3.x
- PostgreSQL / SQLite
- Bootstrap para interface
- Chart.js para gráficos
- Django Import-Export para manipulação de arquivos
- Django Money para controle dos campos monetários

## Instalação

### Pré-requisitos

Certifique-se de ter o Python e o Git instalados em seu ambiente.

```bash
# Clone o repositório
git clone https://github.com/joeljonattas/sys_inventory.git
cd sys_inventory

# Crie e ative um ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate  # Windows

# Instale as dependências
pip install -r requirements.txt

# Configure o banco de dados
python manage.py migrate

# Crie um superusuário para acessar o admin
python manage.py createsuperuser

# Inicie o servidor
python manage.py runserver
```

Acesse o sistema em `http://127.0.0.1:8000/`.

## Licença

Este projeto está licenciado sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

### Contato

Caso tenha dúvidas ou sugestões, entre em contato:

- **GitHub**: [joeljonattas](https://github.com/joeljonattas)
- **Email**: [a.joeljonatas12@gmail.com](mailto:a.joeljonatas12@gmail.com)

---

🚀 Desenvolvido por Joel Jonatas Arlt.

