import sqlite3  # Importa a biblioteca sqlite3 para trabalhar com o banco de dados SQLite
import os  # Importa a biblioteca os para trabalhar com caminhos de arquivos

# Definir caminho do diretório atual
dir_path = os.path.dirname(os.path.abspath(__file__))  # Obtém o caminho absoluto do diretório do arquivo

# Criar banco de dados no diretório atual
db_path = os.path.join(dir_path, "imobiliaria.db")  # Cria o caminho para o arquivo do banco de dados
conn = sqlite3.connect(db_path)  # Conecta ao banco de dados SQLite
c = conn.cursor()  # Cria um cursor para executar comandos SQL

def criar_tabelas():
    c.execute('''CREATE TABLE IF NOT EXISTS inquilinos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    imovel TEXT NOT NULL,
                    proprietario TEXT NOT NULL
                )''')  # Cria a tabela inquilinos se ela não existir

    c.execute('''CREATE TABLE IF NOT EXISTS recibos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    imovel TEXT NOT NULL,
                    aluguel REAL NOT NULL,
                    condominio REAL NOT NULL,
                    agua REAL NOT NULL,
                    iptu REAL NOT NULL,
                    luz REAL NOT NULL,
                    seguro REAL NOT NULL,
                    taxa_incendio REAL NOT NULL,
                    luz_servico REAL NOT NULL,
                    total REAL NOT NULL,
                    data_emissao TEXT NOT NULL,
                    mes_referencia TEXT NOT NULL,
                    ano_referencia TEXT NOT NULL,
                    data_vencimento TEXT NOT NULL
                )''') # Cria a tabela recibos se ela não existir
    conn.commit()  # Salva as alterações no banco de dados

def cadastrar_inquilino(nome, imovel, proprietario):
    c.execute("INSERT INTO inquilinos (nome, imovel, proprietario) VALUES (?, ?, ?)",
              (nome, imovel, proprietario))  # Insere um novo inquilino na tabela
    conn.commit()  # Salva as alterações no banco de dados

def inserir_recibo(nome, imovel, aluguel, condominio, agua, iptu, luz, seguro, taxa_incendio, luz_servico, total, data_emissao, mes_referencia, ano_referencia, data_vencimento):
    c.execute("INSERT INTO recibos (nome, imovel, aluguel, condominio, agua, iptu, luz, seguro, taxa_incendio, luz_servico, total, data_emissao, mes_referencia, ano_referencia, data_vencimento) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
              (nome, imovel, aluguel, condominio, agua, iptu, luz, seguro, taxa_incendio, luz_servico, total, data_emissao, mes_referencia, ano_referencia, data_vencimento))  # Insere um novo recibo na tabela
    conn.commit()  # Salva as alterações no banco de dados

def listar_inquilinos():
    c.execute("SELECT * FROM inquilinos")  # Seleciona todos os inquilinos da tabela
    return c.fetchall()  # Retorna todos os resultados da consulta

def listar_recibos():
    c.execute("SELECT * FROM recibos")  # Seleciona todos os recibos da tabela
    return c.fetchall()  # Retorna todos os resultados da consulta

def obter_comissao(proprietario):
    comissoes = {"X": 0.07, "Y": 0.08, "Z": 0.10}  # Define as comissões para cada proprietário
    return comissoes.get(proprietario, 0.07)  # Retorna a comissão do proprietário ou 0.07 se não encontrado

def obter_recibos_por_inquilino(nome_inquilino):
    c.execute("SELECT * FROM recibos WHERE nome = ?", (nome_inquilino,))  # Seleciona os recibos do inquilino especificado
    return c.fetchall()  # Retorna todos os resultados da consulta

def obter_inquilinos_por_proprietario(nome_proprietario):
    c.execute("SELECT * FROM inquilinos WHERE proprietario = ?", (nome_proprietario,))  # Seleciona os inquilinos do proprietário especificado
    return c.fetchall()  # Retorna todos os resultados da consulta

def obter_recibos_por_proprietario(nome_proprietario):
    inquilinos = obter_inquilinos_por_proprietario(nome_proprietario)  # Obtém os inquilinos do proprietário
    recibos = []  # Inicializa a lista de recibos
    for inquilino in inquilinos:  # Loop para percorrer os inquilinos
        recibos.extend(obter_recibos_por_inquilino(inquilino[1]))  # Adiciona os recibos do inquilino à lista
    return recibos  # Retorna a lista de recibos

def obter_recibos_por_mes(mes, ano):
    c.execute("SELECT * FROM recibos WHERE strftime('%m', data_emissao) = ? AND strftime('%Y', data_emissao) = ?", (mes, ano))  # Seleciona os recibos do mês e ano especificados
    return c.fetchall()  # Retorna todos os resultados da consulta

criar_tabelas()  # Chama a função para criar as tabelas do banco de dados