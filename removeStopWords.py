# -*- coding: utf-8

def _list_de_stopWords(arquivo):
    '''
        carrega lista de stopwords de arquivo.
        padrão utf-8
    '''
    lista = []
    arq = open(arquivo)

    for stop_word in arq:
        stop_word = stop_word.lower()
        stop_word = stop_word.replace('\n','')
        stop_word = stop_word.replace('\r','')
        lista.append(str(stop_word))
    
    arq.close()
    return lista  

def listStopWords(language="pt-br"):

    arquivo = "stopwords_pt.txt"
    if language == "pt-br":
        arquivo = "stopwords_pt.txt"
    else:
        print("Inclua a lista e altere o método listStopWords em removeStopWords")

    return _list_de_stopWords(arquivo)
