folder = 'temp/'

for i in range(41,55):
    arq = open(folder+"T"+str(i)+".csv")
    cont = 0
    cont2= 0
    for linha in arq:
        linha = linha.split(",")
        cont += 1
        if len(linha) <= 0:
            
            print cont
        elif len(linha) == 1:
            cont2+= 2
           
        else:
            pass
    print cont
