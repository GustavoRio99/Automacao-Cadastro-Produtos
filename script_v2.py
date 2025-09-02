from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import csv
from dotenv import load_dotenv

load_dotenv()
user_login = os.getenv("user_login")
user_key = os.getenv("user_key")
organizacao = os.getenv("organizacao")
# --- Configuração ---
navegador = webdriver.Edge()
wait = WebDriverWait(navegador, 20)

navegador.get(organizacao)
navegador.maximize_window()

print("Iniciando login...")
user = wait.until(EC.presence_of_element_located((By.ID, "usuario")))
user.send_keys(user_login)
senha = wait.until(EC.presence_of_element_located((By.ID, "senha")))
senha.send_keys(user_key)
botao = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn.btn-login.w-100")))
botao.click()
print("Login realizado com sucesso!")

# --- Navegar até Produtos ---
print("Aguardando o link de 'Produtos'...")
link_produtos = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[data-view='produtos']")))
link_produtos.click()
print("Sucesso! Página de produtos aberta.")

# --- Ler CSV e carregar imagens ---
try:
    with open('produtos.csv', mode='r', encoding='utf-8') as arquivo_csv:
        leitor_csv = csv.DictReader(arquivo_csv)

        for linha in leitor_csv:
            caminho_imagem = os.path.abspath(linha['imagem'])
            print(f"\n--- Upload da imagem: {caminho_imagem} ---")

            if not os.path.exists(caminho_imagem):
                print(f"⚠️ Arquivo não encontrado: {caminho_imagem}")
                continue

            try:
                # 1. Abrir modal de novo produto
                novo_produto_botao = wait.until(EC.element_to_be_clickable((By.ID, "btn-novo-produto")))
                novo_produto_botao.click()
                modal_produto = wait.until(EC.visibility_of_element_located((By.ID, "modal-produto")))

                # 2. Carregar imagem
                imagem_input = wait.until(EC.presence_of_element_located((By.ID, "produto-foto")))
                imagem_input.send_keys(caminho_imagem)
                print("✅ Imagem carregada com sucesso!")

                # 3. Preencher o Formulário com CSV
                nome_produto_input = wait.until(EC.visibility_of_element_located((By.ID, "produto-nome")))
                nome_produto_input.send_keys(linha['nome'])

                descricao_input = navegador.find_element(By.ID, "produto-descricao")
                descricao_input.send_keys(linha['descricao'])

                categoria_dropdown_element = navegador.find_element(By.ID, "produto-categoria")
                select_categoria = Select(categoria_dropdown_element)
                select_categoria.select_by_visible_text(linha['categoria'])

                preco_input = navegador.find_element(By.ID, "produto-preco")
                preco_input.clear()
                preco_input.send_keys(linha['preco'])
                print("Formulário preenchido.")

                # 4. Clicar em Salvar
                botao_salvar = wait.until(EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, "#modal-produto button[type='submit']")))
                botao_salvar.click()
                print(f"Produto '{linha['nome']}' salvo com sucesso!")

                # 5. Esperar o Modal Desaparecer
                wait.until(EC.invisibility_of_element_located((By.ID, "modal-produto")))
                print("Modal fechado. Preparando para o próximo produto...")
                time.sleep(1)

            except Exception as erro_produto:
                print(f"❌ Erro ao processar produto '{linha.get('nome', 'Desconhecido')}': {erro_produto}")
                continue

except FileNotFoundError:
    print("Erro: Arquivo 'produtos.csv' não encontrado.")
except Exception as e:
    print(f"Ocorreu um erro inesperado: {e}")

# --- Finalização ---
print("\n--- Fim do upload de imagens ---")
time.sleep(3)
navegador.quit()
