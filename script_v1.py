from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
import time
import os
from dotenv import load_dotenv
import csv

# --- Configuração ---
load_dotenv()
user_login = os.getenv("user_login")
user_key = os.getenv("user_key")
organizacao = os.getenv("organizacao")
navegador = webdriver.Edge()
wait = WebDriverWait(navegador, 20)

navegador.get(organizacao)
navegador.maximize_window()

# --- Login ---
print("Iniciando login...")
user = wait.until(EC.presence_of_element_located(("id", "usuario")))
user.send_keys(user_login)
senha = wait.until(EC.presence_of_element_located(("id", "senha")))
senha.send_keys(user_key)
botao = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn.btn-login.w-100")))
botao.click()
print("Login realizado com sucesso!")




print("Aguardando o link de 'Produtos'...")
link_produtos = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[data-view='produtos']")))
link_produtos.click()
print(" Sucesso! Navegou para a página de produtos.")




try:
    with open('produtos.csv', mode='r', encoding='utf-8') as arquivo_csv:
        leitor_csv = csv.DictReader(arquivo_csv)
        
        for linha in leitor_csv:
            print(f"--- Iniciando cadastro do produto: {linha['nome']} ---")

            
            novo_produto_botao = wait.until(EC.element_to_be_clickable((By.ID, "btn-novo-produto")))
            novo_produto_botao.click()
            modal_produto = wait.until(EC.visibility_of_element_located((By.ID, "modal-produto")))

           
            nome_produto_input = wait.until(EC.visibility_of_element_located((By.ID, "produto-nome")))
            nome_produto_input.send_keys(linha['nome'])

            descricao_input = navegador.find_element(By.ID, "produto-descricao")
            descricao_input.send_keys(linha['descricao'])

            categoria_dropdown_element = navegador.find_element(By.ID, "produto-categoria")
            select_categoria = Select(categoria_dropdown_element)
            select_categoria.select_by_visible_text(linha['categoria'])

            preco_input = navegador.find_element(By.ID, "produto-preco")
            preco_input.send_keys(linha['preco'])
            print("Formulário preenchido.")

            # 3. Clicar em Salvar
            botao_salvar = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#modal-produto button[type='submit']")))
            botao_salvar.click()
            print(f"Produto '{linha['nome']}' salvo com sucesso!")

            
            wait.until(EC.invisibility_of_element_located((By.ID, "modal-produto")))
            print("Modal fechado. Preparando para o próximo produto...")
            time.sleep(1)

except FileNotFoundError:
    print("Erro: Arquivo 'produtos.csv' não encontrado. Verifique se ele está na mesma pasta do script.")
except Exception as e:
    print(f"Ocorreu um erro inesperado durante o cadastro: {e}")


print("--- Fim dos cadastros ---")
time.sleep(5)
print("Fechando o navegador.")
navegador.quit()