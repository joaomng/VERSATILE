
#arquivos de origem ja estao separados por dia
def getNextWindow(period,folderOrigin,folderDestin,windowSize = 7):

    ini = 0 #define quantidade de janelas    
    window = windowSize
    while window < len(period):
        fileDest = open(folderDestin+"T"+str(ini)+".csv","w")
        T = period[ini:window]
        for i in T:
            #arq = open(folderOrigin+i+".json")
            arq = open(folderOrigin+i)
            for linha in arq:
                linha = linha.replace(" ",",")
                fileDest.write(linha)

        ini += 1
        window += 1        
        fileDest.close()



#folderOrigin = 'separacaoWordNetWithouStopWordsStemming/palavrasSeparadasVirgula/'
#folderDestin = 'timeWindowFunc/'
#para verificar coesao apenas nas mensagens negativas e positivas
#folderOrigin = 'timeWindowFunc/negative/'
#folderDestin = 'timeWindowFunc/negativeWindows/'
#primeiro fiz nas negativas, a proxima agora sao as positivas
folderOrigin = 'timeWindowFunc/positive/'
folderDestin = 'timeWindowFunc/positiveWindows/'



period = ['1-6', '2-6', '3-6', '4-6', '5-6', '6-6', '7-6', '8-6', '9-6', '10-6', '11-6', '12-6', '13-6', '14-6', '15-6', '16-6', '17-6', '18-6', '19-6', '20-6', '21-6', '22-6', '23-6', '24-6', '25-6', '26-6', '27-6', '28-6', '29-6', '30-6', '1-7', '2-7', '3-7', '4-7', '5-7', '6-7', '7-7', '8-7', '9-7', '10-7', '11-7', '12-7', '13-7', '14-7', '15-7', '16-7', '17-7', '18-7', '19-7', '20-7', '21-7', '22-7', '23-7', '24-7', '25-7', '26-7', '27-7', '28-7', '29-7', '30-7', '31-7', '1-8']

getNextWindow(period,folderOrigin,folderDestin, 7)
