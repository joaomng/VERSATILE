import pymongo
import pegarTweetsPerfilPorNome as pegarTweetsPerfil
import pegarTweetsProjTimeline as pegarTweetsProj
import pandas as pd


#nota: texto do tweet é 'full_text',
#e a data é 'created_at' , não confundir com 'user'['created_at'] 
mongo = pymongo.MongoClient()
db = mongo["covid19_perfis_v3"]
'''users = pegarTweetsPerfil.getUserNameFromList()
for user in users:
    print("procurando dados do usuario ",user)
    print("\n")
    collection = db[user]
    encontrados = collection.find_one()
    if (encontrados == None):
    	print("f\n")
    else:
        print(encontrados)
        print("\n")
'''

users = pegarTweetsPerfil.getUserNameFromList()
for user in users:

	try:
		collection = db[user]
	except:
		continue

	tweets = collection.find()
	mongo_docs = list(tweets)
	#if(len(mongo_docs)>=50):
    #	mongo_docs = mongo_docs[:50]
    
	print("usuario"+user+"tem "+str(len(mongo_docs))+" tweets\n")

	docs = pd.DataFrame(columns=[]) #é o que eu vou salvar no json
	for num,doc in enumerate(mongo_docs):
		doc["_id"] = str(doc["_id"])
		series_obj = pd.Series( doc, name=doc['_id'] )
		docs.append(series_obj)
    	#docs = docs.append(series_obj)?
	nome = user+".json"
    print("len(docs) = "+str(len(docs))+"\n")
	docs.to_json(nome)
	print("funcionou? "+user+"\n\n")



