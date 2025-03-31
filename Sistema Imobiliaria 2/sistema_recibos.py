import sqlite3
import os
from tkinter import Tk, Label, Entry, Button, messagebox
from fpdf import FPDF
from datetime import datetime
from num2words import num2words


# Definir caminho do diretório atual
dir_path = os.path.dirname(os.path.abspath(__file__))

# Criar banco de dados no diretório atual
db_path = os.path.join(dir_path, "imobiliaria.db")
conn = sqlite3.connect(db_path)
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS inquilinos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                imovel TEXT NOT NULL,
                proprietario TEXT NOT NULL
            )''')

c.execute('''CREATE TABLE IF NOT EXISTS recibos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                imovel TEXT NOT NULL,
                aluguel REAL NOT NULL,
                condominio REAL NOT NULL,
                agua REAL NOT NULL,
                iptu REAL NOT NULL,
                total REAL NOT NULL,
                data_emissao TEXT NOT NULL
            )''')
conn.commit()

# Criar pasta para armazenar recibos
recibo_dir = os.path.join(dir_path, "recibos")
if not os.path.exists(recibo_dir):
    os.makedirs(recibo_dir)

# Função para cadastrar inquilino
def cadastrar_inquilino():
    nome = entry_nome.get()
    imovel = entry_imovel.get()
    proprietario = entry_proprietario.get()
    
    if nome and imovel and proprietario:
        c.execute("INSERT INTO inquilinos (nome, imovel, proprietario) VALUES (?, ?, ?)",
                  (nome, imovel, proprietario))
        conn.commit()
        messagebox.showinfo("Sucesso", "Inquilino cadastrado com sucesso!")
    else:
        messagebox.showwarning("Erro", "Preencha todos os campos")

# Função para gerar recibo em PDF
def gerar_recibo():
    nome = entry_nome.get()
    imovel = entry_imovel.get()
    aluguel = float(entry_aluguel.get())
    condominio = float(entry_condominio.get())
    agua = float(entry_agua.get())
    iptu = float(entry_iptu.get())
    multa = aluguel * 0.10  # 10% de multa se houver atraso
    juros = aluguel * 0.01  # 1% de juros ao mês
    total = aluguel + condominio + agua + iptu + multa + juros
    valor_extenso = num2words(total, lang='pt_BR').capitalize()
    data_emissao = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    
    # Salvar no banco de dados
    c.execute("INSERT INTO recibos (nome, imovel, aluguel, condominio, agua, iptu, total, data_emissao) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
              (nome, imovel, aluguel, condominio, agua, iptu, total, data_emissao))
    conn.commit()
    
    # Gerar PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", size=12)
    pdf.cell(200, 10, text="Recibo de Aluguel", new_x="LMARGIN", new_y="NEXT", align='C')
    pdf.ln(10)
    pdf.cell(200, 10, text=f"Inquilino: {nome}", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(200, 10, text=f"Imóvel: {imovel}", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(200, 10, text=f"Aluguel: R$ {aluguel:.2f}", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(200, 10, text=f"Condomínio: R$ {condominio:.2f}", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(200, 10, text=f"Água: R$ {agua:.2f}", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(200, 10, text=f"IPTU: R$ {iptu:.2f}", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(200, 10, text=f"Multa: R$ {multa:.2f}", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(200, 10, text=f"Juros: R$ {juros:.2f}", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(200, 10, text=f"Total: R$ {total:.2f}", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(200, 10, text=f"Total: R$ {total:.2f} ({valor_extenso})", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(200, 10, text=f"Data de Emissão: {data_emissao}", new_x="LMARGIN", new_y="NEXT")
    
    # Definir nome do arquivo com data e hora
    data_hora = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
    nome_arquivo = os.path.join(recibo_dir, f"recibo_{nome}_{data_hora}.pdf")
    pdf.output(nome_arquivo)
    
    messagebox.showinfo("Sucesso", f"Recibo gerado! Arquivo salvo em {nome_arquivo}")

# Criar interface gráfica
root = Tk()
root.title("Sistema Imobiliário")

Label(root, text="Nome do Inquilino:").pack()
entry_nome = Entry(root)
entry_nome.pack()

Label(root, text="Imóvel:").pack()
entry_imovel = Entry(root)
entry_imovel.pack()

Label(root, text="Proprietário:").pack()
entry_proprietario = Entry(root)
entry_proprietario.pack()

Label(root, text="Aluguel:").pack()
entry_aluguel = Entry(root)
entry_aluguel.pack()

Label(root, text="Condomínio:").pack()
entry_condominio = Entry(root)
entry_condominio.pack()

Label(root, text="Água:").pack()
entry_agua = Entry(root)
entry_agua.pack()

Label(root, text="IPTU:").pack()
entry_iptu = Entry(root)
entry_iptu.pack()

Button(root, text="Cadastrar Inquilino", command=cadastrar_inquilino).pack()
Button(root, text="Gerar Recibo", command=gerar_recibo).pack()

root.mainloop()
