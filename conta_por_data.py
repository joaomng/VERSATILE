import json
#import datetime
from dateutil import parser

arq0 = open("collection_0.json")
arq1 = open("collection_1.json")
arq2 = open("collection_2.json")
arq3 = open("collection_3.json")
arq4 = open("collection_4.json")
arq5 = open("collection_5.json")


dicionario = {}

for arq in [arq0, arq1,arq2,arq3,arq4,arq5]:
    for tweet in arq:
        tweet = json.loads(tweet)
        data = tweet["created_at"]
        data = parser.parse(data)
        chave = str(data.day)+"-"+str(data.month)
        if (dicionario.has_key(chave)):
            dicionario.update({chave:dicionario.get(chave)+1})
        else:
            dicionario.update({chave:1})

arq_novo = open("freq_tweets.csv","w")
for i,j in dicionario.items():
    arq_novo.write(i+","+str(j)+"\n")

arq0.close()
arq1.close()
arq2.close()
arq3.close()
arq4.close()
arq5.close()
arq_novo.close()
