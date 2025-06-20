import pdfplumber
import re
from datetime import datetime
from fpdf import FPDF
import gradio as gr
import zipfile

def extrair_texto_pdf(pdf):
    try:
        texto = ""
        with pdfplumber.open(pdf) as pdf_file:
            for pagina in pdf_file.pages:
                texto += pagina.extract_text() + "\n"
        return texto.strip()
    except Exception as e:
        return f"Erro ao ler o PDF: {str(e)}"

def converter_data_textual(texto_data):
    meses = {
        "janeiro": 1, "fevereiro": 2, "março": 3, "abril": 4,
        "maio": 5, "junho": 6, "julho": 7, "agosto": 8,
        "setembro": 9, "outubro": 10, "novembro": 11, "dezembro": 12
    }
    try:
        match = re.search(r'(\d{1,2}) de (\w+) de (\d{4})', texto_data.lower())
        if match:
            dia = int(match.group(1))
            mes = meses.get(match.group(2), 0)
            ano = int(match.group(3))
            if mes > 0:
                return datetime(ano, mes, dia).strftime('%d/%m/%Y')
        return None
    except:
        return None

def identificar_resultado(texto):
    texto = texto.lower()
    if "julgo procedente" in texto or "condeno" in texto:
        return "Favorável ao autor"
    elif "julgo improcedente" in texto or "extingo o processo" in texto or "indefiro" in texto:
        return "Desfavorável ao autor"
    else:
        return "Não identificado claramente"

def gerar_pdf(relatorio, nome_arquivo="relatorio_sentenca.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for linha in relatorio.split('\n'):
        pdf.cell(200, 10, txt=linha, ln=True, align='L')
    pdf.output(nome_arquivo)
    return nome_arquivo

def analisar_sentenca(pdf):
    texto = extrair_texto_pdf(pdf)
    if texto.startswith("Erro ao ler o PDF"):
        return texto, None

    # Juiz
    juiz = None
    for label in ['Juiz', 'Juíza', 'Relator']:
        match = re.search(rf'{label}:\s*(.*)', texto, re.IGNORECASE)
        if match:
            juiz = match.group(1).strip()
            break
    if not juiz:
        juiz = "Não encontrado"

    # Data
    data = None
    data_match = re.search(r'\b(\d{2}/\d{2}/\d{4})\b', texto)
    if data_match:
        data = data_match.group(1)
    else:
        data_textual_match = re.search(r'São Paulo, (.*?)[\.\n]', texto)
        if data_textual_match:
            data = converter_data_textual(data_textual_match.group(1))
    if not data:
        data = "Não encontrada"

    # Tipo de ação
    acao_match = re.search(r'Classe:\s*(.*)', texto)
    tipo_acao = acao_match.group(1).strip() if acao_match else "Não identificado"

    # Resultado
    resultado = identificar_resultado(texto)

    relatorio = (
        "----- RELATÓRIO DE ANÁLISE DA SENTENÇA -----\n\n"
        f"Nome do Juiz: {juiz}\n"
        f"Data da Decisão: {data}\n"
        f"Tipo da Ação: {tipo_acao}\n"
        f"Resultado da Ação: {resultado}\n\n"
        "--------------------------------------------"
    )

    # Arquivos individuais
    nome_txt = "relatorio_sentenca.txt"
    nome_pdf = "relatorio_sentenca.pdf"

    with open(nome_txt, "w", encoding="utf-8") as f:
        f.write(relatorio)
    gerar_pdf(relatorio, nome_pdf)

    # Criar .zip
    nome_zip = "relatorio_analise.zip"
    with zipfile.ZipFile(nome_zip, "w") as zipf:
        zipf.write(nome_txt)
        zipf.write(nome_pdf)

    return relatorio, nome_zip

interface = gr.Interface(
    fn=analisar_sentenca,
    inputs=gr.File(label="Enviar sentença (PDF)"),
    outputs=[
        gr.Textbox(label="Relatório"),
        gr.File(label="Download dos Arquivos (ZIP)")
    ],
    title="Analisador de Sentença Jurídica",
    description="Extraia automaticamente informações da sentença e baixe o relatório completo em PDF e TXT juntos em um único arquivo ZIP."
)

interface.launch()
