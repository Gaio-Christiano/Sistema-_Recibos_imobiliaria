from reportlab.lib.pagesizes import letter  # Importa o tamanho da página carta
from reportlab.pdfgen import canvas  # Importa a classe canvas para criar o PDF
from num2words import num2words  # Importa a função num2words para converter números em texto

def gerar_recibo_pdf(nome, imovel, aluguel, condominio, agua, iptu, luz, seguro, taxa_incendio, luz_servico, total, data_emissao, mes_referencia, ano_referencia, data_vencimento, multa_aluguel, juros_aluguel, multa_contas, juros_contas, igpm, correcao_monetaria):
    """Função para gerar um recibo em PDF."""
    c = canvas.Canvas(f"recibo_{nome.replace(' ', '_')}_{data_emissao.split(' ')[0]}.pdf", pagesize=letter)  # Cria um novo arquivo PDF

    c.drawString(100, 750, "Recibo de Aluguel")  # Adiciona o título do recibo
    c.drawString(100, 730, f"Inquilino: {nome}")  # Adiciona o nome do inquilino
    c.drawString(100, 710, f"Imóvel: {imovel}")  # Adiciona o endereço do imóvel

    c.drawString(100, 690, f"Aluguel: R$ {aluguel:.2f}")  # Adiciona o valor do aluguel
    c.drawString(100, 670, f"Condomínio: R$ {condominio:.2f}")  # Adiciona o valor do condomínio
    c.drawString(100, 650, f"Água: R$ {agua:.2f}")  # Adiciona o valor da água
    c.drawString(100, 630, f"IPTU: R$ {iptu:.2f}")  # Adiciona o valor do IPTU
    c.drawString(100, 610, f"Luz: R$ {luz:.2f}")  # Adiciona o valor da luz
    c.drawString(100, 590, f"Seguro: R$ {seguro:.2f}")  # Adiciona o valor do seguro
    c.drawString(100, 570, f"Taxa de Incêndio: R$ {taxa_incendio:.2f}")  # Adiciona o valor da taxa de incêndio
    c.drawString(100, 550, f"Luz de Serviço: R$ {luz_servico:.2f}")  # Adiciona o valor da luz de serviço

    c.drawString(100, 530, f"Multa do Aluguel (10%): R$ {multa_aluguel:.2f}")  # Adiciona o valor da multa do aluguel
    c.drawString(100, 510, f"Juros do Aluguel (1%): R$ {juros_aluguel:.2f}")  # Adiciona o valor dos juros do aluguel
    c.drawString(100, 490, f"Multa das Contas (10%): R$ {multa_contas:.2f}")  # Adiciona o valor da multa das contas
    c.drawString(100, 470, f"Juros das Contas (1%): R$ {juros_contas:.2f}")  # Adiciona o valor dos juros das contas
    c.drawString(100, 450, f"Correção Monetária (IGPM {igpm:.2%}): R$ {correcao_monetaria:.2f}")  # Adiciona o valor da correção monetária e o índice do IGPM

    c.drawString(100, 430, f"Total: R$ {total:.2f} ({num2words(total, lang='pt-BR', to='currency')})")  # Adiciona o valor total do recibo e o escreve por extenso

    c.drawString(100, 410, f"Data de Emissão: {data_emissao}")  # Adiciona a data de emissão do recibo
    c.drawString(100, 390, f"Mês de Referência: {mes_referencia}")  # Adiciona o mês de referência
    c.drawString(100, 370, f"Ano de Referência: {ano_referencia}")  # Adiciona o ano de referência
    c.drawString(100, 350, f"Data de Vencimento: {data_vencimento}")  # Adiciona a data de vencimento

    c.save()  # Salva o arquivo PDF