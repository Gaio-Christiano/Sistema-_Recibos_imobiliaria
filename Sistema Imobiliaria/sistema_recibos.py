import sqlite3  # Biblioteca para interagir com bancos de dados SQLite
import os  # Biblioteca para interagir com o sistema operacional (caminhos de arquivos, etc.)
from tkinter import Tk, Label, Entry, Button, messagebox, Listbox, Scrollbar, END, IntVar, Checkbutton  # Módulos do Tkinter para criar a interface gráfica
from fpdf import FPDF  # Biblioteca para gerar arquivos PDF
from datetime import datetime  # Biblioteca para trabalhar com datas e horas
from num2words import num2words  # Biblioteca para converter números em texto por extenso

# Função para converter valores numéricos em texto por extenso
def numero_por_extenso(valor):
    valor_int = int(valor)  # Obtém a parte inteira do valor
    valor_centavos = int((valor - valor_int) * 100)  # Obtém a parte decimal (centavos)
    extenso_reais = num2words(valor_int, lang='pt_BR')  # Converte a parte inteira para texto
    extenso_centavos = num2words(valor_centavos, lang='pt_BR')  # Converte os centavos para texto
    if valor_centavos > 0:  # Se houver centavos
        return f"{extenso_reais} Reais e {extenso_centavos} centavos"
    else:  # Se não houver centavos
        return f"{extenso_reais} Reais"

# Criar banco de dados
db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "imobiliaria.db")  # Define o caminho do banco de dados
conn = sqlite3.connect(db_path)  # Conecta ao banco de dados
c = conn.cursor()  # Cria um cursor para executar comandos SQL
print(f"Banco de dados criado em: {db_path}")

# Criar tabelas caso não existam
try:
    c.execute('''CREATE TABLE IF NOT EXISTS inquilinos (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nome TEXT NOT NULL,
                        cpf TEXT,
                        imovel TEXT NOT NULL,
                        proprietario TEXT NOT NULL,
                        comissao REAL DEFAULT 0.07,
                        data_inicio_contrato TEXT,
                        data_fim_contrato TEXT,
                        transferiu_luz INTEGER DEFAULT 0,
                        data_entrega_chaves TEXT
                    )''')  # Cria a tabela de inquilinos
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
                        data_vencimento TEXT NOT NULL,
                        parcela_iptu TEXT,
                        parcela_seguro TEXT,
                        parcela_taxa_incendio TEXT
                    )''')  # Cria a tabela de recibos
    c.execute('''CREATE TABLE IF NOT EXISTS prestacao_contas (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        recibo_id INTEGER NOT NULL,
                        prestado_conta INTEGER NOT NULL DEFAULT 0,
                        FOREIGN KEY (recibo_id) REFERENCES recibos(id)
                    )''')  # Cria a tabela de prestação de contas
    conn.commit()  # Salva as alterações no banco de dados
except sqlite3.Error as e:
    print(f"Erro ao criar tabelas: {e}")

# Criar pasta para armazenar recibos
recibos_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "recibos")  # Define o caminho da pasta de recibos
if not os.path.exists(recibos_dir):  # Se a pasta não existir
    os.makedirs(recibos_dir)  # Cria a pasta

# Função para cadastrar inquilino
def cadastrar_inquilino():
    nome = entry_nome.get()  # Obtém o nome do inquilino
    cpf = entry_cpf.get()  # Obtém o CPF do inquilino
    imovel = entry_imovel.get()  # Obtém o imóvel do inquilino
    proprietario = entry_proprietario.get()  # Obtém o proprietário do imóvel
    comissao_str = entry_comissao.get().replace(',', '.')  # Obtém a comissão do inquilino (e trata vírgula)
    comissao = float(comissao_str) / 100 if comissao_str else 0.07  # Calcula a comissão (ou usa 0.07 padrão)
    data_inicio_contrato = entry_data_inicio_contrato.get()  # Obtém a data de início do contrato
    data_fim_contrato = entry_data_fim_contrato.get()  # Obtém a data de fim do contrato
    transferiu_luz = var_transferiu_luz.get()  # Obtém o valor do checkbox de transferência de luz
    data_entrega_chaves = entry_data_entrega_chaves.get()  # Obtém a data de entrega das chaves

    if nome and imovel and proprietario:  # Se todos os campos obrigatórios estiverem preenchidos
        c.execute("INSERT INTO inquilinos (nome, cpf, imovel, proprietario, comissao, data_inicio_contrato, data_fim_contrato, transferiu_luz, data_entrega_chaves) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                  (nome, cpf, imovel, proprietario, comissao, data_inicio_contrato, data_fim_contrato, transferiu_luz, data_entrega_chaves))  # Insere o inquilino no banco de dados
        conn.commit()  # Salva as alterações no banco de dados
        messagebox.showinfo("Sucesso", "Inquilino cadastrado com sucesso!")  # Exibe mensagem de sucesso
    else:  # Se algum campo obrigatório estiver vazio
        messagebox.showwarning("Erro", "Preencha todos os campos")  # Exibe mensagem de erro

# Função para gerar recibo em PDF
def gerar_recibo():
    nome = entry_nome.get()  # Obtém o nome do inquilino
    imovel = entry_imovel.get()  # Obtém o imóvel do inquilino
    proprietario = entry_proprietario.get()  # Obtém o proprietário do imóvel
    aluguel = float(entry_aluguel.get().replace(',', '.')) if entry_aluguel.get() else 0  # Obtém o valor do aluguel (e trata vírgula)
    condominio = float(entry_condominio.get().replace(',', '.')) if entry_condominio.get() else 0  # Obtém o valor do condomínio (e trata vírgula)
    agua = float(entry_agua.get().replace(',', '.')) if entry_agua.get() else 0  # Obtém o valor da água (e trata vírgula)
    iptu = float(entry_iptu.get().replace(',', '.')) if entry_iptu.get() else 0  # Obtém o valor do IPTU (e trata vírgula)
    luz = float(entry_luz.get().replace(',', '.')) if entry_luz.get() else 0  # Obtém o valor da luz (e trata vírgula)
    taxa_incendio = float(entry_taxa_incendio.get().replace(',', '.')) if entry_taxa_incendio.get() else 0  # Obtém o valor da taxa de incêndio (e trata vírgula)
    seguro = float(entry_seguro.get().replace(',', '.')) if entry_seguro.get() else 0  # Obtém o valor do seguro (e trata vírgula)
    try:
        mes_referencia = int(entry_mes_referencia.get())  # Obtém o mês de referência
    except ValueError:
        messagebox.showerror("Erro", "Mês de Referência deve ser um número inteiro.")
        return
    ano_referencia = int(entry_ano_referencia.get())  # Obtém o ano de referência
    data_vencimento_str = entry_data_vencimento.get()  # Obtém a data de vencimento
    parcela_iptu = entry_parcela_iptu.get()  # Obtém a parcela do IPTU
    parcela_seguro = entry_parcela_seguro.get()  # Obtém a parcela do seguro
    parcela_taxa_incendio = entry_parcela_taxa_incendio.get()  # Obtém a parcela da taxa de incêndio

    # Calcular dias de atraso
    try:
        data_vencimento = datetime.strptime(data_vencimento_str, "%d/%m/%Y").date()  # Converte a data de vencimento para objeto datetime
    except ValueError:
        messagebox.showerror("Erro", "Data de vencimento deve estar no formato DD/MM/YYYY.")
        return
    data_atual = datetime.now().date()  # Obtém a data atual
    dias_atraso = (data_atual - data_vencimento).days if data_atual > data_vencimento else 0  # Calcula os dias de atraso

    # Multa e juros do aluguel
    multa_aluguel = aluguel * 0.10  # Calcula a multa do aluguel (10%)
    juros_aluguel = (aluguel * 0.01 / 30) * dias_atraso  # Calcula os juros do aluguel (1% ao mês proporcional)

    # Multa e juros para contas
    multa_encargos = (condominio + agua + iptu + luz + taxa_incendio + seguro) * 0.02  # Calcula a multa dos encargos (2%)
    juros_encargos = (condominio + agua + iptu + luz + taxa_incendio + seguro) * (0.01 / 30) * dias_atraso  # Calcula os juros dos encargos (1% ao mês proporcional)

    total_aluguel = aluguel + multa_aluguel + juros_aluguel  # Calcula o total do aluguel com multa e juros
    total_encargos = condominio + agua + iptu + luz + taxa_incendio + seguro + multa_encargos + juros_encargos  # Calcula o total dos encargos com multa e juros
    total = total_aluguel + total_encargos  # Calcula o total geral
    total_extenso = numero_por_extenso(total)  # Converte o total para texto por extenso
    data_emissao = datetime.now().strftime("%d-%m-%Y %H:%M:%S")  # Obtém a data e hora de emissão do recibo

    # Obter dados do inquilino
    c.execute('''SELECT data_inicio_contrato, data_fim_contrato, transferiu_luz, data_entrega_chaves
                    FROM inquilinos
                    WHERE nome = ?''', (nome,))  # Busca os dados do inquilino no banco de dados
    inquilino_info = c.fetchone()  # Obtém os dados do inquilino
    if inquilino_info:
        data_inicio_contrato = inquilino_info[0]  # Obtém a data de início do contrato
        data_fim_contrato = inquilino_info[1]  # Obtém a data de fim do contrato
        transferiu_luz = inquilino_info[2]  # Obtém o valor do checkbox de transferência de luz
        data_entrega_chaves = inquilino_info[3]  # Obtém a data de entrega das chaves
    else:
        data_inicio_contrato = "N/A"  # Se não encontrar o inquilino, define como "N/A"
        data_fim_contrato = "N/A"  # Se não encontrar o inquilino, define como "N/A"
        transferiu_luz = 0  # Se não encontrar o inquilino, define como 0
        data_entrega_chaves = "N/A"  # Se não encontrar o inquilino, define como "N/A"

    # Calcular próxima atualização do aluguel (exemplo: 12 meses após a entrega das chaves)
    if data_entrega_chaves != "N/A":  # Se houver data de entrega das chaves
        data_entrega = datetime.strptime(data_entrega_chaves, "%d/%m/%Y")  # Converte a data de entrega para objeto datetime
        proxima_atualizacao_aluguel = (data_entrega.replace(year=data_entrega.year + 1)).strftime("%d/%m/%Y")  # Calcula a próxima atualização (1 ano após a entrega)
    else:
        proxima_atualizacao_aluguel = "N/A"  # Se não houver data de entrega, define como "N/A"

    # Salvar no banco de dados
    c.execute("INSERT INTO recibos (nome, imovel, aluguel, condominio, agua, iptu, luz, taxa_incendio, seguro, multa_aluguel, juros_aluguel, multa_encargos, juros_encargos, total, total_extenso, data_emissao, dias_atraso, mes_referencia, ano_referencia, data_vencimento, parcela_iptu, parcela_seguro, parcela_taxa_incendio) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
              (nome, imovel, aluguel, condominio, agua, iptu, luz, taxa_incendio, seguro, multa_aluguel, juros_aluguel, multa_encargos, juros_encargos, total, total_extenso, data_emissao, dias_atraso, mes_referencia, ano_referencia, data_vencimento_str, parcela_iptu, parcela_seguro, parcela_taxa_incendio))  # Insere o recibo no banco de dados
    recibo_id = c.lastrowid  # Obtém o ID do último recibo inserido
    conn.commit()  # Salva as alterações no banco de dados

    # Salvar na tabela de prestação de contas
    c.execute("INSERT INTO prestacao_contas (recibo_id) VALUES (?)", (recibo_id,))  # Insere o recibo na tabela de prestação de contas
    conn.commit()  # Salva as alterações no banco de dados

    # Gerar PDF em duas colunas
    pdf = FPDF()  # Cria um objeto PDF
    pdf.add_page()  # Adiciona uma página ao PDF
    pdf.set_font("Helvetica", size=12)  # Define a fonte e o tamanho da fonte

    # Coluna 1 (Dados do recibo)
    pdf.cell(95, 10, text="Recibo de Aluguel", border=1)
    pdf.ln()
    pdf.cell(95, 10, text=f"Inquilino: {nome}", border=1)
    pdf.ln()
    pdf.cell(95, 10, text=f"Imóvel: {imovel}", border=1)
    pdf.ln()
    pdf.cell(95, 10, text=f"Proprietário: {proprietario}", border=1)
    pdf.ln()
    pdf.cell(95, 10, text="Aluguel", border=1)
    pdf.cell(95, 10, text="Encargos", border=1)
    pdf.ln()
    pdf.cell(95, 10, text=f"Aluguel: R$ {aluguel:.2f}", border=1)
    pdf.cell(95, 10, text=f"Condomínio: R$ {condominio:.2f}", border=1)
    pdf.ln()
    pdf.cell(95, 10, text=f"Multa de 10% do Aluguel: R$ {multa_aluguel:.2f}", border=1)
    pdf.cell(95, 10, text=f"Água: R$ {agua:.2f}", border=1)
    pdf.ln()
    pdf.cell(95, 10, text=f"Juros de mora de X% do Aluguel: R$ {juros_aluguel:.2f}", border=1)
    pdf.cell(95, 10, text=f"IPTU {parcela_iptu}: R$ {iptu:.2f}", border=1)
    pdf.ln()
    pdf.cell(95, 10, text="____________________________", border=1)
    pdf.cell(95, 10, text=f"Luz: R$ {luz:.2f}", border=1)
    pdf.ln()
    pdf.cell(95, 10, text=f"Semi total: R$ {total_aluguel:.2f}", border=1)
    pdf.cell(95, 10, text=f"Taxa de Incêndio {parcela_taxa_incendio}: R$ {taxa_incendio:.2f}", border=1)
    pdf.ln()
    pdf.cell(95, 10, text="", border=1)
    pdf.cell(95, 10, text=f"Seguro {parcela_seguro}: R$ {seguro:.2f}", border=1)
    pdf.ln()
    pdf.cell(95, 10, text="", border=1)
    pdf.cell(95, 10, text="______________________________", border=1)
    pdf.ln()
    pdf.cell(95, 10, text="", border=1)
    pdf.cell(95, 10, text=f"soma dos encargos: R$ {(condominio + agua + iptu + luz + taxa_incendio + seguro):.2f}", border=1)
    pdf.ln()
    pdf.cell(95, 10, text="", border=1)
    pdf.cell(95, 10, text=f"Multa de 2% dos Encargos: R$ {multa_encargos:.2f}", border=1)
    pdf.ln()
    pdf.cell(95, 10, text="", border=1)
    pdf.cell(95, 10, text=f"Juros de mora de X% dos Encargos: R$ {juros_encargos:.2f}", border=1)
    pdf.ln()
    pdf.cell(95, 10, text="", border=1)
    pdf.cell(95, 10, text="____________________________", border=1)
    pdf.ln()
    pdf.cell(95, 10, text="", border=1)
    pdf.cell(95, 10, text=f"Semi total: R$ {total_encargos:.2f}", border=1)
    pdf.ln()
    pdf.cell(95, 10, text=f"Calculo do valor devido com os encargos (se tiver multa e mora colocar essa frase \"Multa e juros de mora com {dias_atraso} meses de atraso\":", border=1)
    pdf.ln()
    pdf.cell(95, 10, text=f"referente ao aluguel devido R$ {total_aluguel:.2f} + referente aos encargos devido R$ {total_encargos:.2f}", border=1)
    pdf.ln()
    pdf.cell(95, 10, text=f"TOTAL A PAGAR R$ {total:.2f} ({total_extenso}).", border=1)
    pdf.ln()
    pdf.cell(95, 10, text=f"Mês e ano de referencia: {mes_referencia:02d}/{ano_referencia} com vencimento em {data_vencimento_str}", border=1)
    pdf.ln()
    pdf.cell(95, 10, text=f"Recibo emitido em: Rio de janeiro, {data_emissao}", border=1)
    pdf.ln()
    pdf.cell(95, 10, text=f"Próxima atualização do aluguel: {proxima_atualizacao_aluguel}", border=1)
    pdf.ln()
    pdf.cell(95, 10, text=f"Transferiu luz: {'Sim' if transferiu_luz else 'Não'}", border=1)
    pdf.ln()
    pdf.cell(95, 10, text=f"Data início contrato: {data_inicio_contrato}", border=1)
    pdf.ln()
    pdf.cell(95, 10, text=f"Data fim contrato: {data_fim_contrato}", border=1)
    pdf.ln()
    pdf.cell(95, 10, text=f"Data entrega das chaves: {data_entrega_chaves}", border=1)

    # Definir nome do arquivo
    nome_arquivo = os.path.join(recibos_dir, f"recibo_{nome}_{data_emissao.replace(':', '-').replace(' ', '_')}.pdf")  # Define o nome do arquivo PDF
    pdf.output(nome_arquivo)  # Salva o PDF

    messagebox.showinfo("Sucesso", f"Recibo gerado! Arquivo salvo em {nome_arquivo}")  # Exibe mensagem de sucesso

# Função para buscar inquilinos e preencher campos
def buscar_inquilinos():
    termo_busca = entry_busca.get()  # Obtém o termo de busca
    c.execute("SELECT * FROM inquilinos WHERE nome LIKE ? OR imovel LIKE ? OR proprietario LIKE ?",
              ('%' + termo_busca + '%', '%' + termo_busca + '%', '%' + termo_busca + '%'))  # Busca os inquilinos no banco de dados
    resultados = c.fetchall()  # Obtém os resultados da busca
    listbox_resultados.delete(0, END)  # Limpa a lista de resultados
    for resultado in resultados:  # Para cada resultado
        listbox_resultados.insert(END, f"Nome: {resultado[1]}, Imóvel: {resultado[3]}, Proprietário: {resultado[4]}")  # Adiciona o resultado à lista

def preencher_campos(event):
    selecionado = listbox_resultados.curselection()  # Obtém o item selecionado na lista
    if selecionado:  # Se algum item estiver selecionado
        item = listbox_resultados.get(selecionado[0])  # Obtém o texto do item selecionado
        nome = item.split(", ")[0].split(": ")[1]  # Obtém o nome do inquilino do texto do item
        c.execute('''SELECT r.*, i.data_inicio_contrato, i.data_fim_contrato, i.transferiu_luz, i.data_entrega_chaves
                        FROM recibos r
                        JOIN inquilinos i ON r.nome = i.nome
                        WHERE i.nome = ?
                        ORDER BY r.data_emissao DESC
                        LIMIT 1''', (nome,))  # Busca o último recibo do inquilino no banco de dados
        recibo = c.fetchone()  # Obtém os dados do recibo
        if recibo:  # Se encontrar o recibo
            entry_nome.delete(0, END)  # Limpa o campo de nome
            entry_nome.insert(0, recibo[1])  # Preenche o campo de nome com o nome do recibo
            entry_imovel.delete(0, END)  # Limpa o campo de imóvel
            entry_imovel.insert(0, recibo[2])  # Preenche o campo de imóvel com o imóvel do recibo
            entry_aluguel.delete(0, END)  # Limpa o campo de aluguel
            entry_aluguel.insert(0, recibo[3])  # Preenche o campo de aluguel com o aluguel do recibo
            entry_condominio.delete(0, END)  # Limpa o campo de condomínio
            entry_condominio.insert(0, recibo[4])  # Preenche o campo de condomínio com o condomínio do recibo
            entry_agua.delete(0, END)  # Limpa o campo de água
            entry_agua.insert(0, recibo[5])  # Preenche o campo de água com a água do recibo
            entry_iptu.delete(0, END)  # Limpa o campo de IPTU
            entry_iptu.insert(0, recibo[6])  # Preenche o campo de IPTU com o IPTU do recibo
            entry_luz.delete(0, END)  # Limpa o campo de luz
            entry_luz.insert(0, recibo[7])  # Preenche o campo de luz com a luz do recibo
            entry_taxa_incendio.delete(0, END)  # Limpa o campo de taxa de incêndio
            entry_taxa_incendio.insert(0, recibo[8])  # Preenche o campo de taxa de incêndio com a taxa de incêndio do recibo
            entry_seguro.delete(0, END)  # Limpa o campo de seguro
            entry_seguro.insert(0, recibo[9])  # Preenche o campo de seguro com o seguro do recibo
            entry_mes_referencia.delete(0, END)  # Limpa o campo de mês de referência
            entry_mes_referencia.insert(0, recibo[18])  # Preenche o campo de mês de referência com o mês de referência do recibo
            entry_ano_referencia.delete(0, END)  # Limpa o campo de ano de referência
            entry_ano_referencia.insert(0, recibo[19])  # Preenche o campo de ano de referência com o ano de referência do recibo
            entry_data_vencimento.delete(0, END)  # Limpa o campo de data de vencimento
            entry_data_vencimento.insert(0, recibo[20])  # Preenche o campo de data de vencimento com a data de vencimento do recibo
            entry_parcela_iptu.delete(0, END)  # Limpa o campo de parcela do IPTU
            entry_parcela_iptu.insert(0, recibo[21])  # Preenche o campo de parcela do IPTU com a parcela do IPTU do recibo
            entry_parcela_seguro.delete(0, END)  # Limpa o campo de parcela do seguro
            entry_parcela_seguro.insert(0, recibo[22])  # Preenche o campo de parcela do seguro com a parcela do seguro do recibo
            entry_parcela_taxa_incendio.delete(0, END)  # Limpa o campo de parcela da taxa de incêndio
            entry_parcela_taxa_incendio.insert(0, recibo[23])  # Preenche o campo de parcela da taxa de incêndio com a parcela da taxa de incêndio do recibo
            entry_data_inicio_contrato.delete(0, END)  # Limpa o campo de data de início do contrato
            entry_data_inicio_contrato.insert(0, recibo[24])  # Preenche o campo de data de início do contrato com a data de início do contrato do recibo
            entry_data_fim_contrato.delete(0, END)  # Limpa o campo de data de fim do contrato
            entry_data_fim_contrato.insert(0, recibo[25])  # Preenche o campo de data de fim do contrato com a data de fim do contrato do recibo
            var_transferiu_luz.set(recibo[26])  # Preenche o checkbox de transferência de luz com o valor do recibo
            entry_data_entrega_chaves.delete(0, END)  # Limpa o campo de data de entrega das chaves
            entry_data_entrega_chaves.insert(0, recibo[27])  # Preenche o campo de data de entrega das chaves com a data de entrega das chaves do recibo

# Função para prestação de contas
def prestacao_contas():
    recibo_id_str = entry_recibo_id.get()  # Obtém o ID do recibo
    if recibo_id_str:  # Se o ID do recibo for válido
        try:
            recibo_id = int(recibo_id_str)  # Converte o ID do recibo para inteiro
            c.execute("UPDATE prestacao_contas SET prestado_conta = 1 WHERE recibo_id = ?", (recibo_id,))  # Atualiza a prestação de contas no banco de dados
            conn.commit()  # Salva as alterações no banco de dados
            messagebox.showinfo("Sucesso", "Prestação de contas realizada!")  # Exibe mensagem de sucesso
        except ValueError:
            messagebox.showerror("Erro", "ID do recibo deve ser um número inteiro.")  # Exibe mensagem de erro
    else:
        messagebox.showerror("Erro", "Preencha o ID do recibo.")  # Exibe mensagem de erro

# Função para gerar balancete anual
def gerar_balancete():
    ano_str = entry_ano_balancete.get()  # Obtém o ano do balancete
    if ano_str:  # Se o ano do balancete for válido
        try:
            ano = int(ano_str)  # Converte o ano do balancete para inteiro
            c.execute('''SELECT i.nome, i.cpf, r.mes_referencia, r.ano_referencia, r.total, i.comissao
                            FROM recibos r
                            JOIN inquilinos i ON r.nome = i.nome
                            WHERE r.ano_referencia = ?''', (ano,))  # Busca os dados do balancete no banco de dados
            resultados = c.fetchall()  # Obtém os resultados da busca

            pdf = FPDF()  # Cria um objeto PDF
            pdf.add_page()  # Adiciona uma página ao PDF
            pdf.set_font("Helvetica", size=12)  # Define a fonte e o tamanho da fonte
            pdf.cell(0, 10, text=f"Balancete Anual - {ano}", ln=True)  # Adiciona o título do balancete ao PDF
            pdf.cell(40, 10, "Nome Inquilino")  # Adiciona o cabeçalho da coluna de nome
            pdf.cell(30, 10, "CPF")  # Adiciona o cabeçalho da coluna de CPF
            pdf.cell(30, 10, "Mês")  # Adiciona o cabeçalho da coluna de mês
            pdf.cell(30, 10, "Ano")  # Adiciona o cabeçalho da coluna de ano
            pdf.cell(30, 10, "Total Pago")  # Adiciona o cabeçalho da coluna de total pago
            pdf.cell(30, 10, "Comissão")  # Adiciona o cabeçalho da coluna de comissão
            pdf.ln()  # Adiciona uma nova linha

            total_comissao = 0  # Inicializa o total da comissão
            for resultado in resultados:  # Para cada resultado
                comissao = resultado[4] * resultado[5]  # Calcula a comissão
                pdf.cell(40, 10, resultado[0])  # Adiciona o nome do inquilino ao PDF
                pdf.cell(30, 10, resultado[1])  # Adiciona o CPF do inquilino ao PDF
                pdf.cell(30, 10, str(resultado[2]))  # Adiciona o mês ao PDF
                pdf.cell(30, 10, str(resultado[3]))  # Adiciona o ano ao PDF
                pdf.cell(30, 10, f"R$ {resultado[4]:.2f}")  # Adiciona o total pago ao PDF
                pdf.cell(30, 10, f"R$ {comissao:.2f}")  # Adiciona a comissão ao PDF
                pdf.ln()  # Adiciona uma nova linha
                total_comissao += comissao  # Soma a comissão ao total

            pdf.cell(0, 10, f"Total Comissão: R$ {total_comissao:.2f}", ln=True)  # Adiciona o total da comissão ao PDF
            nome_arquivo = f"balancete_{ano}.pdf"  # Define o nome do arquivo PDF
            pdf.output(nome_arquivo)  # Salva o PDF
            messagebox.showinfo("Sucesso", f"Balancete gerado! Arquivo salvo em {nome_arquivo}")  # Exibe mensagem de sucesso
        except ValueError:
            messagebox.showerror("Erro", "Ano do balancete deve ser um número inteiro.")  # Exibe mensagem de erro
    else:
        messagebox.showerror("Erro", "Preencha o ano do balancete.")  # Exibe mensagem de erro

# Criar interface gráfica
root = Tk()  # Cria a janela principal
root.title("Sistema Imobiliário")  # Define o título da janela

# Campos de entrada
Label(root, text="Nome do Inquilino:").grid(row=0, column=0)
entry_nome = Entry(root)
entry_nome.grid(row=0, column=1)

Label(root, text="CPF:").grid(row=1, column=0)
entry_cpf = Entry(root)
entry_cpf.grid(row=1, column=1)

Label(root, text="Imóvel:").grid(row=2, column=0)
entry_imovel = Entry(root)
entry_imovel.grid(row=2, column=1)

Label(root, text="Proprietário:").grid(row=3, column=0)
entry_proprietario = Entry(root)
entry_proprietario.grid(row=3, column=1)

Label(root, text="Comissão (%):").grid(row=4, column=0)
entry_comissao = Entry(root)
entry_comissao.grid(row=4, column=1)
entry_comissao.insert(0, "7") # Valor padrão de 7%

Label(root, text="Aluguel:").grid(row=5, column=0)
entry_aluguel = Entry(root)
entry_aluguel.grid(row=5, column=1)

Label(root, text="Condomínio:").grid(row=6, column=0)
entry_condominio = Entry(root)
entry_condominio.grid(row=6, column=1)

Label(root, text="Água:").grid(row=7, column=0)
entry_agua = Entry(root)
entry_agua.grid(row=7, column=1)

Label(root, text="IPTU:").grid(row=8, column=0)
entry_iptu = Entry(root)
entry_iptu.grid(row=8, column=1)

Label(root, text="Luz:").grid(row=9, column=0)
entry_luz = Entry(root)
entry_luz.grid(row=9, column=1)

Label(root, text="Taxa de Incêndio:").grid(row=10, column=0)
entry_taxa_incendio = Entry(root)
entry_taxa_incendio.grid(row=10, column=1)

Label(root, text="Seguro:").grid(row=11, column=0)
entry_seguro = Entry(root)
entry_seguro.grid(row=11, column=1)

Label(root, text="Mês de Referência:").grid(row=12, column=0)
entry_mes_referencia = Entry(root)
entry_mes_referencia.grid(row=12, column=1)

Label(root, text="Ano de Referência:").grid(row=13, column=0)
entry_ano_referencia = Entry(root)
entry_ano_referencia.grid(row=13, column=1)

Label(root, text="Data de Vencimento:").grid(row=14, column=0)
entry_data_vencimento = Entry(root)
entry_data_vencimento.grid(row=14, column=1)

Label(root, text="Parcela IPTU:").grid(row=15, column=0)
entry_parcela_iptu = Entry(root)
entry_parcela_iptu.grid(row=15, column=1)

Label(root, text="Parcela Seguro:").grid(row=16, column=0)
entry_parcela_seguro = Entry(root)
entry_parcela_seguro.grid(row=16, column=1)

Label(root, text="Parcela Taxa de Incêndio:").grid(row=17, column=0)
entry_parcela_taxa_incendio = Entry(root)
entry_parcela_taxa_incendio.grid(row=17, column=1)

Label(root, text="Data Entrega das Chaves:").grid(row=18, column=0)
entry_data_entrega_chaves = Entry(root)
entry_data_entrega_chaves.grid(row=18, column=1)

Label(root, text="Data Início Contrato:").grid(row=19, column=0)
entry_data_inicio_contrato = Entry(root)
entry_data_inicio_contrato.grid(row=19, column=1)

Label(root, text="Data Fim Contrato:").grid(row=20, column=0)
entry_data_fim_contrato = Entry(root)
entry_data_fim_contrato.grid(row=20, column=1)

var_transferiu_luz = IntVar()
Checkbutton(root, text="Transferiu Luz", variable=var_transferiu_luz).grid(row=21, column=0, columnspan=2)

Button(root, text="Cadastrar Inquilino", command=cadastrar_inquilino).grid(row=22, column=0, columnspan=2)
Button(root, text="Gerar Recibo", command=gerar_recibo).grid(row=23, column=0, columnspan=2)

# Busca de inquilinos
Label(root, text="Buscar Inquilino:").grid(row=24, column=0)
entry_busca = Entry(root)
entry_busca.grid(row=24, column=1)
Button(root, text="Buscar", command=buscar_inquilinos).grid(row=25, column=0, columnspan=2)

scrollbar_resultados = Scrollbar(root)
scrollbar_resultados.grid(row=26, column=2, sticky='ns')

listbox_resultados = Listbox(root, yscrollcommand=scrollbar_resultados.set, width=50)
listbox_resultados.grid(row=26, column=0, columnspan=2)

scrollbar_resultados.config(command=listbox_resultados.yview)

# Evento de clique na Listbox
listbox_resultados.bind("<Double-1>", preencher_campos)

# Prestação de contas
Label(root, text="ID do Recibo:").grid(row=27, column=0)
entry_recibo_id = Entry(root)
entry_recibo_id.grid(row=27, column=1)
Button(root, text="Prestação de Contas", command=prestacao_contas).grid(row=28, column=0, columnspan=2)

# Balancete anual
Label(root, text="Ano do Balancete:").grid(row=29, column=0)
entry_ano_balancete = Entry(root)
entry_ano_balancete.grid(row=29, column=1)
Button(root, text="Gerar Balancete Anual", command=gerar_balancete).grid(row=30, column=0, columnspan=2)

root.mainloop()  # Inicia o loop principal da interface gráfica
