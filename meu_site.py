from flask import Flask, render_template, request, redirect, url_for
from fpdf import FPDF
import mariadb
import datetime
import locale
import webbrowser


#Configurando a localização para o Brasil
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

app = Flask(__name__)

#rota para logout
@app.route('/logout', methods=['POST'])
def logout():
    return redirect(url_for('login'))

#rota para login
@app.route("/")
def login():
    return render_template("tela_login.html")

#rota para homepage
@app.route("/homepage.html")
def homepage():
    return render_template("homepage.html")

#criando conexão com o banco
conexao = mariadb.connect(
    user="root",
    password="uni@2024",
    host="localhost",
    port=3306,
    database="banco2.0"
)
#Criando cursor
sql = conexao.cursor()

#rota e função para salvar no banco
@app.route("/salvar", methods=['GET', 'POST'])
def salvar_dados():
    if request.method =='POST':
        cliente = request.form['cliente']
        endereco = request.form['endereco']
        telefone = request.form['telefone']
        descricao_projeto = request.form['descricao']
        carga_horária = float (request.form['execucao'])
        valor_hora = float (request.form['hora'])
        valor_material = float (request.form['material'])
        prazo = request.form['entrega']  
        valor_final = carga_horária * valor_hora + valor_material
       
        data_orcamento = datetime.datetime.now().strftime('%d/%m/%Y')

        try:
            sql.execute("INSERT INTO clientes(data_orcamento, orcamento, cliente, endereco, telefone, descricao_projeto, carga_horária, valor_hora, valor_material, prazo, valor_final)values (?,?,?,?,?,?,?,?,?,?,?)", (data_orcamento,None,cliente,endereco,telefone,descricao_projeto,carga_horária,valor_hora,valor_material,prazo,valor_final))
            conexao.commit()

#Obtendo o número do último orçamento inserido
            sql.execute("SELECT LAST_INSERT_ID()")
            orcamento = sql.fetchone()[0]
            print(f'O último número de orçamento inserido é: {orcamento}')
            filename = f"Orçamento_{orcamento}.pdf" #Incluir número no orçamento

#Gerando o PDF

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
            print(f'Orçamento gerado com sucesso! Nome do arquivo: {filename}')
            return render_template("/homepage.html")
        except mariadb.Error as e:
            print(f"Erro ao salvar os dados: {e}")
            return "Erro ao salvar os dados"
        finally:
            sql.close()

    

#colocar o site no ar
if __name__ == "__main__":
#Abrir automaticamente o navegador com o endereço local
    webbrowser.open(url = 'http://127.0.0.1:5000', new=1, autoraise=True)    
    app.run(debug=True)

