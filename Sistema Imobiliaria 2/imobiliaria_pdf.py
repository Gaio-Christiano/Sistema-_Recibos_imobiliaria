from fpdf import FPDF  # Importa a classe FPDF para gerar arquivos PDF
import os  # Importa a biblioteca os para trabalhar com caminhos de arquivos
from datetime import datetime  # Importa a classe datetime para trabalhar com datas e horas
from num2words import num2words  # Importa a função num2words para converter números em texto

# Definir caminho do diretório atual
dir_path = os.path.dirname(os.path.abspath(__file__))  # Obtém o caminho absoluto do diretório do arquivo

# Criar pasta para armazenar recibos
recibo_dir = os.path.join(dir_path, "recibos")  # Cria o caminho para a pasta de recibos
if not os.path.exists(recibo_dir):  # Verifica se a pasta não existe
    os.makedirs(recibo_dir)  # Cria a pasta de recibos

def gerar_recibo_pdf(nome, imovel, aluguel, condominio, agua, iptu, luz, seguro, taxa_incendio, luz_servico, total, data_emissao, mes_referencia, ano_referencia, data_vencimento):
    pdf = FPDF()  # Cria um objeto FPDF
    pdf.add_page()  # Adiciona uma página ao PDF
    pdf.set_font("Helvetica", size=12)  # Define a fonte e o tamanho do texto
    pdf.cell(200, 10, text="Recibo de Aluguel", new_x="LMARGIN", new_y="NEXT", align='C')  # Adiciona o título do recibo
    pdf.ln(10)  # Adiciona uma linha em branco
    pdf.cell(200, 10, text=f"Inquilino: {nome}", new_x="LMARGIN", new_y="NEXT")  # Adiciona o nome do inquilino
    pdf.cell(200, 10, text=f"Imóvel: {imovel}", new_x="LMARGIN", new_y="NEXT")  # Adiciona o endereço do imóvel
    pdf.cell(200, 10, text=f"Aluguel: R$ {aluguel:.2f}", new_x="LMARGIN", new_y="NEXT")  # Adiciona o valor do aluguel
    pdf.cell(200, 10, text=f"Condomínio: R$ {condominio:.2f}", new_x="LMARGIN", new_y="NEXT")  # Adiciona o valor do condomínio
    pdf.cell(200, 10, text=f"Água: R$ {agua:.2f}", new_x="LMARGIN", new_y="NEXT")  # Adiciona o valor da água
    pdf.cell(200, 10, text=f"IPTU: R$ {iptu:.2f}", new_x="LMARGIN", new_y="NEXT")  # Adiciona o valor do IPTU
    pdf.cell(200, 10, text=f"Luz: R$ {luz:.2f}", new_x="LMARGIN", new_y="NEXT")  # Adiciona o valor da luz
    pdf.cell(200, 10, text=f"Seguro: R$ {seguro:.2f}", new_x="LMARGIN", new_y="NEXT")  # Adiciona o valor do seguro
    pdf.cell(200, 10, text=f"Taxa de Incêndio: R$ {taxa_incendio:.2f}", new_x="LMARGIN", new_y="NEXT")  # Adiciona o valor da taxa de incêndio
    pdf.cell(200, 10, text=f"Luz de Serviço: R$ {luz_servico:.2f}", new_x="LMARGIN", new_y="NEXT")  # Adiciona o valor da luz de serviço
    pdf.cell(200, 10, text=f"Total: R$ {total:.2f} ({num2words(total, lang='pt_BR').capitalize()})", new_x="LMARGIN", new_y="NEXT")  # Adiciona o valor total do recibo e o valor por extenso
    pdf.cell(200, 10, text=f"Data de Emissão: {data_emissao}", new_x="LMARGIN", new_y="NEXT")  # Adiciona a data de emissão do recibo
    pdf.cell(200, 10, text=f"Mês de Referência: {mes_referencia}", new_x="LMARGIN", new_y="NEXT") # Adiciona o mês de referência
    pdf.cell(200, 10, text=f"Ano de Referência: {ano_referencia}", new_x="LMARGIN", new_y="NEXT") # Adiciona o ano de referência
    pdf.cell(200, 10, text=f"Data de Vencimento: {data_vencimento}", new_x="LMARGIN", new_y="NEXT") # Adiciona a data de vencimento

    # Definir nome do arquivo com data e hora
    data_hora = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")  # Obtém a data e hora atual no formato especificado
    nome_arquivo = os.path.join(recibo_dir, f"recibo_{nome}_{data_hora}.pdf")  # Cria o nome do arquivo PDF
    pdf.output(nome_arquivo)  # Salva o arquivo PDF