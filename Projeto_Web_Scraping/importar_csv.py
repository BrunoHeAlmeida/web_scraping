import csv
import os

# importar conteudo do csv
def csv_arquivo(nome_csv, nome_lista):
    with open(nome_csv, 'r') as csv_arquivo:
        csv_conteudo = csv.reader(csv_arquivo)
        
        for linha in csv_conteudo:
            nome_lista.append((', '.join(linha)))

# importar lista de arquivos
lista_arquivos = os.listdir('C:\\Users\\Bruno\\Desktop\\web_scraping\\Entrada')
arquivo_csv = []
Lista_CNPJ = []

def csv_conteudo():
    for arquivo in lista_arquivos:
        if ".csv" in arquivo: 
            arquivo_csv.append(arquivo)
    for i in arquivo_csv:
        csv_arquivo('C:\\Users\\Bruno\\Desktop\\web_scraping\\Entrada\\' + i, Lista_CNPJ)
    return Lista_CNPJ

# subdivisão das listas
def listas_menores(lista, n):
    for i in range(0, len(lista), n):
        yield lista[i:i + n]
