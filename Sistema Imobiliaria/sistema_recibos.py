import sqlite3  # Importa a biblioteca SQLite3 para manipulação de bancos de dados
import os  # Importa a biblioteca OS para interações com o sistema operacional (caminhos de arquivos, etc.)
from tkinter import Tk, Label, Entry, Button, messagebox, Listbox, Scrollbar, END  # Importa componentes específicos da biblioteca Tkinter para criação da interface gráfica
from fpdf import FPDF  # Importa a classe FPDF da biblioteca fpdf para geração de arquivos PDF
from datetime import datetime  # Importa a classe datetime para trabalhar com datas e horas
from num2words import num2words  # Importa a função num2words para converter números em texto por extenso

# Função para converter valores numéricos em texto por extenso
def numero_por_extenso(valor):
    """
    Converte um valor numérico em sua representação textual em português do Brasil.

    Args:
        valor (int ou float): O valor numérico a ser convertido.

    Returns:
        str: A representação textual do valor.
    """
    return num2words(valor, lang='pt_BR')

# Criar banco de dados
db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "imobiliaria.db")  # Define o caminho do banco de dados no mesmo diretório do script
conn = sqlite3.connect(db_path)  # Estabelece conexão com o banco de dados (cria o arquivo se não existir)
c = conn.cursor()  # Cria um cursor para executar comandos SQL
print(f"Banco de dados criado em: {db_path}")  # Imprime o caminho do banco de dados criado

# Criar tabelas caso não existam
try:
    c.execute('''CREATE TABLE IF NOT EXISTS inquilinos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    cpf TEXT,
                    imovel TEXT NOT NULL,
                    proprietario TEXT NOT NULL,
                    comissao REAL DEFAULT 0.07
                )''')  # Cria a tabela inquilinos se não existir
    c.execute('''CREATE TABLE IF NOT EXISTS recibos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    imovel TEXT NOT NULL,
                    aluguel REAL NOT NULL,
                    condominio REAL NOT NULL,
                    agua REAL NOT NULL,
                    iptu REAL NOT NULL,
                    luz REAL NOT NULL,
                    taxa_incendio REAL NOT NULL,
                    seguro REAL NOT NULL,
                    multa_aluguel REAL NOT NULL,
                    juros_aluguel REAL NOT NULL,
                    multa_encargos REAL NOT NULL,
                    juros_encargos REAL NOT NULL,
                    total REAL NOT NULL,
                    total_extenso TEXT NOT NULL,
                    data_emissao TEXT NOT NULL,
                    dias_atraso INTEGER NOT NULL,
                    mes_referencia INTEGER NOT NULL,
                    ano_referencia INTEGER NOT NULL,
                    data_vencimento TEXT NOT NULL
                )''')  # Cria a tabela recibos se não existir
    c.execute('''CREATE TABLE IF NOT EXISTS prestacao_contas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    recibo_id INTEGER NOT NULL,
                    prestado_conta INTEGER NOT NULL DEFAULT 0,
                    FOREIGN KEY (recibo_id) REFERENCES recibos(id)
                )''')  # Cria a tabela prestacao_contas se não existir
    conn.commit()  # Salva as alterações no banco de dados
except sqlite3.Error as e:
    print(f"Erro ao criar tabelas: {e}")  # Imprime mensagem de erro se a criação das tabelas falhar

# Criar pasta para armazenar recibos
recibos_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "recibos")  # Define o caminho da pasta de recibos
if not os.path.exists(recibos_dir):  # Verifica se a pasta de recibos existe
    os.makedirs(recibos_dir)  # Cria a pasta de recibos se não existir

# Função para cadastrar inquilino
def cadastrar_inquilino():
    """
    Cadastra um novo inquilino no banco de dados.
    """
    nome = entry_nome.get()  # Obtém o nome do inquilino do campo de entrada
    cpf = entry_cpf.get()  # Obtém o CPF do inquilino do campo de entrada
    imovel = entry_imovel.get()  # Obtém o imóvel do inquilino do campo de entrada
    proprietario = entry_proprietario.get()  # Obtém o proprietário do inquilino do campo de entrada
    comissao_str = entry_comissao.get().replace(',', '.')  # Obtém a comissão do inquilino do campo de entrada e substitui vírgula por ponto
    comissao = float(comissao_str)  # Converte a comissão para float

    if nome and imovel and proprietario:  # Verifica se os campos obrigatórios estão preenchidos
        c.execute("INSERT INTO inquilinos (nome, cpf, imovel, proprietario, comissao) VALUES (?, ?, ?, ?, ?)",
                  (nome, cpf, imovel, proprietario, comissao))  # Insere os dados do inquilino na tabela
        conn.commit()  # Salva as alterações no banco de dados
        messagebox.showinfo("Sucesso", "Inquilino cadastrado com sucesso!")  # Exibe mensagem de sucesso
    else:
        messagebox.showwarning("Erro", "Preencha todos os campos")  # Exibe mensagem de erro se os campos obrigatórios não forem preenchidos

# Função para gerar recibo em PDF
def gerar_recibo():
    """
    Gera um recibo em PDF com os dados fornecidos.
    """
    nome = entry_nome.get()  # Obtém o nome do inquilino do campo de entrada
    imovel = entry_imovel.get()  # Obtém o imóvel do campo de entrada
    aluguel_str = entry_aluguel.get().replace(',', '.')  # Obtém o valor do aluguel do campo de entrada e substitui vírgula por ponto
    aluguel = float(aluguel_str)  # Converte o valor do aluguel para float
    condominio_str = entry_condominio.get().replace(',', '.')  # Obtém o valor do condomínio do campo de entrada e substitui vírgula por ponto
    condominio = float(condominio_str)  # Converte o valor do condomínio para float
    agua_str = entry_agua.get().replace(',', '.')  # Obtém o valor da água do campo de entrada e substitui vírgula por ponto
    agua = float(agua_str)  # Converte o valor da água para float
    iptu_str = entry_iptu.get().replace(',', '.')  # Obtém o valor do IPTU do campo de entrada e substitui vírgula por ponto
    iptu = float(iptu_str)  # Converte o valor do IPTU para float
    luz_str = entry_luz.get().replace(',', '.')  # Obtém o valor da luz do campo de entrada e substitui vírgula por ponto
    luz = float(luz_str)  # Converte o valor da luz para float
    taxa_incendio_str = entry_taxa_incendio.get().replace(',', '.')  # Obtém o valor da taxa de incêndio do campo de entrada e substitui vírgula por ponto
    taxa_incendio = float(taxa_incendio_str)  # Converte o valor da taxa de incêndio para float
    seguro_str = entry_seguro.get().replace(',', '.')  # Obtém o valor do seguro do campo de entrada e substitui vírgula por ponto
    seguro = float(seguro_str)  # Converte o valor do seguro para float
    try:
        mes_referencia = int(entry_mes_referencia.get())  # Obtém o mês de referência do campo de entrada e converte para inteiro
    except ValueError:
        messagebox.showerror("Erro", "Mês de Referência deve ser um número inteiro.")  # Exibe mensagem de erro se o mês não for um número inteiro
        return
    ano_referencia = int(entry_ano_referencia.get())  # Obtém o ano de referência do campo de entrada e converte para inteiro
    data_vencimento_str = entry_data_vencimento.get()  # Obtém a data de vencimento do campo de entrada

    # Calcular dias de atraso
    try:
        data_vencimento = datetime.strptime(data_vencimento_str, "%d/%m/%Y").date()  # Converte a data de vencimento para objeto date
    except ValueError:
        messagebox.showerror("Erro", "Data de vencimento deve estar no formato DD/MM/YYYY.")  # Exibe mensagem de erro se a data estiver em formato incorreto
        return
    data_atual = datetime.now().date()  # Obtém a data atual
    dias_atraso = (data_atual - data_vencimento).days if data_atual > data_vencimento else 0  # Calcula os dias de atraso

    # Multa e juros do aluguel
    multa_aluguel = aluguel * 0.10  # Multa de 10%
    juros_aluguel = (aluguel * 0.01 / 30) * dias_atraso  # Mora de 1% ao mês proporcional

    # Multa e juros para contas
    multa_encargos = (condominio + agua + iptu + luz + taxa_incendio + seguro) * 0.02  # 2% de multa
    juros_encargos = (condominio + agua + iptu + luz + taxa_incendio + seguro) * (0.01 / 30) * dias_atraso  # 1% ao mês proporcional

    total = aluguel + condominio + agua + iptu + luz + taxa_incendio + seguro + multa_aluguel + juros_aluguel + multa_encargos + juros_encargos  # Calcula o total do recibo
    total_extenso = numero_por_extenso(total)  # Converte o total para extenso
    data_emissao = datetime.now().strftime("%d-%m-%Y %H:%M:%S")  # Obtém a data e hora de emissão do recibo

    # Salvar no banco de dados
    c.execute("INSERT INTO recibos (nome, imovel, aluguel, condominio, agua, iptu, luz, taxa_incendio, seguro, multa_aluguel, juros_aluguel, multa_encargos, juros_encargos, total, total_extenso, data_emissao, dias_atraso, mes_referencia, ano_referencia, data_vencimento) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
              (nome, imovel, aluguel, condominio, agua, iptu, luz, taxa_incendio, seguro, multa_aluguel, juros_aluguel, multa_encargos, juros_encargos, total, total_extenso, data_emissao, dias_atraso, mes_referencia, ano_referencia, data_vencimento_str))  # Insere os dados do recibo na tabela
    recibo_id = c.lastrowid  # Obtém o ID do recibo inserido
    conn.commit()  # Salva as alterações no banco de dados

    # Salvar na tabela de prestação de contas
    c.execute("INSERT INTO prestacao_contas (recibo_id) VALUES (?)", (recibo_id,))  # Insere o ID do recibo na tabela de prestação de contas
    conn.commit()  # Salva as alterações no banco de dados

    # Gerar PDF
    pdf = FPDF()  # Cria um objeto PDF
    pdf.add_page()  # Adiciona uma página ao PDF
    pdf.set_font("Helvetica", size=12)  # Define a fonte do PDF
    pdf.cell(200, 10, text="Recibo de Aluguel", new_x="LMARGIN", new_y="NEXT", align='C')  # Adiciona o título do recibo ao PDF
    pdf.ln(10)  # Adiciona uma linha em branco
    pdf.cell(200, 10, text=f"Inquilino: {nome}", new_x="LMARGIN", new_y="NEXT")  # Adiciona o nome do inquilino ao PDF
    pdf.cell(200, 10, text=f"Imóvel: {imovel}", new_x="LMARGIN", new_y="NEXT")  # Adiciona o imóvel ao PDF
    pdf.cell(200, 10, text=f"Aluguel: R$ {aluguel:.2f}", new_x="LMARGIN", new_y="NEXT")  # Adiciona o valor do aluguel ao PDF
    pdf.cell(200, 10, text=f"Condomínio: R$ {condominio:.2f}", new_x="LMARGIN", new_y="NEXT")  # Adiciona o valor do condomínio ao PDF
    pdf.cell(200, 10, text=f"Água: R$ {agua:.2f}", new_x="LMARGIN", new_y="NEXT")  # Adiciona o valor da água ao PDF
    pdf.cell(200, 10, text=f"IPTU: R$ {iptu:.2f}", new_x="LMARGIN", new_y="NEXT")  # Adiciona o valor do IPTU ao PDF
    pdf.cell(200, 10, text=f"Luz: R$ {luz:.2f}", new_x="LMARGIN", new_y="NEXT")  # Adiciona o valor da luz ao PDF
    pdf.cell(200, 10, text=f"Taxa de Incêndio: R$ {taxa_incendio:.2f}", new_x="LMARGIN", new_y="NEXT")  # Adiciona o valor da taxa de incêndio ao PDF
    pdf.cell(200, 10, text=f"Seguro: R$ {seguro:.2f}", new_x="LMARGIN", new_y="NEXT")  # Adiciona o valor do seguro ao PDF
    pdf.cell(200, 10, text=f"Multa Aluguel: R$ {multa_aluguel:.2f}", new_x="LMARGIN", new_y="NEXT")  # Adiciona o valor da multa do aluguel ao PDF
    pdf.cell(200, 10, text=f"Juros Aluguel: R$ {juros_aluguel:.2f}", new_x="LMARGIN", new_y="NEXT")  # Adiciona o valor dos juros do aluguel ao PDF
    pdf.cell(200, 10, text=f"Multa Encargos: R$ {multa_encargos:.2f}", new_x="LMARGIN", new_y="NEXT")  # Adiciona o valor da multa dos encargos ao PDF
    pdf.cell(200, 10, text=f"Juros Encargos: R$ {juros_encargos:.2f}", new_x="LMARGIN", new_y="NEXT")  # Adiciona o valor dos juros dos encargos ao PDF
    pdf.cell(200, 10, text=f"Total: R$ {total:.2f}", new_x="LMARGIN", new_y="NEXT")  # Adiciona o valor total do recibo ao PDF
    pdf.cell(200, 10, text=f"Total por extenso: {total_extenso}", new_x="LMARGIN", new_y="NEXT")  # Adiciona o valor total por extenso ao PDF
    pdf.cell(200, 10, text=f"Data de Emissão: {data_emissao}", new_x="LMARGIN", new_y="NEXT")  # Adiciona a data de emissão ao PDF
    pdf.cell(200, 10, text=f"Dias de atraso: {dias_atraso}", new_x="LMARGIN", new_y="NEXT")  # Adiciona os dias de atraso ao PDF
    pdf.cell(200, 10, text=f"Mês de Referência: {mes_referencia}", new_x="LMARGIN", new_y="NEXT")  # Adiciona o mês de referência ao PDF
    pdf.cell(200, 10, text=f"Ano de Referência: {ano_referencia}", new_x="LMARGIN", new_y="NEXT")  # Adiciona o ano de referência ao PDF
    pdf.cell(200, 10, text=f"Data de Vencimento: {data_vencimento_str}", new_x="LMARGIN", new_y="NEXT")  # Adiciona a data de vencimento ao PDF

    # Definir nome do arquivo
    nome_arquivo = os.path.join(recibos_dir, f"recibo_{nome}_{data_emissao.replace(':', '-').replace(' ', '_')}.pdf")  # Define o nome do arquivo PDF
    pdf.output(nome_arquivo)  # Salva o arquivo PDF

    messagebox.showinfo("Sucesso", f"Recibo gerado! Arquivo salvo em {nome_arquivo}")  # Exibe mensagem de sucesso com o caminho do arquivo PDF

# Função para buscar inquilinos e preencher campos
def buscar_inquilinos():
    """
    Busca inquilinos no banco de dados e exibe os resultados na listbox.
    """
    termo_busca = entry_busca.get()  # Obtém o termo de busca do campo de entrada
    c.execute("SELECT * FROM inquilinos WHERE nome LIKE ? OR imovel LIKE ? OR proprietario LIKE ?",
              ('%' + termo_busca + '%', '%' + termo_busca + '%', '%' + termo_busca + '%'))  # Executa a busca no banco de dados
    resultados = c.fetchall()  # Obtém os resultados da busca
    listbox_resultados.delete(0, END)  # Limpa a listbox
    for resultado in resultados:
        listbox_resultados.insert(END, f"Nome: {resultado[1]}, Imóvel: {resultado[3]}, Proprietário: {resultado[4]}")  # Adiciona os resultados à listbox

def preencher_campos(event):
    """
    Preenche os campos de entrada com os dados do inquilino selecionado na listbox.
    """
    selecionado = listbox_resultados.curselection()  # Obtém o índice do item selecionado na listbox
    if selecionado:  # Verifica se algum item foi selecionado
        item = listbox_resultados.get(selecionado[0])  # Obtém o item selecionado
        nome = item.split(", ")[0].split(": ")[1]  # Extrai o nome do inquilino do item selecionado
        c.execute("SELECT * FROM inquilinos WHERE nome = ?", (nome,))  # Busca os dados do inquilino no banco de dados
        inquilino = c.fetchone()  # Obtém os dados do inquilino
        if inquilino:  # Verifica se o inquilino foi encontrado
            entry_nome.delete(0, END)  # Limpa o campo de entrada do nome
            entry_nome.insert(0, inquilino[1])  # Preenche o campo de entrada do nome com os dados do inquilino
            entry_cpf.delete(0, END)  # Limpa o campo de entrada do CPF
            entry_cpf.insert(0, inquilino[2])  # Preenche o campo de entrada do CPF com os dados do inquilino
            entry_imovel.delete(0, END)  # Limpa o campo de entrada do imóvel
            entry_imovel.insert(0, inquilino[3])  # Preenche o campo de entrada do imóvel com os dados do inquilino
            entry_proprietario.delete(0, END)  # Limpa o campo de entrada do proprietário
            entry_proprietario.insert(0, inquilino[4])  # Preenche o campo de entrada do proprietário com os dados do inquilino
            entry_comissao.delete(0, END)  # Limpa o campo de entrada da comissão
            entry_comissao.insert(0, inquilino[5])  # Preenche o campo de entrada da comissão com os dados do inquilino

# Função para prestação de contas
def prestacao_contas():
    """
    Realiza a prestação de contas de um recibo.
    """
    recibo_id_str = entry_recibo_id.get()  # Obtém o ID do recibo do campo de entrada
    if recibo_id_str:  # Verifica se o ID do recibo foi fornecido
        try:
            recibo_id = int(recibo_id_str)  # Converte o ID do recibo para inteiro
            c.execute("UPDATE prestacao_contas SET prestado_conta = 1 WHERE recibo_id = ?", (recibo_id,))  # Atualiza o status da prestação de contas
            conn.commit()  # Salva as alterações no banco de dados
            messagebox.showinfo("Sucesso", "Prestação de contas realizada!")  # Exibe mensagem de sucesso
        except ValueError:
            messagebox.showerror("Erro", "ID do recibo deve ser um número inteiro.")  # Exibe mensagem de erro se o ID não for um número inteiro
    else:
        messagebox.showerror("Erro", "Preencha o ID do recibo.")  # Exibe mensagem de erro se o ID não for fornecido

# Função para gerar balancete anual
def gerar_balancete():
    """
    Gera um balancete anual em PDF.
    """
    ano_str = entry_ano_balancete.get()  # Obtém o ano do balancete do campo de entrada
    if ano_str:  # Verifica se o ano foi fornecido
        try:
            ano = int(ano_str)  # Converte o ano para inteiro
            c.execute('''SELECT i.nome, i.cpf, r.mes_referencia, r.ano_referencia, r.total, i.comissao
                        FROM recibos r
                        JOIN inquilinos i ON r.nome = i.nome
                        WHERE r.ano_referencia = ?''', (ano,))  # Busca os dados dos recibos e inquilinos do ano especificado
            resultados = c.fetchall()  # Obtém os resultados da busca

            pdf = FPDF()  # Cria um objeto PDF
            pdf.add_page()  # Adiciona uma página ao PDF
            pdf.set_font("Helvetica", size=12)  # Define a fonte do PDF
            pdf.cell(0, 10, text=f"Balancete Anual - {ano}", ln=True)  # Adiciona o título do balancete ao PDF
            pdf.cell(40, 10, "Nome Inquilino")  # Adiciona o cabeçalho "Nome Inquilino"
            pdf.cell(30, 10, "CPF")  # Adiciona o cabeçalho "CPF"
            pdf.cell(30, 10, "Mês")  # Adiciona o cabeçalho "Mês"
            pdf.cell(30, 10, "Ano")  # Adiciona o cabeçalho "Ano"
            pdf.cell(30, 10, "Total Pago")  # Adiciona o cabeçalho "Total Pago"
            pdf.cell(30, 10, "Comissão")  # Adiciona o cabeçalho "Comissão"
            pdf.ln()  # Adiciona uma linha em branco

            total_comissao = 0  # Inicializa o total da comissão
            for resultado in resultados:
                comissao = resultado[4] * resultado[5]  # Calcula a comissão do inquilino
                pdf.cell(40, 10, resultado[0])  # Adiciona o nome do inquilino ao PDF
                pdf.cell(30, 10, resultado[1])  # Adiciona o CPF do inquilino ao PDF
                pdf.cell(30, 10, str(resultado[2]))  # Adiciona o mês do recibo ao PDF
                pdf.cell(30, 10, str(resultado[3]))  # Adiciona o ano do recibo ao PDF
                pdf.cell(30, 10, f"R$ {resultado[4]:.2f}")  # Adiciona o total pago ao PDF
                pdf.cell(30, 10, f"R$ {comissao:.2f}")  # Adiciona a comissão ao PDF
                pdf.ln()  # Adiciona uma linha em branco
                total_comissao += comissao  # Atualiza o total da comissão

            pdf.cell(0, 10, f"Total Comissão: R$ {total_comissao:.2f}", ln=True)  # Adiciona o total da comissão ao PDF
            nome_arquivo = f"balancete_{ano}.pdf"  # Define o nome do arquivo PDF
            pdf.output(nome_arquivo)  # Salva o arquivo PDF
            messagebox.showinfo("Sucesso", f"Balancete gerado! Arquivo salvo em {nome_arquivo}")  # Exibe mensagem de sucesso com o caminho do arquivo PDF
        except ValueError:
            messagebox.showerror("Erro", "Ano do balancete deve ser um número inteiro.")  # Exibe mensagem de erro se o ano não for um número inteiro
    else:
        messagebox.showerror("Erro", "Preencha o ano do balancete.")  # Exibe mensagem de erro se o ano não for fornecido

# Criar interface gráfica
root = Tk()  # Cria a janela principal
root.title("Sistema Imobiliário")  # Define o título da janela

# Campos de entrada
Label(root, text="Nome do Inquilino:").grid(row=0, column=0)  # Cria o rótulo "Nome do Inquilino"
entry_nome = Entry(root)  # Cria o campo de entrada para o nome do inquilino
entry_nome.grid(row=0, column=1)  # Posiciona o campo de entrada na grade

Label(root, text="CPF:").grid(row=1, column=0)  # Cria o rótulo "CPF"
entry_cpf = Entry(root)  # Cria o campo de entrada para o CPF
entry_cpf.grid(row=1, column=1)  # Posiciona o campo de entrada na grade

Label(root, text="Imóvel:").grid(row=2, column=0)  # Cria o rótulo "Imóvel"
entry_imovel = Entry(root)  # Cria o campo de entrada para o imóvel
entry_imovel.grid(row=2, column=1)  # Posiciona o campo de entrada na grade

Label(root, text="Proprietário:").grid(row=3, column=0)  # Cria o rótulo "Proprietário"
entry_proprietario = Entry(root)  # Cria o campo de entrada para o proprietário
entry_proprietario.grid(row=3, column=1)  # Posiciona o campo de entrada na grade

Label(root, text="Comissão (%):").grid(row=4, column=0)  # Cria o rótulo "Comissão (%)"
entry_comissao = Entry(root)  # Cria o campo de entrada para a comissão
entry_comissao.grid(row=4, column=1)  # Posiciona o campo de entrada na grade
entry_comissao.insert(0, "0.07")  # Define o valor padrão da comissão

Label(root, text="Aluguel:").grid(row=5, column=0)  # Cria o rótulo "Aluguel"
entry_aluguel = Entry(root)  # Cria o campo de entrada para o aluguel
entry_aluguel.grid(row=5, column=1)  # Posiciona o campo de entrada na grade

Label(root, text="Condomínio:").grid(row=6, column=0)  # Cria o rótulo "Condomínio"
entry_condominio = Entry(root)  # Cria o campo de entrada para o condomínio
entry_condominio.grid(row=6, column=1)  # Posiciona o campo de entrada na grade

Label(root, text="Água:").grid(row=7, column=0)  # Cria o rótulo "Água"
entry_agua = Entry(root)  # Cria o campo de entrada para a água
entry_agua.grid(row=7, column=1)  # Posiciona o campo de entrada na grade

Label(root, text="IPTU:").grid(row=8, column=0)  # Cria o rótulo "IPTU"
entry_iptu = Entry(root)  # Cria o campo de entrada para o IPTU
entry_iptu.grid(row=8, column=1)  # Posiciona o campo de entrada na grade

Label(root, text="Luz:").grid(row=9, column=0)  # Cria o rótulo "Luz"
entry_luz = Entry(root)  # Cria o campo de entrada para a luz
entry_luz.grid(row=9, column=1)  # Posiciona o campo de entrada na grade

Label(root, text="Taxa de Incêndio:").grid(row=10, column=0)  # Cria o rótulo "Taxa de Incêndio"
entry_taxa_incendio = Entry(root)  # Cria o campo de entrada para a taxa de incêndio
entry_taxa_incendio.grid(row=10, column=1)  # Posiciona o campo de entrada na grade

Label(root, text="Seguro:").grid(row=11, column=0)  # Cria o rótulo "Seguro"
entry_seguro = Entry(root)  # Cria o campo de entrada para o seguro
entry_seguro.grid(row=11, column=1)  # Posiciona o campo de entrada na grade

Label(root, text="Dias de Atraso:").grid(row=12, column=0)  # Cria o rótulo "Dias de Atraso"
entry_dias_atraso = Entry(root)  # Cria o campo de entrada para os dias de atraso
entry_dias_atraso.grid(row=12, column=1)  # Posiciona o campo de entrada na grade
entry_dias_atraso.insert(0, "0")  # Define o valor padrão dos dias de atraso

Label(root, text="Mês de Referência:").grid(row=13, column=0)  # Cria o rótulo "Mês de Referência"
entry_mes_referencia = Entry(root)  # Cria o campo de entrada para o mês de referência
entry_mes_referencia.grid(row=13, column=1)  # Posiciona o campo de entrada na grade

Label(root, text="Ano de Referência:").grid(row=14, column=0)  # Cria o rótulo "Ano de Referência"
entry_ano_referencia = Entry(root)  # Cria o campo de entrada para o ano de referência
entry_ano_referencia.grid(row=14, column=1)  # Posiciona o campo de entrada na grade

Label(root, text="Data de Vencimento:").grid(row=15, column=0)  # Cria o rótulo "Data de Vencimento"
entry_data_vencimento = Entry(root)  # Cria o campo de entrada para a data de vencimento
entry_data_vencimento.grid(row=15, column=1)  # Posiciona o campo de entrada na grade

Button(root, text="Cadastrar Inquilino", command=cadastrar_inquilino).grid(row=16, column=0, columnspan=2)  # Cria o botão "Cadastrar Inquilino"
Button(root, text="Gerar Recibo", command=gerar_recibo).grid(row=17, column=0, columnspan=2)  # Cria o botão "Gerar Recibo"

# Busca de inquilinos
Label(root, text="Buscar Inquilino:").grid(row=18, column=0)  # Cria o rótulo "Buscar Inquilino"
entry_busca = Entry(root)  # Cria o campo de entrada para a busca de inquilinos
entry_busca.grid(row=18, column=1)  # Posiciona o campo de entrada na grade
Button(root, text="Buscar", command=buscar_inquilinos).grid(row=19, column=0, columnspan=2)  # Cria o botão "Buscar"

scrollbar_resultados = Scrollbar(root)  # Cria a barra de rolagem para a listbox
scrollbar_resultados.grid(row=20, column=2, sticky='ns')  # Posiciona a barra de rolagem na grade

listbox_resultados = Listbox(root, yscrollcommand=scrollbar_resultados.set, width=50)  # Cria a listbox para exibir os resultados da busca
listbox_resultados.grid(row=20, column=0, columnspan=2)  # Posiciona a listbox na grade

scrollbar_resultados.config(command=listbox_resultados.yview)  # Configura a barra de rolagem para controlar a listbox

# Evento de clique na Listbox
listbox_resultados.bind("<Double-1>", preencher_campos)  # Associa a função preencher_campos ao evento de clique duplo na listbox

# Prestação de contas
Label(root, text="ID do Recibo:").grid(row=21, column=0)  # Cria o rótulo "ID do Recibo"
entry_recibo_id = Entry(root)  # Cria o campo de entrada para o ID do recib
