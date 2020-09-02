#!/usr/bin/env python
# coding: utf-8

# # Webscraping dos discursos de Bolsonaro

# Neste notebook você encontrará a programação em Python para coleta dos discursos, limpeza do texto e estruturação do banco de dados.
# 
# #### Essas são as etapas da programação (serão enumeradas ao longo do script):
# 
# 1) Coleta dos códigos fonte das páginas que em que estão os links das transcrições dos discursos. Criação dos links da paginação e scraping dessas páginas.
# 
# 2) Limpeza dos códigos fonte das páginas e coleta de todos os links que levam à transcrição dos discursos.
# 
# 3) Scraping da transcrição dos discursos.
# 
# 4) Coleta da data dos discursos
# 
# 5) Coleta dos textos dos discursos
# 
# 6) Limpeza dos textos e estruturação em banco de dados

# #### Fonte dos dados:
# Site do Planalto: https://www.gov.br/planalto/pt-br/acompanhe-o-planalto/discursos

# #### Carregando os pacotes


# Manipulação de dados

import os
import sys
import re
import time
import string
import unidecode
import requests
import datetime
import numpy as np
import pandas as pd

#Web scraping e processamento

from collections import Counter
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


# ## Web Scraping 
# Coleta realizada no dia 2 de setembro de 2020

# #### 1) Coleta dos códigos fonte das páginas que em que estão os links das transcrições dos discursos. Criação dos links da paginação e scraping dessas páginas.


#Primeiro preciso fazer um loop para abrir os links da paginação
# para em seguida coletar os links para os discursos dentro de cada 
#página.

#Primeiro crio uma lista com os números id das páginas
pgs = list(range(0,270,30))

#Agora crio os loops para salvar as urls criadas em uma lista
lista_urls = []
for i in pgs:
    url_completa = 'https://www.gov.br/planalto/pt-br/acompanhe-o-planalto/discursos?b_start:int=' + str(i)
    lista_urls.append(url_completa)


#Visualizando a lista de urls
lista_urls


#Função para fazer o scraping do código fonte das páginas (crawling da
#paginação). 

#Criando um contador para as paginas. São 9 páginas
contador = 9

#Criando a função
def scraping_urls(urls):
    
    # Define o driver
    driver = webdriver.Safari()
    
    # Lista para o resultado
    soup_list = []
 
    
    # Contador
    count = 0
    
    # Loop pelas urls
    for i in urls:
        if count < contador:
            driver.get(i)
            driver.refresh()
            time.sleep(5)
            soup_list.append(BeautifulSoup(driver.page_source, 'html.parser'))
        count += 1
    driver.close()
    return soup_list



#Fazendo o scraping das páginas
fonte= scraping_urls(lista_urls)


# #### 2) Limpeza dos códigos fonte das páginas e coleta de todos os links que levam à transcrição dos discursos.


#Coletando apenas as tags em que estão os links
tag_links=[]
for f in fonte:
    link=f.find_all('a', class_="summary url")
    tag_links.append(link)



#Finalmente coletando os links dentro das tags
links=[]
for i in tag_links:
    for j in i:
        link=re.search(r'<a class="summary url" href=\"(.*?)" title="Document">', str(j)).group(1)
        links.append(link)                       


# #### 3) Scraping da transcrição dos discursos.


# Definindo a função para fazer o scraping do texto dos discursos dos 
#links coletados acima

def extrai_discurso(urls):
    driver = webdriver.Safari()
    doc_source = []
    for i in urls:
        driver.get(i)
        time.sleep(5)
        doc_source.append(BeautifulSoup(driver.page_source, 'html.parser'))
    driver.close()
    return doc_source



# Aplicando a função à lista de links
#Encerrar a seção do webdriver anterior caso ela ainda esteja aberta!
discursos = extrai_discurso(links)


# #### 4) Coleta da data dos discursos


#Farei duas extrações da lista de links: uma para coletar as datas dos
#discursos e outra para coletar o texto em si. Vou começar coletando
#as datas.

#função para retirar data da tag span class="documentPublished"
def coleta_data(soup_object):
    data_list = []
    for s in soup_object:
        data= s.find_all('span', class_= 'documentPublished')
        data_list.append(data)
    return data_list



#loop para extração da data. Salvando as datas em lista
lista_data=[]
for i in coleta_data(discursos):
    lista_data.append(len(i))



#extraindo resultado da coleta
datas= coleta_data(discursos)



#Loop para coletar apenas a data que aparece entre as tags span
#de class=value e para retirar o horário
data_limpa=[]
for c in datas:
    cleaner= re.search(r'<span class="value"\>(.*?)</span>',str(c)).group(1)
    data_limpa.append(cleaner)

data_s_hora=[]
for d in data_limpa:
    sem_hora=d.split(' ',1)[0]
    data_s_hora.append(sem_hora)
    


# #### 5) Coleta dos textos dos discursos


#Agora seguirei para a extração dos textos dos discursos

# Função para extrair o texto dos discursos dos links. Uso o beautiful
#soup para encontrar as tags html de parágrafo ('p') e salvo os textos
#em lista
def extrai_texto(soup_object):
    text_list = []
    for s in soup_object:
        text = s.find_all('p')
        text_list.append(text)
    return text_list



# Loop para extração do texto. Salvo os textos em lista.
discurso_lista = []
for i in extrai_texto(discursos):
    discurso_lista.append(len(i))



# Extrai os discursos
primeiros_discursos = extrai_texto(discursos)



#Verificando quantos discursos foram coletados
len(primeiros_discursos)



#Dando uma olhada nos textos. Pegando apenas o primeiro da lista
primeiros_discursos[0]


# ### Limpeza do texto e estruturação do banco de dados


# Função para remover tags html
def remove_html_tags(text):
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)



#Aplicando a função para remover tags
strings=[]
for d in primeiros_discursos:
    cleaned=remove_html_tags(str(d))
    strings.append(cleaned)



#retirando \xa0 e colocando tudo em letras minúsculas.
limpos=[ ]
for i in strings:
    tira_xa=i.replace('\xa0', ' ').lower()
    limpos.append(tira_xa)



#Existem casos no texto em que não existe espaço entre pontuação e 
#palavras. Desta forma, precisarei incluir espaços entre pontuações
#e palavras antes de retirar a pontuação, assim evito que palavras 
#sejam concatenadas. Logo depois retirarei espaços em excesso.

#Incluindo espaços

limpos_espaco=[]
for i in limpos:
    esp=re.sub('([.,!?()])', r' \1 ', i)
    limpos_espaco.append(esp)



#Criando função para remover pontuação
def remove_pontuacao(valor):
    result = ""
    for c in valor:
        if c not in string.punctuation:
            result += c
    return result



#aplicando função para retirar pontuação na lista limpos
mais_limpos=[]
for i in limpos_espaco:
    tira_pontuacao=remove_pontuacao(i)
    mais_limpos.append(tira_pontuacao)



#retirando excesso de espaços em branco
s_espaco=[]
for i in mais_limpos:
    limpa_espaco=i.replace("    ", " ").replace("   ", " ").replace("  ", " ")
    s_espaco.append(limpa_espaco)




#Retirando acentos
texto_final=[]
for i in s_espaco:
    s_acento=unidecode.unidecode(i)
    texto_final.append(s_acento)



#Formatando as datas da lista data_s_hora (criada na seção anterior durante
#a coleta de string para date e salvando em um objeto do tipo pandas
data_final=pd.to_datetime(data_s_hora, format='%d/%m/%Y')



#criando objeto pandas apenas com os anos
anos=pd.DatetimeIndex(data_final).year



#Finalmente criando um data frame com data, ano, link do discurso e o
#texto do discurso

bolsonaro=pd.DataFrame([data_final, anos, links, texto_final]).T
bolsonaro.columns=['data', 'ano', 'link', 'transcricao']
bolsonaro.insert(0,'presidente', 'bolsonaro')
bolsonaro.head(5)



#Salvando o banco como csv:
bolsonaro.to_csv('discursos_bolsonaro.csv')



