import networkx as nx

#OSS339357E72DB145E2B   ENGLISH LIVE

def extractVectorFromFile(arq):
    edges = []
    cliques = []
    qtdeNodesInitialState = 0
    for tweet in arq:
        tokens = tweet.replace("\n","")
        tokens = tokens.split(' ')
        #tokens = list(map(str.strip,tokens))
        tokens.sort()
        tokens2 = list(set(tokens))
        tokens2.sort()
        cliques.append(tokens2)
        tam = len(tokens2)
        qtdeNodesInitialState += tam
        aux = []
        for i in range(tam):        
            for j in range(i+1, tam):
               aux.append((tokens2[i],tokens2[j]))
        edges.extend(aux)
    arq.close()
    return edges,cliques,qtdeNodesInitialState

def q0(nodesVector, qtdeNodesInitialState): #initial Values
    '''
        nodesVector = cliques (cada tweet forma um clique o qual e um vetor com os tokens enquanto cliques [nodesVector] e um vetor de tweets)
        qtdeNodesInitialState = quantidade de tokens antes de juxtaposition e overlaping
    '''

    val = 0
    K_q0 = 0
    for clique in nodesVector: #nodesVector e o conjunto de cliques (palavras dos tweets)
        qtdeNodesInClique = len(clique)
        val += (qtdeNodesInClique * (qtdeNodesInClique-1)) #somatorio de qi (quantidade de nos em um clique)
        
    aux = qtdeNodesInitialState * (qtdeNodesInitialState - 1) #total de nos, total de possiveis vertices n * (n-1) para grafos nao direcionados
    delta = val/float(aux)
    K_q0 = val/float(qtdeNodesInitialState)
    
    return delta,K_q0


def metricsForGraph(fileDestination,qtdeNodesInitialState,edgesVector, cliquesVector, initialDensity, initialNetDegree):

    '''
    fileDestination
    qtdeNodesInitialState -> qtdeNodesInitialState
    edges -> edgesVector
    cliques -> cliquesVector
    initialDensity -> initialDensity
    initialNetDegree -> initialNetDegree        
    '''
    
    G = nx.Graph()
    G.add_edges_from(edgesVector)
          
    numberOfNodes = len(G.nodes())
    numberOfEdges = len(G.edges())

    netCentrality = 0.0 #ou netDegree
    for x,y in nx.degree_centrality(G).items():
        netCentrality += float(y)

    graphDensity = nx.density(G)
    clusteringCoef = nx.average_clustering(G)
   
    qtdeComponents = nx.number_connected_components(G)
    #print qtdeComponents
    #components = sorted(nx.connected_components(G), key=len, reverse=True) #nao precisa ordenar, muito menos de ordem reversa ou opelo tamanho
    aux = 0
    components = nx.connected_components(G)
    S = [G.subgraph(c).copy() for c in components]
    for i in S:
       qtdeNodes = len(i.nodes)
       aux+=qtdeNodes*(qtdeNodes - 1)

    F = 1 - aux/(len(G.nodes())*(len(G.nodes()) - 1))

    
    #cálculo antigo da fragmentação aqui:
    #aux = 0
    #for i in cliquesVector:
    #   qtdeNodes = len(i)
    #   aux += qtdeNodes * (qtdeNodes-1)

    #F = 1 - aux/float(numberOfNodes*(numberOfNodes-1))
    Fcliques = (qtdeComponents-1)/float(len(cliquesVector)-1)
    
    #DEBUG
    print("escrevendo métricas no arquivo")
    fileDestination.write(str(qtdeNodesInitialState)+','+str(numberOfNodes)+","+str(numberOfEdges)+","+str(graphDensity)+","+str(initialDensity)+','+str(netCentrality)+","+str(initialNetDegree)+','+str(clusteringCoef)+','+str(F)+','+str(Fcliques)+"\n")


def apenasFragmentacao(fileDestination,qtdeNodesInitialState,edgesVector, cliquesVector, initialDensity, initialNetDegree):
	G = nx.Graph()
	G.add_edges_from(edgesVector)

	aux = 0
	components = nx.connected_components(G)
	S = [G.subgraph(c).copy() for c in nx.connected_components(G)]
	for i in S:
		qtdeNodes = len(i.nodes)
		aux+=qtdeNodes*(qtdeNodes - 1)

	F = 1 - aux/(len(G.nodes())*(len(G.nodes()) - 1))

	print("escrevendo Fragmentação no arquivo")
	fileDestination.write(str(F)+"\n")
   

def weightedVector(edgesVector):
    setVector = set(edgesVector)
    weightedVector = []
    
    for feature in setVector:
        weightedVector.append((feature[0], feature[1], edgesVector.count(feature)))
    
    print(weightedVector)
    return weightedVector
    

def metricsForWeightedGraph(fileDestination,edgesVector):
    G = nx.Graph()

    #G.add_weighted_edges_from(weightedVector(edgesVector))
    v = weightedVector(edgesVector)
    for i in v:
        G.add_edge(i[0],i[1],weight=i[2])
    
    
    fileDestination.write("nodes,edges,networkCentrality,graphDensity,clusteringCoef\n")
    
    numberOfNodes = len(G.nodes())
    numberOfEdges = len(G.edges())

    netCentrality = 0.0
    for x,y in nx.degree_centrality(G).items():
        netCentrality += float(y)

    graphDensity = nx.density(G)
    clusteringCoef = nx.average_clustering(G)

    fileDestination.write(str(numberOfNodes)+","+str(numberOfEdges)+","+str(netCentrality)+","+str(graphDensity)+","+str(clusteringCoef)+"\n")    



#MultiGraph nao tem algumas funcoes como average_clustering
def metricsForMultiGraph(fileDestination,edgesVector):
    G = nx.MultiGraph()
    G.add_edges_from(edgesVector)
    
    fileDestination.write("nodes,edges,networkCentrality,graphDensity,clusteringCoef\n")
    
    numberOfNodes = len(G.nodes())
    numberOfEdges = len(G.edges())

    netCentrality = 0.0
    for x,y in nx.degree_centrality(G).items():
        netCentrality += float(y)

    graphDensity = nx.density(G)
    clusteringCoef = nx.average_clustering(G)
    #clusteringCoef = nx.clustering(G)

    fileDestination.write(str(numberOfNodes)+","+str(numberOfEdges)+","+str(netCentrality)+","+str(graphDensity)+","+str(clusteringCoef)+"\n")    




def setInCliques(arq):

    setCliques = []    
    for tweet in arq:
        tokens = tweet.replace("\n","")
        tokens = tweet.split(',')
        tokens = map(str.strip,tokens)
        tokens.sort()
        #print tokens
        if (setCliques.count(tokens) == 0):
            setCliques.append(tokens)
            setCliques.sort()
        #print setCliques

    return setCliques

def principal(n_arqs, destino):
    '''
        Pega n_arqs com tweets na pasta janelas e salva as metricas no arquivo
        graph/<destino>.csv
    '''
    fileDestination = open("graph/"+destino+".csv","w+")
#fileDestinationMultiGraph = open("multiGraph/results.csv","w")
#fileDestination.write("nodes,edges,networkCentrality,graphDensity,clusteringCoef\n")
    fileDestination.write("total_nodes,nodes,edges,graphDensity,initialDensity,networkDegree,initialNetDegree,clusteringCoef,fragmentation,fragClique\n")

    for i in range(0,n_arqs):
        #arq = open("T"+str(i)+".csv")
        arq = open("Janelas/T"+str(i)+".txt")
        edges,cliques,qtdeNodesInitialState = extractVectorFromFile(arq)
        if((len(edges)==0) or (len(cliques)<=1)): #pra nao haver divisão por zero
            arq.close()
            continue
        initialDensity, initialNetDegree = q0(cliques, qtdeNodesInitialState)

    #cliques = setInCliques(arq)
    #print len(cliques)

        metricsForGraph(fileDestination,qtdeNodesInitialState,edges,cliques,initialDensity,initialNetDegree)
    #metricsForMultiGraph(fileDestinationMultiGraph,edges)
        arq.close()

    fileDestination.close()
#cliques


    print("graph")
    return


def principal2(origem, destino):
    '''
        Pega o arquivo origem e salva as metricas no arquivo
        graph/<destino>.csv
    '''
    fileDestination = open("graph/"+destino+".csv","w+")
#fileDestinationMultiGraph = open("multiGraph/results.csv","w")
#fileDestination.write("nodes,edges,networkCentrality,graphDensity,clusteringCoef\n")
    fileDestination.write("total_nodes,nodes,edges,graphDensity,initialDensity,networkDegree,initialNetDegree,clusteringCoef,fragmentation,fragClique\n")

    
    #arq = open("T"+str(i)+".csv")
    arq = open(origem)
    edges,cliques,qtdeNodesInitialState = extractVectorFromFile(arq)
    if((len(edges)==0) or (len(cliques)<=1)): #pra nao haver divisão por zero
        arq.close()
        print("arquivo origem vazio ou quase")
        return
    initialDensity, initialNetDegree = q0(cliques, qtdeNodesInitialState)

    #cliques = setInCliques(arq)
    #print len(cliques)

    metricsForGraph(fileDestination,qtdeNodesInitialState,edges,cliques,initialDensity,initialNetDegree)
    #metricsForMultiGraph(fileDestinationMultiGraph,edges)
    arq.close()

    fileDestination.close()
#cliques


    print("Sucesso, cheque o arquivo destino na pasta graph")
    return


'''
fileDestination = open("weightedGraph/results.csv","w")
metricsForWeightedGraph(fileDestination,edges)
print "weightedgraph"
'''

'''
fileDestination = open("multiGraph/results.csv","w")
metricsForMultiGraph(fileDestination,edges)
print "multiGraph"
'''
def principal3(inicial, final, destino, append):
    '''
        Pega arquivos com tweets na pasta janelas (entre inicial e final), de nome T<num> e salva as metricas no arquivo
        graph/<destino>.csv , levando em consideração a informação de existencia ou não desse arquivo (se append = True, então
        o arquivo já existe)
    '''

    if(append):
    	fileDestination = open("graph/"+destino+".csv","a")
    else: 
    	fileDestination = open("graph/"+destino+".csv","w+")
#fileDestinationMultiGraph = open("multiGraph/results.csv","w")
#fileDestination.write("nodes,edges,networkCentrality,graphDensity,clusteringCoef\n")
    if(not(append)):
    	fileDestination.write("total_nodes,nodes,edges,graphDensity,initialDensity,networkDegree,initialNetDegree,clusteringCoef,fragmentation,fragClique\n")
    
    #n_arqs = (final - inicial) + 1 #se o final é T2 e o inicial T1, são 2 arquivos (2 - 1 +1)
    for i in range(inicial,final+1):
        #arq = open("T"+str(i)+".csv")
        print("Janela ", i)

        arq = open("Janelas/T"+str(i)+".txt")
        edges,cliques,qtdeNodesInitialState = extractVectorFromFile(arq)
        if((len(edges)==0) or (len(cliques)<=1)): #pra nao haver divisão por zero
            print("Não tem texto suficiente na janela", i)
            arq.close()
            continue
        initialDensity, initialNetDegree = q0(cliques, qtdeNodesInitialState)

    #cliques = setInCliques(arq)
    #print len(cliques)

        metricsForGraph(fileDestination,qtdeNodesInitialState,edges,cliques,initialDensity,initialNetDegree)
    #metricsForMultiGraph(fileDestinationMultiGraph,edges)
        arq.close()

    fileDestination.close()
#cliques


    print("graph")
    return


def principal4(inicial, final, destino, append):
    '''
        Pega arquivos com tweets na pasta janelas (entre inicial e final), de nome T<num> e salva APENAS A FRAGMENTAÇÃO
        no arquivo graph/<destino>.csv, levando em consideração a informação de existencia ou não desse arquivo (se append = True, então
        o arquivo já existe)

        ATENÇÃO ao nome da pasta com as janelas!!!
    '''

    if(append):
    	fileDestination = open("graph/"+destino+".csv","a")
    else: 
    	fileDestination = open("graph/"+destino+".csv","w+")
#fileDestinationMultiGraph = open("multiGraph/results.csv","w")
#fileDestination.write("nodes,edges,networkCentrality,graphDensity,clusteringCoef\n")
    if(not(append)):
    	fileDestination.write("fragmentation\n")
    
    #n_arqs = (final - inicial) + 1 #se o final é T2 e o inicial T1, são 2 arquivos (2 - 1 +1)
    for i in range(inicial,final+1):
        #arq = open("T"+str(i)+".csv")
        print("Janela ", i)

        arq = open("Janelas_Full_Com_Lema/T"+str(i)+".txt")
        edges,cliques,qtdeNodesInitialState = extractVectorFromFile(arq)
        if((len(edges)==0) or (len(cliques)<=1)): #pra nao haver divisão por zero
            print("Não tem texto suficiente na janela")
            arq.close()
            continue
        initialDensity, initialNetDegree = q0(cliques, qtdeNodesInitialState)

    #cliques = setInCliques(arq)
    #print len(cliques)

        apenasFragmentacao(fileDestination,qtdeNodesInitialState,edges,cliques,initialDensity,initialNetDegree)
    #metricsForMultiGraph(fileDestinationMultiGraph,edges)
        arq.close()

    fileDestination.close()
#cliques


    print("graph")
    return




