import sqlite3  # Importa a biblioteca SQLite para interagir com o banco de dados
import os  # Importa a biblioteca os para interagir com o sistema operacional (criar pastas, etc.)
from tkinter import Tk, Label, Entry, Button, messagebox  # Importa componentes do Tkinter para criar a interface gráfica
from fpdf import FPDF  # Importa a biblioteca fpdf para gerar arquivos PDF
from datetime import datetime  # Importa a classe datetime para trabalhar com datas e horas
from num2words import num2words  # Importa a função num2words para converter números em texto

# Função para converter valores numéricos em texto por extenso
def numero_por_extenso(valor):
    return num2words(valor, lang='pt_BR')  # Converte o valor numérico em texto usando a língua portuguesa

# Criar banco de dados
conn = sqlite3.connect("imobiliaria.db")  # Conecta ao banco de dados SQLite (cria se não existir)
c = conn.cursor()  # Cria um cursor para executar comandos SQL

# Criar tabelas caso não existam
c.execute('''CREATE TABLE IF NOT EXISTS inquilinos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    imovel TEXT NOT NULL,
                    proprietario TEXT NOT NULL
                )''')  # Cria a tabela 'inquilinos' se não existir

c.execute('''CREATE TABLE IF NOT EXISTS recibos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    imovel TEXT NOT NULL,
                    aluguel REAL NOT NULL,
                    condominio REAL NOT NULL,
                    agua REAL NOT NULL,
                    iptu REAL NOT NULL,
                    multa REAL NOT NULL,
                    juros REAL NOT NULL,
                    total REAL NOT NULL,
                    total_extenso TEXT NOT NULL,
                    data_emissao TEXT NOT NULL,
                    dias_atraso INTEGER NOT NULL
                )''')  # Cria a tabela 'recibos' se não existir
conn.commit()  # Salva as alterações no banco de dados

# Criar pasta para armazenar recibos
if not os.path.exists("recibos"):  # Verifica se a pasta 'recibos' existe
    os.makedirs("recibos")  # Cria a pasta 'recibos' se não existir

# Função para cadastrar inquilino
def cadastrar_inquilino():
    nome = entry_nome.get()  # Obtém o nome do inquilino do campo de entrada
    imovel = entry_imovel.get()  # Obtém o imóvel do campo de entrada
    proprietario = entry_proprietario.get()  # Obtém o proprietário do campo de entrada

    if nome and imovel and proprietario:  # Verifica se todos os campos estão preenchidos
        c.execute("INSERT INTO inquilinos (nome, imovel, proprietario) VALUES (?, ?, ?)",
                  (nome, imovel, proprietario))  # Insere os dados do inquilino na tabela
        conn.commit()  # Salva as alterações no banco de dados
        messagebox.showinfo("Sucesso", "Inquilino cadastrado com sucesso!")  # Exibe mensagem de sucesso
    else:
        messagebox.showwarning("Erro", "Preencha todos os campos")  # Exibe mensagem de erro

# Função para gerar recibo em PDF
def gerar_recibo():
    nome = entry_nome.get()  # Obtém o nome do inquilino do campo de entrada
    imovel = entry_imovel.get()  # Obtém o imóvel do campo de entrada
    aluguel = float(entry_aluguel.get())  # Obtém o valor do aluguel do campo de entrada
    condominio = float(entry_condominio.get())  # Obtém o valor do condomínio do campo de entrada
    agua = float(entry_agua.get())  # Obtém o valor da água do campo de entrada
    iptu = float(entry_iptu.get())  # Obtém o valor do IPTU do campo de entrada

    dias_atraso = 5  # Exemplo: 5 dias de atraso

    # Multa e juros do aluguel
    multa_aluguel = aluguel * 0.10  # Multa de 10%
    juros_aluguel = (aluguel * 0.01 / 30) * dias_atraso  # Mora de 1% ao mês proporcional

    # Multa e juros para contas
    multa_contas = (condominio + agua + iptu) * 0.02  # 2% de multa
    juros_contas = (condominio + agua + iptu) * (0.01 / 30) * dias_atraso  # 1% ao mês proporcional

    total = aluguel + condominio + agua + iptu + multa_aluguel + juros_aluguel + multa_contas + juros_contas
    total_extenso = numero_por_extenso(total)  # Converte o valor total em texto
    data_emissao = datetime.now().strftime("%d-%m-%Y %H:%M:%S")  # Obtém a data e hora atual

    # Salvar no banco de dados
    c.execute("INSERT INTO recibos (nome, imovel, aluguel, condominio, agua, iptu, multa, juros, total, total_extenso, data_emissao, dias_atraso) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
              (nome, imovel, aluguel, condominio, agua, iptu, multa_aluguel + multa_contas, juros_aluguel + juros_contas, total, total_extenso, data_emissao, dias_atraso))  # Insere os dados do recibo na tabela
    conn.commit()  # Salva as alterações no banco de dados

    # Gerar PDF
    pdf = FPDF()  # Cria um objeto PDF
    pdf.add_page()  # Adiciona uma página ao PDF
    pdf.set_font("Helvetica", size=12)  # Define a fonte e o tamanho do texto
    pdf.cell(200, 10, text="Recibo de Aluguel", new_x="LMARGIN", new_y="NEXT", align='C')  # Adiciona o título do recibo
    pdf.ln(10)  # Adiciona uma linha em branco
    pdf.cell(200, 10, text=f"Inquilino: {nome}", new_x="LMARGIN", new_y="NEXT")  # Adiciona o nome do inquilino
    pdf.cell(200, 10, text=f"Imóvel: {imovel}", new_x="LMARGIN", new_y="NEXT")  # Adiciona o imóvel
    pdf.cell(200, 10, text=f"Aluguel: R$ {aluguel:.2f}", new_x="LMARGIN", new_y="NEXT")  # Adiciona o valor do aluguel
    pdf.cell(200, 10, text=f"Condomínio: R$ {condominio:.2f}", new_x="LMARGIN", new_y="NEXT")  # Adiciona o valor do condomínio
    pdf.cell(200, 10, text=f"Água: R$ {agua:.2f}", new_x="LMARGIN", new_y="NEXT")  # Adiciona o valor da água
    pdf.cell(200, 10, text=f"IPTU: R$ {iptu:.2f}", new_x="LMARGIN", new_y="NEXT")  # Adiciona o valor do IPTU
    pdf.cell(200, 10, text=f"Multa: R$ {(multa_aluguel + multa_contas):.2f}", new_x="LMARGIN", new_y="NEXT")  # Adiciona o valor da multa
    pdf.cell(200, 10, text=f"Juros: R$ {(juros_aluguel + juros_contas):.2f}", new_x="LMARGIN", new_y="NEXT")  # Adiciona o valor dos juros
    pdf.cell(200, 10, text=f"Total: R$ {total:.2f}", new_x="LMARGIN", new_y="NEXT")  # Adiciona o valor total
    pdf.cell(200, 10, text=f"Total por extenso: {total_extenso}", new_x="LMARGIN", new_y="NEXT")  # Adiciona o valor total por extenso
    pdf.cell(200, 10, text=f"Data de Emissão: {data_emissao}", new_x="LMARGIN", new_y="NEXT")  # Adiciona a data de emissão
    pdf.cell(200, 10, text=f"Dias de atraso: {dias_atraso}", new_x="LMARGIN", new_y="NEXT")  # Adiciona a data de emissão

    # Definir nome do arquivo
    nome_arquivo = f"recibos/recibo_{nome}_{data_emissao.replace(':', '-').replace(' ', '_')}.pdf"  # Define o nome do arquivo PDF
    pdf.output(nome_arquivo)  # Salva o arquivo PDF

    messagebox.showinfo("Sucesso", f"Recibo gerado! Arquivo salvo em {nome_arquivo}")  # Exibe mensagem de sucesso

# Criar interface gráfica
root = Tk()  # Cria a janela principal da interface
root.title("Sistema Imobiliário")  # Define o título da janela

Label(root, text="Nome do Inquilino:").pack()  # Cria um rótulo para o nome do inquilino
entry_nome = Entry(root)  # Cria um campo de entrada para o nome do inquilino
entry_nome.pack()  # Adiciona o campo de entrada à janela

Label(root, text="Imóvel:").pack()  # Cria um rótulo para o imóvel
entry_imovel = Entry(root)  # Cria um campo de entrada para o imóvel
entry_imovel.pack()  # Adiciona o campo de entrada à janela

Label(root, text="Proprietário:").pack()  # Cria um rótulo para o proprietário
entry_proprietario = Entry(root)  # Cria um campo de entrada para o proprietário
entry_proprietario.pack()  # Adiciona o campo de entrada à janela

Label(root, text="Aluguel:").pack()  # Cria um rótulo para o aluguel
entry_aluguel = Entry(root)  # Cria um campo de entrada para o aluguel
entry_aluguel.pack()  # Adiciona o campo de entrada à janela

Label(root, text="Condomínio:").pack()  # Cria um rótulo para o condomínio
entry_condominio = Entry(root)  # Cria um campo de entrada para o condomínio
entry_condominio.pack()  # Adiciona o campo de entrada à janela

Label(root, text="Água:").pack()  # Cria um rótulo para a água
entry_agua = Entry(root)  # Cria um campo de entrada para a água
entry_agua.pack()  # Adiciona o campo de entrada à janela

Label(root, text="IPTU:").pack()  # Cria um rótulo para o IPTU
entry_iptu = Entry(root)  # Cria um campo de entrada para o IPTU
entry_iptu.pack()  # Adiciona o campo de entrada à janela

Button(root, text="Cadastrar Inquilino", command=cadastrar_inquilino).pack()  # Cria um botão para cadastrar inquilino
Button(root, text="Gerar Recibo", command=gerar_recibo).pack()  # Cria um botão para gerar recibo

root.mainloop()  # Inicia o loop principal da interface gráfica
