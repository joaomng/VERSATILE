from pegarTweetsProjTimeline import pegarTweetsUsuarioCovid19
import oauth2 as oauth
import pymongo
import json
import time

def getMaxIdInPreviousData(collection):

    maxId = 0
    #Busca de base para o usuário
    tweet = collection.find().sort("id",1).limit(1)
    #Se existe existe, continua a coleta de onde parou ou pega apenas os novos. Se não existe, maxId e sinceId continuam zero
    if (tweet.count()):#count is deprecated
    #if (tweet.count_documents):#versoes mais antigas do python nao reconhecem count_documents

        #TODO: checar se já atingiu a última mensagem, ou seja, no bd 'celetou_tudo' é TRUE
        #se coletou_tudo sinceId
        maxId = tweet[0]["id"]
        maxId -= 1 # diminui 1 porque maxId inclusive

    return maxId

#diferente de maxId, sinceId é exclusive, então não precisar subritair ou somar nada
def getSinceIdInPreviousData(collection):

    sinceId = 0
    #Busca de base para o usuário
    tweet = collection.find().sort("id",-1).limit(1)
    #Se existe existe, continua a coleta de onde parou ou pega apenas os novos. Se não existe, maxId e sinceId continuam zero
    if (tweet.count()):#count is deprecated
    #if (tweet.count_documents): #versoes mais antigas do python nao reconhecem count_documents

        #TODO: checar se já atingiu a última mensagem, ou seja, no bd 'celetou_tudo' é TRUE
        #se coletou_tudo sinceId
        sinceId = tweet[0]["id"]
    return sinceId

#verifica se janela diaria foi alcançada. se foi, poe pra dormir ate o proximo dia (janela de 24h)
def verifyingRemainingRequestsInADay(response):
    #existe um maximo de requisicoes por dia. atualmente 100000
    remainingRequestsInADay = int(response["x-app-rate-limit-remaining"])
    #maxRequestsIn24Hours = float(response["x-app-rate-limit-limit"])   

    #verificando se atingiu maximo de requisicoes em 24h
    slept = False
    
    if ( remainingRequestsInADay == 0 ):
        #epoch time para encerrar as 24h
        dayRateLimitReset= float(response["x-app-rate-limit-reset"])
        currentMoment = time.time()
        timeSleeping = round(dayRateLimitReset - currentMoment)
        print("dormindo ate completar 24h. Faltam ",timeSleeping," sec")
        time.sleep(timeSleeping)
        slept = True

    return slept

#verifica se janela de requisicoes foi alcançada. se foi, poe pra dormir ate a proxima janela
def verifyingRemainingRequestInAWindows(response):
    #existe uma maximo de requisicao a cada janela de tempo e esse maximo depende do autenticacao
    #requestPerWindow = float(response["x-rate-limit-limit"])
    remainingRequestInCurrentWindow = int(response["x-rate-limit-remaining"])
    
    #verificando se atingiu numero maximo de requisicoes na janela
    slept = False
    if ( remainingRequestInCurrentWindow == 0 ) :
        #epoch time do momento no qual a janela será zerada
        rateLimitReset = float(response["x-rate-limit-reset"])
        currentMoment = time.time()
        timeSleeping = round(rateLimitReset - currentMoment)

        time.sleep(timeSleeping)
        slept = True        

    return slept

def getDataUserFromTimeLine(user_name, collection,client):
    #sempre comecam com zero
    maxId = getMaxIdInPreviousData(collection)
    sinceId = getSinceIdInPreviousData(collection)

    #auxilia na identificacao se está (re)iniciando a coleta, entao apenas novas postagens devem ser coletadas
    aux = 0
    #dispara a coleta por perfil
    while True:

        try:
            
            #pegando apenas os tweets novos após a primeira coleta
            if ((sinceId > 0) and (aux == 0)):
                maxId = 0
            
            aux = 1
            
            response,data = pegarTweetsUsuarioCovid19(client, user_name, sinceId, maxId)

            #verifica se janela diaria foi alcançada. se foi, dormiu e ja é outra janela de 24h           
            if  (verifyingRemainingRequestsInADay(response)):
                continue
            
            #verifica se janela de requisicoes foi alcancada. se foi, dormiu e ja e outra janela
            if (verifyingRemainingRequestInAWindows(response)):
                continue

            #LEVI
            data = data.decode("utf-8")
            data = json.loads(data)
            #verifica se dados estao vazios, se nao atingiu os limites de requisicao, chegou a última mensagem
            if (len(data) == 0):
                #TODO: setar 'coletou_tudo' no bd relacional como TRUE para indicar que já foi ao fim
                #TODO: atualizar o sinceId para o mais recente na base e atualizar banco
                #interromper coleta
                break
            
            #atualiza o maxId para o menor da lista
            maxId = (data[-1]['id'] - 1)

            collection.insert_many(data,ordered=False)
            #paradas de acordo com o response

           #TODO: atualizar maxId no bd relacional    
                
        except Exception as e:
            print(e, "In getDataUserFromTimeLine")
            print("user_name: ",user_name)
            print("max_id: ",maxId)
            
            break
            #dorme intervalo maximo de um dia para zerar maximo de requisicoes diárias
            #time.sleep(3600 * 24)
        
def getUserNameFromList():
    #with open("TwitterPerfis.csv") as arq:
    linhas = open("TwitterPerfis.csv")

    perfis = []
    for perfil in linhas:
        perfil = perfil.strip()
        perfil = perfil.replace("@","")
        perfis.append(perfil)
    
    perfis.sort()
    #removendo possiveis repeticoes
    return set(perfis)    


def setColeta(client, db):

    users = getUserNameFromList()
    
    while True:
        for user_name in users:
            collection = db[user_name]
            getDataUserFromTimeLine(user_name, collection,client)


if __name__ == "__main__":
    
    Consumer_key = "tgkEDvvrO5ZaID0JiSfL3qEEu"
    Consumer_secret = "CufyEvNWOF2Q8qxEh6e11iR5LEldQzrDKS9sSutP6dMOvdZTWN"
    Access_token = "3054840988-xakWZhFQpBdZSN2AA2OG0S6Tws7F4CHZId1JnYK"
    Access_token_secret = "zbHrs60Jhe46d9RvOcV9MSKDRBcq7gkREeajjeUIEPFks"

    consumer = oauth.Consumer(key=Consumer_key, secret=Consumer_secret)
    access_token = oauth.Token(key=Access_token, secret=Access_token_secret)
    client = oauth.Client(consumer, access_token)

    mongo = pymongo.MongoClient()
    db = mongo["covid19_perfis_v3"]
    
    setColeta(client, db)
