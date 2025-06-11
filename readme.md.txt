# Analisador de Sentenças Judiciais em Python

Este projeto é uma aplicação simples desenvolvida em Python para ajudar profissionais do direito a automatizar a análise de sentenças judiciais em PDF.

## O que o sistema faz

- Lê sentenças em arquivos PDF
- Identifica o nome do juiz, a data da decisão e o tipo de ação judicial
- Informa se a decisão foi favorável ou não ao autor
- Gera relatórios nos formatos PDF e TXT para facilitar o armazenamento e a consulta

## Por que usar?

Analisar centenas de sentenças manuais pode consumir muito tempo e estar sujeito a erros. Com esta ferramenta, você pode acelerar esse processo e garantir maior precisão na extração das informações importantes.

## Como usar

1. Faça o upload do arquivo PDF da sentença
2. O sistema processa o documento e extrai as informações relevantes
3. Você pode visualizar o relatório gerado na tela
4. Opção para baixar o relatório em PDF ou TXT para armazenar e consultar posteriormente

## Tecnologias usadas

- Python
- pdfplumber (para leitura de PDFs)
- fpdf (para geração de PDFs)
- Gradio (interface web simples para facilitar o uso)

## Como executar

1. Clone este repositório
2. Instale as dependências:
   ```bash
   pip install pdfplumber fpdf gradio