#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import codecs

arq1 = open("protests_collection.json")
arq2 = open("protests_collection_1.json")
arq3 = open("protests_collection_2.json")
arq4 = open("protests_collection_3.json")
arq5 = open("protests_collection_4.json")

destino = ""

des = codecs.open(destino+"teste.json",'w',"utf-8")
a = "tião o caçador de órgãos"
des.write(a.decode("utf-8"))
des.close()
exit()

des1 = codecs.open(destino+"collection_1.json",'w',"utf-8")
des2 = codecs.open(destino+"collection_2.json",'w',"utf-8")
des3 = codecs.open(destino+"collection_3.json",'w',"utf-8")
des4 = codecs.open(destino+"collection_4.json",'w',"utf-8")
des5 = codecs.open(destino+"collection_5.json",'w',"utf-8")

arquivos = [arq1,arq2,arq3,arq4,arq5]
destinos = [des1,des2,des3,des4,des5]

for i in range(len(arquivos)):
    arq = arquivos[i]
    des = destinos[i]

    for linha in arq:
        linha = "{"+linha[50:]
        #tweet = json.loads(linha)
        #del tweet["_id"]
        des.write(linha.decode("utf-8"))
        
        #a = input("sair - 0")        
        #if int(a) == 0:
        #    exit()
           
