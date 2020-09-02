# Web scraping de discursos presidenciais
coleta e estruturação dos textos transcritos dos discursos dos presidentes

***Em desenvolvimento***

O objetivo deste projeto é coletar todos os discursos presidenciais disponíveis em órgãos oficiais (Planalto e Biblioteca do Planalto) e disponibilizá-los de forma estruturada como banco de dados. 

No momento este repositório contém banco csv, jupyter notebook e script pyhton com códigos para web scraping, limpeza e estruturação dos discursos de Bolsonaro desde a posse até 2 de setembro de 2020.  Os textos coletados (270 ao todo) foram completamente limpos: tags html, acentos e pontuação foram retirados. No entanto, algumas transcrições apresentam cabeçalho com local e data que não foi possível retirar pois faziam parte do corpo do texto (ou seja, não estavam contidos em tags html separadas). Desta forma, palavras repetidas que constam no cabeçalho deverão ser tratadas quando o pesquisador fizer o tratamento do corpus para a análise segundo as necessidades de seu estudo.

Na pasta "Bolsonaro" constam:

**discursos_bolsonaro.csv:** banco de dados em formato csv com os textos coletados, data do discurso, ano do discurso e o link onde está hospedado o texto.

**webscraping_bolsonaro.py:** script Python com o desenvolvimento do projeto. 
