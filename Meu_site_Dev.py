from flask import Flask, render_template, request
from fpdf import FPDF
from datetime import datetime

#Pasta Template
app = Flask(__name__, template_folder="C:/Users/guilherme.MCITRUS/Documents/PI/PythonFlask/Meu Site/templates")

# Rota para a página de login
@app.route("/tela_login.html")
def login():
    return render_template("tela_login.html")

# Rota para a homepage
@app.route("/homepage.html")
def homepage():
    return render_template("homepage.html")


#Formatar data Gerado
def inserir_data_atual():
    # Obter a data atual
    data_atual = datetime.now().strftime('%d/%m/%Y')
    return data_atual
import locale
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
#Formatar hora
def formatar_carga_horaria(horas):
    horas_int = int(horas)
    minutos = int((horas - horas_int) * 60)
    return f'{horas_int}h {minutos}min'
import mariadb
# conectando ao banco
conexao = mariadb.connect(
    user="root",
    password="uni@2024",
    host="localhost",
    port=3306,
    database="banco2.0"
)
# Criando cursor
sql = conexao.cursor()
#sql.execute("create table clientes ( "+
#            "data_orcamento date, "+
#            "orcamento varchar(20), "+
#            "cliente varchar(55), "+
#            "telefone varchar(50), "+
#            "descricao_projeto varchar(55), "+
#            "carga_horária varchar(20), "+
#            "valor_hora varchar(40), "+
#            "valor_material varchar(40), "+
#            "prazo date, "+
#            "valor_final varchar(40))")
# Daqui para cima alterar conforme

data_orcamento = inserir_data_atual()
#orcamento = input('Insira número do orçamento: ')
cliente = input('Insira o nome do cliente: ')
endereco = input('Insira o endereço: ')
telefone = input('Insira o telefone: ')
descricao_projeto = input('Insira a descrição do projeto ')
carga_horária = float(input('Insira a quantidade estimada de horas: '))
valor_hora = float(input('Insira o valor da hora trabalhada: '))
valor_material = float(input('Insira o valor do material utilizado: '))
prazo = input('Insira o prazo de execução: ')
valor_final = valor_hora * carga_horária + valor_material
#print(projeto)
print(f'Valor do projeto: R${valor_final :.2f}')
carga_horaria_formatada = formatar_carga_horaria(carga_horária)
valor_final_formatado = locale.currency(valor_final, grouping=True)
#try:
sql.execute("insert into clientes (data_orcamento,orcamento,cliente,endereco,telefone,descricao_projeto,carga_horária,valor_hora,valor_material,prazo,valor_final) values (?,?,?,?,?,?,?,?,?,?,?)",(data_orcamento,None,cliente,endereco,telefone,descricao_projeto,carga_horária,valor_hora,valor_material,prazo,valor_final))
conexao.commit()

#Gerando número de orçamento em sequência com o banco
sql.execute("SELECT LAST_INSERT_ID()")
orcamento = sql.fetchone()[0]
print(f'O último número de orçamento inserido é: {orcamento}')
filename = f"Orçamento_{orcamento}.pdf"  # Include budget number in filename

#Gerando o PDF
pdf = FPDF()
pdf.add_font('Arial', '', 'C:/Windows/Fonts/arial.ttf', uni=True)
pdf.add_font
pdf.add_page()
pdf.set_font('Arial', 'B', 14)
pdf.image("C:/Users/guilherme.MCITRUS/Pictures/PI/orcamento.png", x = 0, y = 0)
pdf.set_text_color(255, 255, 255)
pdf.text(173, 13, str(orcamento))
pdf.text(173, 26, data_orcamento)
pdf.text(73, 146, cliente)
pdf.text(73, 160, endereco)
pdf.text(73, 174, telefone)
pdf.text(73, 188, descricao_projeto)
#pdf.text(95, 203, carga_horaria_formatada)
#pdf.text(95, 203, str(f'{carga_horária :.2f} Horas'))
pdf.text(95, 203, str(prazo))
pdf.text(95, 218, valor_final_formatado)
#pdf.text(95, 232, str(f'R$ {valor_final :.2f}'))
pdf.output(f'C:/Users/guilherme.MCITRUS/Pictures/PI/{filename}')
#pdf.output('C:/Users/guilherme.MCITRUS/Pictures/PI/Orçamento.pdf')
print(f'Orçamento gerado com sucesso! Nome do arquivo: {filename}')
#print('Orçamento gerado com sucesso!')
#return "Dados salvos com sucesso!"
#        except mariadb.Error as e:
#            print(f"Erro ao conectar ao MariaDB: {e}")
#            return "Erro ao salvar os dados"
    
# Rodar o aplicativo Flask
if __name__ == "__main__":
    app.run(debug=True)