import sqlite3  # Importa a biblioteca SQLite para interagir com o banco de dados

def cadastrar_inquilino(nome, imovel, proprietario):
    """Função para cadastrar um inquilino no banco de dados."""
    conn = sqlite3.connect('imobiliaria.db')  # Conecta ao banco de dados SQLite
    cursor = conn.cursor()  # Cria um cursor para executar comandos SQL
    cursor.execute("INSERT INTO inquilinos (nome, imovel, proprietario) VALUES (?, ?, ?)", (nome, imovel, proprietario))  # Executa o comando SQL para inserir o inquilino
    conn.commit()  # Salva as alterações no banco de dados
    conn.close()  # Fecha a conexão com o banco de dados

def inserir_recibo(nome, imovel, aluguel, condominio, agua, iptu, luz, seguro, taxa_incendio, luz_servico, total, data, mes_referencia, ano_referencia, data_vencimento):
    """Função para inserir um recibo no banco de dados."""
    conn = sqlite3.connect('imobiliaria.db')  # Conecta ao banco de dados SQLite
    cursor = conn.cursor()  # Cria um cursor para executar comandos SQL
    cursor.execute("INSERT INTO recibos (nome, imovel, aluguel, condominio, agua, iptu, luz, seguro, taxa_incendio, luz_servico, total, data, mes_referencia, ano_referencia, data_vencimento) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (nome, imovel, aluguel, condominio, agua, iptu, luz, seguro, taxa_incendio, luz_servico, total, data, mes_referencia, ano_referencia, data_vencimento))  # Executa o comando SQL para inserir o recibo
    conn.commit()  # Salva as alterações no banco de dados
    conn.close()  # Fecha a conexão com o banco de dados

def listar_inquilinos():
    """Função para listar os inquilinos do banco de dados."""
    conn = sqlite3.connect('imobiliaria.db')  # Conecta ao banco de dados SQLite
    cursor = conn.cursor()  # Cria um cursor para executar comandos SQL
    cursor.execute("SELECT * FROM inquilinos")  # Executa o comando SQL para selecionar todos os inquilinos
    inquilinos = cursor.fetchall()  # Obtém todos os resultados da consulta
    conn.close()  # Fecha a conexão com o banco de dados
    return inquilinos  # Retorna a lista de inquilinos

def listar_recibos():
    """Função para listar os recibos do banco de dados."""
    conn = sqlite3.connect('imobiliaria.db')  # Conecta ao banco de dados SQLite
    cursor = conn.cursor()  # Cria um cursor para executar comandos SQL
    cursor.execute("SELECT * FROM recibos")  # Executa o comando SQL para selecionar todos os recibos
    recibos = cursor.fetchall()  # Obtém todos os resultados da consulta
    conn.close()  # Fecha a conexão com o banco de dados
    return recibos  # Retorna a lista de recibos

def obter_recibos_por_inquilino(nome_inquilino):
    """Função para obter os recibos de um inquilino."""
    conn = sqlite3.connect('imobiliaria.db')  # Conecta ao banco de dados SQLite
    cursor = conn.cursor()  # Cria um cursor para executar comandos SQL
    cursor.execute("SELECT * FROM recibos WHERE nome=?", (nome_inquilino,))  # Executa o comando SQL para selecionar os recibos do inquilino
    recibos = cursor.fetchall()  # Obtém todos os resultados da consulta
    conn.close()  # Fecha a conexão com o banco de dados
    return recibos  # Retorna a lista de recibos do inquilino

def obter_recibos_por_proprietario(nome_proprietario):
    """Função para obter os recibos de um proprietário."""
    conn = sqlite3.connect('imobiliaria.db')  # Conecta ao banco de dados SQLite
    cursor = conn.cursor()  # Cria um cursor para executar comandos SQL
    cursor.execute("SELECT * FROM recibos WHERE proprietario=?", (nome_proprietario,))  # Executa o comando SQL para selecionar os recibos do proprietário
    recibos = cursor.fetchall()  # Obtém todos os resultados da consulta
    conn.close()  # Fecha a conexão com o banco de dados
    return recibos  # Retorna a lista de recibos do proprietário