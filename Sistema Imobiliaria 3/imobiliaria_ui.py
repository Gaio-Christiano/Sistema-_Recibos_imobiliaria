import tkinter as tk  # Importa a biblioteca Tkinter para criar interfaces gráficas
from tkinter import messagebox, simpledialog, scrolledtext  # Importa módulos para mensagens, diálogos e texto com scroll
from imobiliaria_db import cadastrar_inquilino, inserir_recibo, listar_inquilinos, listar_recibos, obter_recibos_por_inquilino, obter_recibos_por_proprietario  # Importa funções do arquivo imobiliaria_db.py
from imobiliaria_pdf import gerar_recibo_pdf  # Importa a função para gerar recibos em PDF
from datetime import datetime, date  # Importa módulos para trabalhar com datas e horas
from num2words import num2words  # Importa a função para converter números em texto
import requests  # Importa a biblioteca para fazer requisições HTTP
import socket  # Importa a biblioteca para lidar com erros de conexão
import sqlite3 #Importa a biblioteca sqlite3

# Variáveis globais para os campos de entrada
entry_nome = None  # Inicializa o campo de entrada para o nome do inquilino
entry_imovel = None  # Inicializa o campo de entrada para o imóvel
entry_proprietario = None  # Inicializa o campo de entrada para o proprietário
entry_aluguel = None  # Inicializa o campo de entrada para o valor do aluguel
entry_condominio = None  # Inicializa o campo de entrada para o valor do condomínio
entry_agua = None  # Inicializa o campo de entrada para o valor da água
entry_iptu = None  # Inicializa o campo de entrada para o valor do IPTU
entry_luz = None  # Inicializa o campo de entrada para o valor da luz
entry_seguro = None  # Inicializa o campo de entrada para o valor do seguro
entry_taxa_incendio = None  # Inicializa o campo de entrada para o valor da taxa de incêndio
entry_luz_servico = None  # Inicializa o campo de entrada para o valor da luz de serviço
entry_mes_referencia = None  # Inicializa o campo de entrada para o mês de referência
entry_ano_referencia = None  # Inicializa o campo de entrada para o ano de referência
entry_data_vencimento = None  # Inicializa o campo de entrada para a data de vencimento

def cadastrar_inquilino_ui():
    """Função para cadastrar um inquilino na interface gráfica."""
    nome = entry_nome.get()  # Obtém o nome do inquilino do campo de entrada
    imovel = entry_imovel.get()  # Obtém o imóvel do campo de entrada
    proprietario = entry_proprietario.get()  # Obtém o proprietário do campo de entrada

    if nome and imovel and proprietario:  # Verifica se todos os campos estão preenchidos
        try:
            cadastrar_inquilino(nome, imovel, proprietario)  # Chama a função para cadastrar o inquilino no banco de dados
            messagebox.showinfo("Sucesso", "Inquilino cadastrado com sucesso!")  # Exibe uma mensagem de sucesso
        except sqlite3.IntegrityError:
            messagebox.showerror("Erro","Inquilino já cadastrado")
    else:
        messagebox.showwarning("Erro", "Preencha todos os campos")  # Exibe uma mensagem de aviso se algum campo estiver vazio

def buscar_inquilino_ui():
    """Função para buscar um inquilino na interface gráfica."""
    inquilinos = listar_inquilinos()  # Obtém a lista de inquilinos do banco de dados
    buscar_janela = tk.Toplevel(root)  # Cria uma nova janela (Toplevel) para exibir a lista de inquilinos
    buscar_janela.title("Buscar Inquilino")  # Define o título da janela

    def selecionar_inquilino(event):
        """Função para selecionar um inquilino da lista."""
        selecionado = lista_inquilinos.curselection()  # Obtém o índice do item selecionado na lista
        if selecionado:  # Verifica se algum item foi selecionado
            indice = selecionado[0]  # Obtém o índice do item selecionado
            inquilino = inquilinos[indice]  # Obtém os dados do inquilino selecionado
            entry_nome.delete(0, tk.END)  # Limpa o campo de entrada do nome
            entry_nome.insert(0, inquilino[1])  # Insere o nome do inquilino no campo de entrada
            entry_imovel.delete(0, tk.END)  # Limpa o campo de entrada do imóvel
            entry_imovel.insert(0, inquilino[2])  # Insere o imóvel do inquilino no campo de entrada
            entry_proprietario.delete(0, tk.END)  # Limpa o campo de entrada do proprietário
            entry_proprietario.insert(0, inquilino[3])  # Insere o proprietário do inquilino no campo de entrada
            buscar_janela.destroy()  # Fecha a janela de busca

    lista_inquilinos = tk.Listbox(buscar_janela)  # Cria uma lista para exibir os inquilinos
    for inquilino in inquilinos:  # Loop para percorrer a lista de inquilinos
        lista_inquilinos.insert(tk.END, f"{inquilino[1]} - {inquilino[2]}")  # Insere o nome e o imóvel do inquilino na lista
    lista_inquilinos.bind("<Double-Button-1>", selecionar_inquilino)  # Vincula o evento de duplo clique à função selecionar_inquilino
    lista_inquilinos.pack()  # Adiciona a lista à janela

def obter_igpm():
    """Função para obter o valor do IGPM da API do Banco Central ou do calculoexato."""
    try:
        url_bcb = "https://api.bcb.gov.br/dados/serie/12/dados/ultimos/1?formato=json"  # URL da API do Banco Central do Brasil
        response = requests.get(url_bcb)  # Faz a requisição HTTP para a API
        response.raise_for_status()  # Lança uma exceção para códigos de status de erro
        dados = response.json()  # Obtém os dados da resposta em formato JSON
        return float(dados[0]['valor']) / 100  # Retorna o valor do IGPM em formato decimal
    except requests.exceptions.RequestException as e:  # Captura exceções relacionadas a erros de requisição
        print(f"Erro ao obter IGPM da API do BCB: {e}")  # Imprime uma mensagem de erro
        try:
            url_calculoexato = "https://api.calculoexato.com.br/indices/igpm/valor" #Url da api do calculoexato
            response_calculoexato = requests.get(url_calculoexato) #faz a requisição http para a api do calculoexato
            response_calculoexato.raise_for_status() #lança exceção para códigos de status de erro
            dados_calculoexato = response_calculoexato.json() #obtem os dados da resposta em formato json
            return float(dados_calculoexato['valor']) /100 #retorna o valor do igpm em formato decimal
        except requests.exceptions.RequestException as e_calculoexato:
            print(f"Erro ao obter IGPM da API do calculoexato: {e_calculoexato}") #imprime a mensagem de erro da api calculoexato
            igpm_manual = simpledialog.askfloat("IGPM Manual", "Digite o valor do IGPM:")  # Abre uma janela para o usuário inserir o IGPM manualmente
            if igpm_manual is not None:  # Verifica se o usuário inseriu um valor
                return igpm_manual / 100  # Retorna o valor do IGPM inserido pelo usuário
            else:
                return 0.01  # Retorna 1% como valor padrão caso o usuário não insira um valor

def gerar_recibo_ui():
    """Função para gerar um recibo na interface gráfica."""
    nome = entry_nome.get()  # Obtém o nome do inquilino do campo de entrada
    imovel = entry_imovel.get()  # Obtém o imóvel do campo de entrada
    aluguel = float(entry_aluguel.get().replace(',', '.'))  # Obtém o valor do aluguel, substitui vírgula por ponto e converte para float
    condominio = float(entry_condominio.get().replace(',', '.'))  # Obtém o valor do condomínio, substitui vírgula por ponto e converte para float
    agua = float(entry_agua.get().replace(',', '.'))  # Obtém o valor da água, substitui vírgula por ponto e converte para float
    iptu = float(entry_iptu.get().replace(',', '.'))  # Obtém o valor do IPTU, substitui vírgula por ponto e converte para float
    luz = float(entry_luz.get().replace(',', '.'))  # Obtém o valor da luz, substitui vírgula por ponto e converte para float
    seguro = float(entry_seguro.get().replace(',', '.'))  # Obtém o valor do seguro, substitui vírgula por ponto e converte para float
    taxa_incendio = float(entry_taxa_incendio.get().replace(',', '.'))  # Obtém o valor da taxa de incêndio, substitui vírgula por ponto e converte para float
    luz_servico = float(entry_luz_servico.get().replace(',', '.'))  # Obtém o valor da luz de serviço, substitui vírgula por ponto e converte para float
    mes_referencia = entry_mes_referencia.get()  # Obtém o mês de referência do campo de entrada
    ano_referencia = entry_ano_referencia.get()  # Obtém o ano de referência do campo de entrada
    data_vencimento = entry_data_vencimento.get()  # Obtém a data de vencimento do campo de entrada

    multa_aluguel = aluguel * 0.10  # Calcula a multa de 10% sobre o aluguel
    juros_aluguel = aluguel * 0.01  # Calcula os juros de 1% sobre o aluguel
    total_aluguel = aluguel + multa_aluguel + juros_aluguel  # Calcula o total do aluguel com multa e juros

    multa_contas = (condominio + agua + iptu + luz + seguro + taxa_incendio + luz_servico) * 0.10  # Calcula a multa de 10% sobre as contas
    juros_contas = (condominio + agua + iptu + luz + seguro + taxa_incendio + luz_servico) * 0.01  # Calcula os juros de 1% sobre as contas
    total_contas = condominio + agua + iptu + luz + seguro + taxa_incendio + luz_servico + multa_contas + juros_contas  # Calcula o total das contas com multa e juros

    igpm = obter_igpm()  # Obtém o valor do IGPM
    correcao_monetaria = (total_aluguel + total_contas) * igpm  # Calcula a correção monetária
    total_recibo = total_aluguel + total_contas + correcao_monetaria  # Calcula o total do recibo com multa, juros e correção monetária

    data_emissao = datetime.now().strftime("%d-%m-%Y %H:%M:%S")  # Obtém a data e hora atual

    try:
        inserir_recibo(nome, imovel, aluguel, condominio, agua, iptu, luz, seguro, taxa_incendio, luz_servico, total_recibo, data_emissao, mes_referencia, ano_referencia, data_vencimento)  # Insere o recibo no banco de dados
        gerar_recibo_pdf(nome, imovel, aluguel, condominio, agua, iptu, luz, seguro, taxa_incendio, luz_servico, total_recibo, data_emissao, mes_referencia, ano_referencia, data_vencimento, multa_aluguel, juros_aluguel, multa_contas, juros_contas, igpm, correcao_monetaria)  # Gera o recibo em PDF
    except sqlite3.OperationalError as e: # Captura exceção caso ocorra erro ao inserir o recibo
        messagebox.showerror("Erro", f"Erro ao inserir recibo: {e}") # Exibe mensagem de erro

def listar_inquilinos_ui():
    """Função para listar os inquilinos na interface gráfica."""
    inquilinos = listar_inquilinos()  # Obtém a lista de inquilinos do banco de dados
    listar_janela = tk.Toplevel(root)  # Cria uma nova janela (Toplevel) para exibir a lista de inquilinos
    listar_janela.title("Lista de Inquilinos")  # Define o título da janela
    for inquilino in inquilinos:  # Loop para percorrer a lista de inquilinos
        tk.Label(listar_janela, text=f"Nome: {inquilino[1]}, Imóvel: {inquilino[2]}, Proprietário: {inquilino[3]}").pack()  # Cria um rótulo para cada inquilino e o adiciona à janela

def listar_recibos_ui():
    """Função para listar os recibos na interface gráfica."""
    recibos = listar_recibos()  # Obtém a lista de recibos do banco de dados
    listar_janela = tk.Toplevel(root)  # Cria uma nova janela (Toplevel) para exibir a lista de recibos
    listar_janela.title("Lista de Recibos")  # Define o título da janela
    for recibo in recibos:  # Loop para percorrer a lista de recibos
        try:
            tk.Label(listar_janela, text=f"Nome: {recibo[1]}, Imóvel: {recibo[2]}, Total: R$ {recibo[11]:.2f}, Data: {recibo[12]}").pack()  # Cria um rótulo para cada recibo e o adiciona à janela
        except IndexError:  # Captura exceção caso o índice esteja fora do intervalo
            print(f"Erro de índice para recibo: {recibo}")  # Imprime uma mensagem de erro

def gerar_prestacao_contas_ui():
    """Função para gerar a prestação de contas de um proprietário na interface gráfica."""
    nome_proprietario = simpledialog.askstring("Prestação de Contas", "Digite o nome do proprietário:")  # Solicita o nome do proprietário
    if nome_proprietario:  # Verifica se o nome do proprietário foi inserido
        recibos = obter_recibos_por_proprietario(nome_proprietario)  # Obtém os recibos do proprietário do banco de dados
        if recibos:  # Verifica se há recibos para o proprietário
            prestacao_contas_janela = tk.Toplevel(root)  # Cria uma nova janela (Toplevel) para exibir a prestação de contas
            prestacao_contas_janela.title("Prestação de Contas")  # Define o título da janela
            for recibo in recibos:  # Loop para percorrer os recibos do proprietário
                tk.Label(prestacao_contas_janela, text=f"Data: {recibo[12]}, Total: R$ {recibo[11]:.2f}, Imóvel: {recibo[2]}").pack()  # Cria um rótulo para cada recibo e o adiciona à janela
        else:
            messagebox.showinfo("Informação", "Nenhum recibo encontrado para este proprietário.")  # Exibe uma mensagem caso não haja recibos
    else:
        messagebox.showwarning("Aviso", "Nome do proprietário não informado.")  # Exibe uma mensagem caso o nome do proprietário não seja informado

def abrir_recibos_gerados_ui():
    """Função para abrir os recibos gerados."""
    # Implementar a função para abrir os recibos gerados.
    pass

def listar_imoveis_por_proprietario_ui():
    """Função para listar os imóveis de um proprietário."""
    # Implementar a função para listar os imóveis de um proprietário.
    pass

def listar_pagamentos_por_data_ui():
    """Função para listar os pagamentos por data."""
    # Implementar a função para listar os pagamentos por data.
    pass

root = tk.Tk()  # Cria a janela principal da interface gráfica
root.title("Sistema Imobiliário")  # Define o título da janela

# Campos de entrada
tk.Label(root, text="Nome do Inquilino:").pack()  # Cria um rótulo para o campo de nome e o adiciona à janela
entry_nome = tk.Entry(root)  # Cria um campo de entrada para o nome
entry_nome.pack()  # Adiciona o campo de entrada à janela

tk.Label(root, text="Imóvel:").pack()  # Cria um rótulo para o campo de imóvel e o adiciona à janela
entry_imovel = tk.Entry(root)  # Cria um campo de entrada para o imóvel
entry_imovel.pack()  # Adiciona o campo de entrada à janela

tk.Label(root, text="Proprietário:").pack()  # Cria um rótulo para o campo de proprietário e o adiciona à janela
entry_proprietario = tk.Entry(root)  # Cria um campo de entrada para o proprietário
entry_proprietario.pack()  # Adiciona o campo de entrada à janela

tk.Label(root, text="Aluguel:").pack()  # Cria um rótulo para o campo de aluguel e o adiciona à janela
entry_aluguel = tk.Entry(root)  # Cria um campo de entrada para o aluguel
entry_aluguel.pack()  # Adiciona o campo de entrada à janela

tk.Label(root, text="Condomínio:").pack()  # Cria um rótulo para o campo de condomínio e o adiciona à janela
entry_condominio = tk.Entry(root)  # Cria um campo de entrada para o condomínio
entry_condominio.pack()  # Adiciona o campo de entrada à janela

tk.Label(root, text="Água:").pack()  # Cria um rótulo para o campo de água e o adiciona à janela
entry_agua = tk.Entry(root)  # Cria um campo de entrada para a água
entry_agua.pack()  # Adiciona o campo de entrada à janela

tk.Label(root, text="IPTU:").pack()  # Cria um rótulo para o campo de IPTU e o adiciona à janela
entry_iptu = tk.Entry(root)  # Cria um campo de entrada para o IPTU
entry_iptu.pack()  # Adiciona o campo de entrada à janela

tk.Label(root, text="Luz:").pack()  # Cria um rótulo para o campo de luz e o adiciona à janela
entry_luz = tk.Entry(root)  # Cria um campo de entrada para a luz
entry_luz.pack()  # Adiciona o campo de entrada à janela

tk.Label(root, text="Seguro:").pack()  # Cria um rótulo para o campo de seguro e o adiciona à janela
entry_seguro = tk.Entry(root)  # Cria um campo de entrada para o seguro
entry_seguro.pack()  # Adiciona o campo de entrada à janela

tk.Label(root, text="Taxa de Incêndio:").pack()  # Cria um rótulo para o campo de taxa de incêndio e o adiciona à janela
entry_taxa_incendio = tk.Entry(root)  # Cria um campo de entrada para a taxa de incêndio
entry_taxa_incendio.pack()  # Adiciona o campo de entrada à janela

tk.Label(root, text="Luz de Serviço:").pack()  # Cria um rótulo para o campo de luz de serviço e o adiciona à janela
entry_luz_servico = tk.Entry(root)  # Cria um campo de entrada para a luz de serviço
entry_luz_servico.pack()  # Adiciona o campo de entrada à janela

tk.Label(root, text="Mês de Referência:").pack()  # Cria um rótulo para o campo de mês de referência e o adiciona à janela
entry_mes_referencia = tk.Entry(root)  # Cria um campo de entrada para o mês de referência
entry_mes_referencia.pack()  # Adiciona o campo de entrada à janela

tk.Label(root, text="Ano de Referência:").pack()  # Cria um rótulo para o campo de ano de referência e o adiciona à janela
entry_ano_referencia = tk.Entry(root)  # Cria um campo de entrada para o ano de referência
entry_ano_referencia.pack()  # Adiciona o campo de entrada à janela

tk.Label(root, text="Data de Vencimento:").pack()  # Cria um rótulo para o campo de data de vencimento e o adiciona à janela
entry_data_vencimento = tk.Entry(root)  # Cria um campo de entrada para a data de vencimento
entry_data_vencimento.pack()  # Adiciona o campo de entrada à janela

# Botões
tk.Button(root, text="Cadastrar Inquilino", command=cadastrar_inquilino_ui).pack()  # Cria um botão para cadastrar inquilino
tk.Button(root, text="Buscar Inquilino", command=buscar_inquilino_ui).pack()  # Cria um botão para buscar inquilino
tk.Button(root, text="Gerar Recibo", command=gerar_recibo_ui).pack()  # Cria um botão para gerar recibo
tk.Button(root, text="Listar Inquilinos", command=listar_inquilinos_ui).pack()  # Cria um botão para listar inquilinos
tk.Button(root, text="Listar Recibos", command=listar_recibos_ui).pack()  # Cria um botão para listar recibos
tk.Button(root, text="Gerar Prestação de Contas", command=gerar_prestacao_contas_ui).pack()  # Cria um botão para gerar prestação de contas
tk.Button(root, text="Abrir Recibos Gerados", command=abrir_recibos_gerados_ui).pack()  # Cria um botão para abrir recibos gerados
tk.Button(root, text="Listar Imóveis por Proprietário", command=listar_imoveis_por_proprietario_ui).pack()  # Cria um botão para listar imóveis por proprietário
tk.Button(root, text="Listar Pagamentos por Data", command=listar_pagamentos_por_data_ui).pack()  # Cria um botão para listar pagamentos por data

root.mainloop()  # Inicia o loop principal da interface gráfica