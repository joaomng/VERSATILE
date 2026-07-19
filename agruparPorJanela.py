def comparaData(dia1, mes1, dia2, mes2):
    '''função que compara duas datas e retorna
    True SOMENTE SE a primeira data for MAIOR
    que a segunda'''
    
    if(mes1 == mes2):
        if(dia1 > dia2):
            return True
        else:
            return False
    else:
        if(mes1 > mes2):
            return True
        else:
            return False
    

def diaAnterior(dia, mes):
    '''função que retorna uma tupla com o dia
    e mes correspondente ao dia anterior
    da data passada como parâmetro'''
    #por enquanto considera ano nao bissexto
    
    meses_com_31 = [1,3,5,7,8,10,12]
    
    if(dia==1):
        mes = mes-1
        if (mes in meses_com_31):
            dia = 31
        elif (mes==2):
            dia=28
        else:
            dia = 30
        
        return (dia, mes) 
            
    else:
        return (dia-1, mes)
    
def diaSeguinte(dia, mes):
    '''função que retorna uma tupla com o dia
    e mes correspondente ao dia seguinte
    da data passada como parâmetro'''
    meses_com_31 = [1,3,5,7,8,10,12]
    
    if ((mes in meses_com_31) and (dia == 31)):
        return (1, mes+1)
    
    elif((mes==2) and (dia==28)):
        return (1, mes+1)
    
    elif(dia==30):
        return (1,mes+1)
    
    else:
        return(dia+1,mes)
    
    

def agrupaPorJanela(inicio, fim, tam_janela):
    '''Função que, dado um data de inicio, uma data de fim
    e o tamanho da janela, coloca em arquivos separados os
    tweets criados em cada janela, com um dia de interseção.
    
    A função considera que os arquivos dos tweets
    estão separados por dias nos seguintes formatos:
    dd-mm, dd-m,d-mm ou d-m, e este também deve ser o
    formato das datas de inicio e fim.
    
    Os arquios das janelas são salvos em
    janela/dia-mes_dia-mes.txt com inicio e fim da janela, 
    por exemplo 7-5_9-11.txt'''
    
    #ToDo!!!
    #Fazer versão mais robusta usando o ano
    #Para isso mudar também as funcções auxiliares 
    #e a codificação no nome dos arquivos salvos com tweets


    
    dia_inicio=0
    mes_inicio = 0
    dia_fim = 0
    mes_fim = 0
    dia_fim_janela
    mes_fima_janela
    
    dia = 0
    mes =0
    
    #descobrindo o formato das datas de inicio e fim
    indice = inicio.index('-')
    dia_inicio = inicio[:indice]
    mes_inicio = inicio[indice+1:]
    
    indice = fim.index('-')
    dia_fim = fim[:indice]
    mes_fim = fim[indice+1:]
    
    dia = dia_inicio
    mes = mes_inicio
    
    path = str(dia)+'-'+str(mes)+"_"+str(dia_fim_janela)+"-"+str(mes_fim_janela)+".txt"
    arq = open(path, 'w+')
    #exemplo de nome: '7-5_14-5.txt" para uma janela de 7 dias (acaba sendo 8 pq conta inicio e fim
    #ToDo: não contar o fim? 
    
    
    #vou usar dia_inicio e mes_inicio como inicio das janelas,
    #ja que daqui pra frente nao usaria pra mais nada
    
    #while(comparaData(dia_inicio, mes_inicio, dia_fim, mes_fim) == False):
    while(True): #a verificação pra sair desse while está dentro do outro
        while(comparaData(dia, mes, dia_fim_janela, mes_fim_janela) == False):
            if(comparaData(dia, mes, dia_fim, mes_fim) == True):
                #pode ser que eu ainda esteja dentro da janela,
                #mas que eu já tenha passado da minha data final
                return
            #else
            #nota: o arquivo da janela foi aberto fora deste while
            arq_atual = open(str(dia)+'-'+str(mes)+'.txt', 'r')
            for linha in arq_atual: #colocando os tweets do dia no arquivo da janela
                arq.write(linha)
            
            dia,mes = diaSeguinte(dia, mes)
            arq_atual.close()
                         
        #fora do while de dentro        
        #gambiarra abaixo para ir para a próxima janela
        for i in range (tam_janela):
            dia_fim_janela,mes_fim_janela = diaSeguinte(dia_fim_janela,mes_fim_janela)
        
        dia,mes = diaAnterior(dia,mes) #pra ter interseção de um dia entre as janelas
        arq.close()
        path = str(dia)+'-'+str(mes)+"_"+str(dia_fim_janela)+"-"+str(mes_fim_janela)+".txt"
        arq = open(path, 'w+')