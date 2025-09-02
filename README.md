# Automação de Cadastro de Produtos

Este projeto realiza o **cadastro automatizado de produtos** em um painel administrativo utilizando **Selenium WebDriver**, com dados fornecidos via **CSV**.  

---

## ⚙️ Funcionalidades
- Login automático no painel administrativo.
- Leitura de dados do arquivo `produtos.csv`.
- Upload automático da **imagem do produto**.
- Preenchimento dos campos: nome, descrição, categoria e preço.
- Salvamento do produto e iteração até o fim do CSV.

---

## 📂 Estrutura
├── produtos.csv # Arquivo com os dados dos produtos

├── .env # Credenciais de acesso (não versionar)

├── requirements.txt # Dependências do projeto

└── main.py # Script principal da automação

**Exemplo do `produtos.csv`:**
```csv
nome,descricao,categoria,preco,imagem
Pizza Margherita,Clássica com manjericão e muçarela,Pizzas,29.90,imagens/pizza.jpg
Refrigerante Lata,350ml gelado,Bebidas,5.00,imagens/refri.jpg'''


---


- ##🚀 Executando

Clone o repositório:

git clone https://github.com/seu-usuario/automacao-cadastro.git
cd automacao-cadastro


Crie o ambiente virtual e instale as dependências:

pip install -r requirements.txt


Configure o arquivo .env:

user_login=SEU_USUARIO
user_key=SUA_SENHA


Execute o script:

python main.py

📦 Dependências

Python 3.9+

Selenium

python-dotenv

🔒 Segurança

Nunca versione o .env com credenciais reais.

Utilize variáveis de ambiente para manter os dados sensíveis fora do código.

📌 Observações

O seletor dos elementos (By.ID, By.CSS_SELECTOR) pode variar conforme alterações no site.

Ajuste o tempo de espera (WebDriverWait) caso a conexão ou site seja lento.
