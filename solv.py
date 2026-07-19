

for i in range(0,55):
    arq = open("T"+str(i)+".csv")
    dest = open("temp/T"+str(i)+".csv","w")
    for linha in arq:
        linha = linha.replace("\n","")
        linha = linha.split(',')        
        tam = len(linha)
        for x in range(tam):
            for w in range(x+1,tam):
                dest.write(linha[x]+","+linha[w]+"\n")
        else:
            if tam == 1:
                dest.write(linha[0]+"\n")
                
    arq.close()
    dest.close()
    
print "FIM"
