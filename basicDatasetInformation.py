# -*- coding: utf-8 -*-
import json

def countUsers(dataset):
        
    allUser = []
    erros = 0
    for arq in dataset:
        for linha in arq:
            try:
                tweet = json.loads(linha)
                user = tweet['user']['screen_name']
                allUser.append(user)
            except:
                erros += 1 
                print tweet
                print
    print "Erros:",erros
    distinctAllUser = set(allUser)
    return len(distinctAllUser)
    


if __name__ == "__main__":
    
    arq0 = open("collection_0.json")
    arq1 = open("collection_1.json")
    arq2 = open("collection_2.json")
    arq3 = open("collection_3.json")
    arq4 = open("collection_4.json")
    arq5 = open("collection_5.json")

    arquivos = [arq0,arq1,arq2,arq3,arq4,arq5]
    pathDestino = "resultadosAnalises/"
    print countUsers(arquivos)
    exit()
    destFile = open(pathDestino+"DatasetBasicInformations.csv","w")    
    destFile.write("total User,"+str(countUsers(arquivos)))
    destFile.close()




    
