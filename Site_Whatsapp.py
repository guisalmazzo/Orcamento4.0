from flask import Flask, render_template, request, redirect, url_for
from fpdf import FPDF
import mariadb
import datetime
import locale
import webbrowser
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time
import os

# Configurando a localização para o Brasil
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

app = Flask(__name__)

# Rota para logout
@app.route('/logout', methods=['POST'])
def logout():
    return redirect(url_for('login'))
    
# Rota para login
@app.route("/")
def login():
    return render_template("tela_login.html")

# Conexão com o banco de dados
conexao = mariadb.connect(
    user="root",
    password="uni@2024",
    host="localhost",
    port=3306,
    database="banco2.0"
)
# Criando cursor
sql = conexao.cursor()

# Rota para homepage
@app.route("/homepage.html")
def homepage():
    return render_template("homepage.html")

# Função para enviar PDF via WhatsApp
def enviar_via_whatsapp(nome_cliente, arquivo_pdf):
    # Caminho para o driver do Chrome (ajuste conforme necessário)
    chrome_driver_path = "C:/chromedriver/chromedriver.exe"
    
    # Configurando o WebDriver do Chrome usando Service
    service = Service(chrome_driver_path)
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=service, options=options)
    
    try:
        # Abrindo o WhatsApp Web
        driver.get("https://web.whatsapp.com")
        
        # Esperar o usuário escanear o QR Code
        time.sleep(15)  # Tempo para escanear o QR code (ajustar se necessário)
        
        # Procurar pelo contato usando o nome do cliente
        search_box = driver.find_element(By.XPATH, "//div[@title='Caixa de texto de pesquisa']")
        search_box.click()
        search_box.send_keys(nome_cliente)
        search_box.send_keys(Keys.ENTER)
        
        time.sleep(5)  # Aguarda o contato ser encontrado e a conversa abrir
        
        # Anexar o arquivo PDF
        attachment_box = driver.find_element(By.CSS_SELECTOR, "span[data-icon='clip']")
        attachment_box.click()
        
        # Carregar o arquivo PDF
        file_input = driver.find_element(By.CSS_SELECTOR, "input[type='file']")
        file_input.send_keys(os.path.abspath(arquivo_pdf))
        
        time.sleep(5)  # Aguardar o upload do arquivo
        
        # Enviar a mensagem
        send_button = driver.find_element(By.XPATH, "//span[@data-icon='send']")
        send_button.click()
        
        time.sleep(5)  # Aguardar o envio da mensagem
    
    finally:
        # Fechar o navegador após o envio
        driver.quit()

# Rota para salvar os dados no banco
@app.route("/salvar", methods=['POST'])
def salvar_dados():
    if request.method == 'POST':
        cliente = request.form['cliente']
        endereco = request.form['endereco']
        telefone = request.form['telefone']
        descricao_projeto = request.form['descricao']
        carga_horária = float(request.form['execucao'])
        valor_hora = float(request.form['hora'])
        valor_material = float(request.form['material'])
        prazo = request.form['entrega']  
        valor_final = carga_horária * valor_hora + valor_material
       
        data_orcamento = datetime.datetime.now().strftime('%d/%m/%Y')

        try:
            sql.execute("INSERT INTO clientes(data_orcamento, orcamento, cliente, endereco, telefone, descricao_projeto, carga_horária, valor_hora, valor_material, prazo, valor_final) VALUES (?,?,?,?,?,?,?,?,?,?,?)", 
                        (data_orcamento, None, cliente, endereco, telefone, descricao_projeto, carga_horária, valor_hora, valor_material, prazo, valor_final))
            conexao.commit()

            # Obtendo o número do último orçamento inserido
            sql.execute("SELECT LAST_INSERT_ID()")
            orcamento = sql.fetchone()[0]
            filename = f"Orçamento_{orcamento}.pdf"  # Incluir número no orçamento

            # Gerando o PDF
            pdf = FPDF()
            pdf.add_font('Arial', '', 'C:/Windows/Fonts/arial.ttf', uni=True)
            pdf.add_page()
            pdf.set_font('Arial', 'B', 14)
            pdf.image("C:/Users/guilherme.MCITRUS/Pictures/PI/orcamento.png", x=0, y=0)
            pdf.set_text_color(255, 255, 255)
            pdf.text(173, 13, str(orcamento))
            pdf.text(173, 26, data_orcamento)
            pdf.text(73, 146, cliente)
            pdf.text(73, 160, endereco)
            pdf.text(73, 174, telefone)
            pdf.text(73, 188, descricao_projeto)
            pdf.text(95, 203, str(prazo))
            pdf.text(95, 218, locale.currency(valor_final, grouping=True))
            pdf.output(f'C:/Users/guilherme.MCITRUS/Pictures/PI/{filename}')
            
            # Redirecionar para a página de envio após salvar os dados
            return redirect(url_for('enviar_orcamento', cliente=cliente, arquivo_pdf=filename))

        except mariadb.Error as e:
            print(f"Erro ao salvar os dados: {e}")
            return "Erro ao salvar os dados"

# Rota para enviar o orçamento via WhatsApp
@app.route("/enviar_orcamento")
def enviar_orcamento():
    cliente = request.args.get('cliente')
    arquivo_pdf = request.args.get('arquivo_pdf')
    enviar_via_whatsapp(cliente, f'C:/Users/guilherme.MCITRUS/Pictures/PI/{arquivo_pdf}')
    return render_template("/homepage.html")

# Colocar o site no ar
if __name__ == "__main__":
    # Abrir automaticamente o navegador com o endereço local
    webbrowser.open(url='http://127.0.0.1:5000', new=1, autoraise=True)    
    app.run()
