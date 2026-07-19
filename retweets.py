# -*- coding: utf-8 -*-
import re
import json
from dateutil import parser
import random
import codecs

def countRetweets(arquivos):
    qtdeRetweets = 0
    for arq in arquivos:

        for tweet in arq:
            tweet = json.loads(tweet)
            text = tweet['text']
            text = "RT @tcruzfranca" #pegar minus
            if (re.findall("RT\s@",text)):
                qtdeRetweets += 1
            break
        break
    print "Quantidade Retweets:", qtdeRetweets



if __name__ =='__main__':

    '''
     informar colecao... no exemplo abaixo, estou lendo de um arquivo. Se for ler do mongo ou outro banco, será necessário adaptar.
    arq0 = open("collection_0.json")
    arq1 = open("collection_1.json")
    arq2 = open("collection_2.json")
    arq3 = open("collection_3.json")
    arq4 = open("collection_4.json")
    arq5 = open("collection_5.json")
    '''

    #arquivos aponta para todas as coleções que quis avaliar
    arquivos = [arq0,arq1,arq2,arq3,arq4,arq5]
    #a linha abaixo aponta para um arquivo csv onde guardo o resultado da análise
    arq_novo = codecs.open("retweets.csv",'w',"utf-8")
    #a funcao countRetweets apenas conta os retweets, mas pode ser facilmente adaptada para realizar outra atividade.
    countRetweets(arquivos)    

    '''
    fechando os arquivos
    arq1.close()
    arq2.close()
    arq3.close()
    arq4.close()
    arq5.close()
    '''
    arq_novo.close()
    #teste()
    #print countRetweets(arquivos)
    print "FIM"

'''
#dicionario = {}
cont = 0
for arq in [arq1,arq2,arq3,arq4,arq5]:
    for linha in arq:
        tweet = json.loads(linha)
        text = tweet['text']
        if

import re
import urllib2
import oauth2 as oauth
import pymongo
import json

Consumer_key = "NChfxFupjBZJKyYhKOPTddY3m"
Consumer_secret = "MoLRppE6ZscKxhqA3f7czPr7EnQPtZ5bhLAEtEgmTy7zgZyakw"
Access_token = "118812510-r35kho23NUMLU0Kd9V2vwaM6KiJNE4EPvJjgFHvo"
Access_token_secret = "2ABbVLH3FGCXXk5lNYj9C3Ws8WMfwWnwXpfZoWVnarW25"

consumer = oauth.Consumer(key=Consumer_key, secret=Consumer_secret)
access_token = oauth.Token(key=Access_token, secret=Access_token_secret)
client = oauth.Client(consumer, access_token)
URL = "https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name=tcruzfranca&count=1"
response,data = client.request(URL,"GET")


print response
print
print
print data

print
tweet = json.loads(data)
print tweet[0]
'''
