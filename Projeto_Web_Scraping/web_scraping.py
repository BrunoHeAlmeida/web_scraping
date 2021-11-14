from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import time
import re

# usuario e pagina para obter html
pagina = 'https://casadosdados.com.br/solucao/cnpj/'
usuario = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36'}
dados_clientes = []
lista_CNPJ = []

# Processo de automação para coleta dos dados
def web_scraping(lista_CNPJ):
    for item in lista_CNPJ:
      url = pagina + item
      req = Request(url, headers=usuario)
      html = urlopen(req)
      soup = BeautifulSoup(html, 'html.parser')
      
      # list comprehension do conteúdo do html
      lista  = [item.getText() for item in soup.findAll('p', {'data-v-0adacb42': ''})]
      lista2 = [item.getText() for item in soup.findAll('a', {'data-v-0adacb42': ''}, href = True)]

      # filtrando os campos dos dados e manipulando os dados
      cnpj = lista[lista.index('CNPJ')+1]
      p = re.compile(r'\d')
      cnpj = p.findall(cnpj)
      cnpj = "".join(cnpj)

      razao = lista[lista.index('Razão Social')+1]
      if(razao == []):
        razao = 'NONE'

      if('Nome Fantasia' in lista):
        fantasia = lista[lista.index('Nome Fantasia')+1]
      else:
        fantasia = 'NONE'

      tipo = lista[lista.index('Tipo')+1]
      if(razao == []):
        tipo = 'NONE'

      abertura = lista2[7]

      cadastral = lista[lista.index('Situação Cadastral')+1]
      if(cadastral == []):
        cadastral = 'NONE'

      data_cadastral = lista[lista.index('Data da Situação Cadastral')+1]
        
      # corrigir formatação do float
      capital = lista[lista.index('Capital Social')+1]
      if capital[-3:-2] == ".":
        p = re.compile('[^,][0-9]+')
        capital = p.findall(capital)
        capital = "".join(capital)
        capital = capital.replace(" ", "")
        capital = float(capital)
      else:
        p = re.compile(r'[0-9]+')
        capital = p.findall(capital)
        capital = "".join(capital)
        capital = int(capital)

      natureza = lista[lista.index('Natureza Jurídica')+1]
      if(natureza == []):
        natureza = 'NONE'
        
      mei = lista[lista.index('Empresa MEI')+1]
      if(mei == []):
        mei = 'NONE'

      logradouro = lista[lista.index('Logradouro')+1]
      if(logradouro == ''):
        logradouro = 'NONE'

      numero = lista[lista.index('Número')+1]
      if(numero == ''):
        numero = 'NONE'
        
      complemento = lista[lista.index('Complemento')+1]
      if(complemento == ''):
        complemento = 'NONE'
      else:
        complemento = complemento.replace("  ","").replace(";", " ").replace(":","").strip()

      cep = lista[lista.index('CEP')+1]
      if(cep == ''):
        cep = 'NONE'
      else:
        p = re.compile(r'\d')
        cep = p.findall(cep)
        cep = "".join(cep)

      bairro = lista[lista.index('Bairro')+1]
      if(bairro == ''): 
        bairro = 'NONE'
        
      municipio = lista[lista.index('Município')+1]
      if(municipio != ''):
        p = re.compile(r'[A-Z]+')
        municipio = p.findall(municipio)
        municipio = " ".join(municipio)
      else:
        municipio = 'NONE'

      uf = lista[lista.index('UF')+1]
      if(uf != ''):
        p = re.compile(r'[A-Z]+')
        uf = p.findall(uf)
        uf = "".join(uf)
      else:
        uf = 'NONE'

      if('Telefone' in lista):
        telefone = lista[lista.index('Telefone')+1:lista.index('E-MAIL')]
        if(len(telefone) > 1):
            telefone = ",".join(telefone)
            telefone = telefone.replace("-", "").replace(" ","")
            telefone = list(telefone.split(","))
        else:
            p = re.compile(r'\d+')  
            telefone = p.findall(str(telefone))
            telefone = "".join(telefone)
      else:
        telefone = 'NONE'

      email = lista[lista.index('E-MAIL')+1]
      if(email == ''):
        email = 'NONE'

      societario = lista[lista.index('Quadro Societário')+1:lista.index('Atividade Principal')]
      if(societario == []):
        societario = 'NONE'

      principal = lista[lista.index('Atividade Principal')+1:lista.index('Atividades Secundárias')]
      if(principal == [' - ']):
        principal = 'NONE'

      secundaria = lista[lista.index('Atividades Secundárias')+1:lista.index('Data da Consulta')]
      if(secundaria == []):
        secundaria = 'NONE'

      # dicionário dos dados obtidos
      dados = {'CNPJ':cnpj,
            'Razao_social':razao,
            'Nome_fantasia':fantasia,
            'Tipo':tipo,
            'Data_abertura':abertura,
            'Situacao_cadastral':cadastral,
            'Data_da_situacao_cadastral':data_cadastral,
            'Capital_social':capital,
            'Natureza_juridica':natureza,
            'MEI':mei,
            'Logradouro':logradouro,
            'Numero':numero,
            'Complemento':complemento,
            'CEP':cep,
            'Bairro':bairro,
            'Municipio':municipio,
            'UF':uf,
            'Telefone':telefone,
            'Email':email,
            'Quadro_societario':societario,
            'Atividade_principal':principal,
            'Atividades_secundaria':secundaria}
      dados_clientes.append(dados)
      time.sleep(0.01)

    # exportando os conteúdo obtido para um csv
    csv_conteudo = pd.DataFrame(dados_clientes)
    csv_conteudo.to_csv('C:\\Users\\Bruno\\Desktop\\web_scraping\\Saida\\dados.csv', sep = ';', index = False, encoding = 'utf-8-sig')