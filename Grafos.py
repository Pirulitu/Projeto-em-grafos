def gerarVertices(quantVertices):# armazena os rotulos da quantidade de verteces desejada em uma lista
    vertices = []
    for x in range (1,quantVertices+1):
        V = "v"
        x = str(x)
        V = V+x
        vertices.append(V)
    return vertices

def gerarArestas(quantArestas):# armazena os rotulos da quantidade de arestas desejada em uma lista
    arestas = []
    for x in range (1,quantArestas+1):
        A = "a"
        x = str(x)
        A = A+x
        arestas.append(A)
    return arestas

def lerMatriz(vertices,arestas):# insere uma matriz VxA desejada com a quantidade previamente definida
    matriz = []
    print("|------------------------------------------------------------|")
    print("|                      LEITURA DA MATRIZ                     |")
    print("|------------------------------------------------------------|")
    print("| Exemplode entrada de uma matriz 3x3:                       |")
    print("| 1 0 3                                                      |")
    print("| 0 2 3                                                      |")
    print("| 1 2 0                                                      |")
    print("| A matriz acima tem arestas de peso 1, 2 e 3 e cada número  |")
    print("| é separado por espaço e um enter ao final de cada linha    |")
    print("|------------------------------------------------------------|")
    print("| Insira a matriz de Incidência do Grafo G "
          "(%d" % vertices, "X %d):          |\r" % arestas)
    print("|------------------------------------------------------------|")

    for x in range (vertices):#olha para a quantidade de linhas e roda
        linha = input().split()#lê uma linha
        for coluna in range(arestas):#pega os elementos da coluna da linha
            linha[coluna] = int(linha[coluna])#transforma em inteiro
        matriz.append(linha)#guarda na matriz
    print("|------------------------------------------------------------|")

    return matriz

def imprimirMatriz(vertices, arestas,matriz): #exibe a matriz desejada formatada como uma tabela

    print("|------------------------------------------------------------|")
    print("|                     MATRIZ DE INCIDENCIA                   |")
    print("|------------------------------------------------------------|")
    print("|    ", end="")
    for aresta in arestas:
        print(aresta, end="  ")
    print("")
    count = 1
    for vertice in vertices:
        print("| ",end="")
        print(vertice, end=" ")

        count2 = 0
        for x in arestas:

            numero =str(matriz[count-1][count2])
            print("%s" %numero, end= " "*(4-len(numero)))
            count2 += 1

        print("")
        count += 1

def escolherOrigem(vertices): #escolhe a origem deesejada dentre o conjunto de vertices

    existe = False
    while existe == False: #enquanto nao for definida uma origem do grafo valida nao pode seguir
        print("|------------------------------------------------------------|")
        print("|                        ORIGEM DO GRAFO                     |")
        print("|------------------------------------------------------------|")
        print("| Vertices do grafo G:")
        print("| ", end="")
        for v in vertices:
            print(v, end=" ")
        print("")
        origem = str(input("| Qual a origem do grafo? "))
        origem = origem.lower()
        for v in vertices:
            if origem == v:
                existe = True
        if existe:
            return origem
        else:
            print("Origem selecionada não existe no conjunto de vertices!")

def criaGrafo(matriz,vertices,arestas):
    # recebe a matriz da entrada, dois conjuntos de strings gerados para referenciar os vertices e as arestas
    # faz a referencia de vertice com aresta e guarda suas respectivas conexoes e assim,
    # ao final, gerando o grafo como uma lista que contem o primeiro elemento a origem
    # e as tuplas seguintes contendo com possiveis nos visinhos, (no, peso)

    indiceV,indiceA = 0,0
    grafo = []

    for a in arestas: #procura conexao nas linhas(arestas), assim somente teremos 2 elementos preenchidos
        indiceV = 0
        ligacao = 0 #contador da ligação de vertice, assim pode-se saber se o vertice ja conectou uma vez com a aresta ou nao
        for v in vertices:

            peso = matriz[indiceV][indiceA]
            if  peso != 0:
                if ligacao == 0:
                    #se nao tiver ligação, faz a primeira e vai procurar a proxima na mesma linha
                    vert = v
                    ligacao = 1#seta 1 na ligação
                else:
                    aresta = (v, peso)#guarda o vertice que é conectado a origem e seu peso em uma tupla
                    conexao1 = [vert,aresta]#guarda a conexao completa da aresta, um lado a origem e do outro o caminho possivel com o seu respectivo peso
                    conexao2 = [v,(vert,peso)]
                    grafo.append(conexao1)#guarda a conexao no grafo
                    grafo.append(conexao2)
                    ligacao = 0#informa que foram feitas as duas ligaçoes e reseta o valor
                    break#para a interação pois ja achou as duas arestas
            indiceV = indiceV + 1
        ligacao = 0 #ignora loop no proprio vertice
        indiceA = indiceA + 1

    count = 1
    grafo.sort()
    while count < len(grafo):#agrupa dois ou mais vertices de mesma origem com varias tuplas de caminhos e peso respectivo

        proximo = grafo[count]
        atual = grafo[count-1]
        if atual[0] == proximo[0]:
            atual.append(proximo[1])
            grafo.remove(proximo)
        else:
            count = count+1

    return grafo

def estruturarGrafo(g,conjuntoV):#estrutura o grafo em lista como um dicionario para facilitar no acesso de comparação

    vertices = conjuntoV.copy()#faz uma copia dos vertices para nao alterar os dados para quando for utilizalo na outra função
    grafo = {}
    for v in g:#para cada origem com varios destinos
        origem = v[0]#pegue origem
        #pegue o conjunto de vertices do grafo
        if vertices.__contains__(origem):#verifique se a origem existe no conjunto de grafos com caminhos
            vertices.remove(origem)     #se existir é por que ele é um elemento que contem nos ligados a ele
            for n in range(1, len(v)):#agrupa os elementos de mesma origem
                vertice = v[n][0]
                peso = v[n][1]
                if n == 1:#se ele for o primeiro elemento agrupado ele guarda como o primeiro destino
                    destino = {vertice: peso}
                    ver = {origem: destino}
                else:#se ele nao for o primeiro, ele agrupa junto com os outros nos existentes
                    destino = {vertice: peso}
                    ver[origem].update(destino)
            grafo.update(ver)#sai do laço da origem atual e grava os nos respectivos

        #se ele nao existir no conjunto de origens significa que ele esta no conjunto de nos ligados a um vertice com origem ou ele é vazio
        #defina o vertice como vazio
    for v in vertices:#adiciona os vertices restantes ao dicionario do grafo
        ver = {v: {}}
        grafo.update(ver)

    return grafo

def caminhoDijkstra(grafo,verticeInicial):
#calcula o menor peso da origem ate qualquer vertice pertencente a o grafo
    atual = verticeInicial
    noNaoVisitados = []
    distanciaAtual,noAtual,caminhosPossiveis = {}, {}, {}

    for v in grafo.keys():
        noNaoVisitados.append(v)  # inclui os vertices aos nos não visitados
        distanciaAtual[v] = float('inf')  # inicia todos os vertices como infinito

    noAtual[atual] = 0
    distanciaAtual[atual] = 0 #seta a distancia da origem ate a origem como 0(trivial)
    noNaoVisitados.remove(atual)#remove dos nos restantes a calcular

    while noNaoVisitados:#enquanto nao visitados tiver elemento roda

        for noVizinho,peso in grafo[atual].items():#pega os nos visinhos do vertice atual com o seu peso
            calcularPeso = peso + noAtual[atual]#calcula a distancia, em peso, do no atual com o no visinho

            if distanciaAtual[noVizinho] == float("inf") or distanciaAtual[noVizinho] > calcularPeso:
                #verifica se a distancia do no vizinho ate a origem ainda nao foi calculada
                # ou é menor do que a distancia do caminho do no atual
                distanciaAtual[noVizinho] = calcularPeso #guarda o peso do no atual ate o visinho
                caminhosPossiveis[noVizinho] = distanciaAtual[noVizinho]#guarda o elemento no grupo de possiveis caminhos para o no visinho

        if caminhosPossiveis == {}:
            #se os caminhosPossiveis for vazio não existe conexao entre os nos
            #e nao tem por que calcular o menor peso do vizinho por que nao existe
            break

        minimoVizinho = min(caminhosPossiveis.items(), key=lambda n: n[1])#seleciona o menor peso dos nos vizinhos possiveis
        atual = minimoVizinho[0]#atual recebe o vertice de menor peso
        noAtual[atual] = minimoVizinho[1]
        noNaoVisitados.remove(atual)#remove o no atual dos visitados
        del caminhosPossiveis[atual]#remove os nos visinhos do no atual

    return distanciaAtual

def caminhoBellman_Ford(grafo,verticeInicial):
    # calcula o menor peso da origem ate qualquer vertice pertencente a o grafo
    distanciaAtual, caminhoAnterior = {}, {}

    for v in grafo.keys():
        distanciaAtual[v] = float('inf')  # inicia todos os vertices como infinito
        caminhoAnterior[v] = None #o vertice anterior nao existe ainda

    origem = verticeInicial
    distanciaAtual[origem] = 0  # seta a distancia da origem ate a origem como 0

    for i in range(len(grafo.keys()) - 1):  # roda a quantidade de vertices - 1
        for vertice in grafo.keys():  # para cada vertice
            for vizinho, peso in grafo[vertice].items():  # pegue os vizinhos e seus respectivos pesos
                # relaxe o vertice
                if distanciaAtual[vizinho] > distanciaAtual[vertice] + peso:
                # se a distancia atual do vertice vizinho for maior que a distancia do vertice atual
                # ate o vertice vizinho, a distancia do vizinho é igual a distancia do atual ate o vizinho
                    distanciaAtual[vizinho] = distanciaAtual[vertice] + peso
                    caminhoAnterior[vizinho] = vertice

    # verificação de ciclos negativos
    for vertice in grafo.keys():
        for vizinho, peso in grafo[vertice].items():
            if distanciaAtual[vizinho] > distanciaAtual[vertice] + peso:
                return "| Existe ciclo negativo!"

    return distanciaAtual

def arvoreMinimaKruskal(grafo,conjuntoV):

    vertices = conjuntoV
    naoVisitados = []
    arvoreKruskal = []
    vizinho = None

    for v in vertices:
        naoVisitados.append(v)
    while naoVisitados:  # fazer ate todos vertices serem visitados
        peso = float('inf')#peso inicia infinito
        for v in vertices:#para cada vertice do grafo
            for ver, p in grafo[v].items():# para cada vizinho, peso do pertice
                if v not in naoVisitados and ver not in naoVisitados:
                    #se a origem ja foi visitada e o vizinho tambem ignore
                    continue
                    #caso contrario pegue o menor peso e veja se é menor que o ja existente
                    #guarde a origem e o vizinho do peso referente
                if p < peso:
                    peso = p
                    origem = v
                    vizinho = ver

        arvoreKruskal.append((origem, vizinho, peso))#adiciona o menor caminho encontrado ao grafo

        if naoVisitados.__contains__(origem):
            #se a origem do caminho encontrado ainda nao foi visitada
            naoVisitados.remove(origem)#remove ele
        if naoVisitados.__contains__(vizinho):#se o vizinho do caminho encontrado ainda nao foi visitada
            naoVisitados.remove(vizinho)#remove ele

    return arvoreKruskal

def arvoreMinimaPrim(grafo,verticeInicial,conjuntoV):

    naoVisitados = []
    caminhoArvoreMinima = {}
    caminhos = []
    origem = verticeInicial
    for v in conjuntoV:#inclui os vertices ao conjunto de nao visitados
        naoVisitados.append(v)

    naoVisitados.remove(origem)#visita a origem(remove)
    caminhos.append(origem)#inicia o caminho da busca

    while naoVisitados:#enquanto existir vertices ainda nao visitados faça

        menorPeso = float('inf')# menor peso inicia grande

        for vertice in caminhos:
            #para cada caminho possivel veja seus vizinhos e
            # veja se o peso dele é menor que o que ja tem
            for vizinho,peso in grafo[vertice].items():

                if peso < menorPeso and caminhos.count(vizinho) == 0:
                    # se o vizinho nao for um caminho(ja tem existe na arvore)
                    # e o peso dele for menor que o que ja tem
                    menorPeso = peso
                    #atualize o peso
                    origem = vertice
                    #guarde a origem do caminho
                    vizin = vizinho
                    #guarde o vertice de destino apartir da origem
        caminhos.append(vizin)
        #adicione o menor vizinho aos caminhos alcançados da arvore

        if caminhoArvoreMinima.keys().__contains__(origem):
        # se o caminho da arvore ja tem um vertice que vai para um vizinho e
        # ele encontra outro caminho no mesmo vertice para outro vizinho diferente
            camin = {vizin:menorPeso}
            caminhoArvoreMinima[origem].update(camin)#adicione o caminho no vertice existente

        else:#caso contrario crie o vertice que origina e adicione o destino
            destino = {vizin: menorPeso}
            camin = {origem:destino}
            caminhoArvoreMinima.update(camin)

        if naoVisitados.count(vizin) == 1:#se o vizinho nao foi removido, remova
            naoVisitados.remove(vizin)

    return caminhoArvoreMinima

def startDijkstra():
    print("|------------------------------------------------------------|")
    print("|                        BUSCA DIJKSTRA                      |")
    print("|------------------------------------------------------------|")
    print("|                                                            |")
    print("| Insira a quantidade de Vertices(V) e Arestas(A) da matriz: |")
    numeroVertices  = int(input("| Numero de vertices:"))
    numeroArestas = int(input("| Numero de arestas:"))
    vertices = gerarVertices(numeroVertices)
    arestas = gerarArestas(numeroArestas)
    matriz = lerMatriz(numeroVertices, numeroArestas)
    print("| Deseja imprimir a matriz gerada?                           |")
    opcao = input("| S ou N:")
    opcao = opcao.upper()

    if opcao == 'S':
        imprimirMatriz(vertices, arestas, matriz)

    origem = escolherOrigem(vertices)

    grafo = criaGrafo(matriz, vertices, arestas)

    grafo = estruturarGrafo(grafo, vertices)

    menoresCustos = caminhoDijkstra(grafo,origem)
    print("|------------------------------------------------------------|")
    print("|                   MENOR CUSTO (DIJKSTRA)                   |")
    print("|------------------------------------------------------------|")
    print("|                                                            |")

    for v,p in menoresCustos.items():
        print("| Distancia de", origem,"para",v,"=",p,"                  ")

    return True

def startBellman_Ford():
    print("|------------------------------------------------------------|")
    print("|                      BUSCA BELLMAN-FORD                    |")
    print("|------------------------------------------------------------|")
    print("|                                                            |")
    print("| Insira a quantidade de Vertices(V) e Arestas(A) da matriz: |")
    numeroVertices = int(input("| Numero de vertices:"))
    numeroArestas = int(input("| Numero de arestas:"))
    vertices = gerarVertices(numeroVertices)
    arestas = gerarArestas(numeroArestas)
    matriz = lerMatriz(numeroVertices, numeroArestas)
    print("| Deseja imprimir a matriz gerada?                           |")
    opcao = input("| S ou N:")
    opcao = opcao.upper()

    if opcao == 'S':
        imprimirMatriz(vertices, arestas, matriz)

    origem = escolherOrigem(vertices)

    grafo = criaGrafo(matriz, vertices, arestas)

    grafo = estruturarGrafo(grafo, vertices)

    menoresCustos = caminhoBellman_Ford(grafo, origem)
    print("|------------------------------------------------------------|")
    print("|                 MENOR CUSTO (BELLMAN-FORD)                 |")
    print("|------------------------------------------------------------|")
    print("|                                                            |")
    if type(menoresCustos) == dict:
        for v, p in menoresCustos.items():
            print("| Distancia de", origem, "para", v, "=", p, "                  ")
    else:
        print(menoresCustos)
    return True

def startPrim():
    print("|------------------------------------------------------------|")
    print("|                     ARVORE MINIMA (PRIM)                   |")
    print("|------------------------------------------------------------|")
    print("|                                                            |")
    print("| Insira a quantidade de Vertices(V) e Arestas(A) da matriz: |")
    numeroVertices = int(input("| Numero de vertices:"))

    numeroArestas = int(input("| Numero de arestas:"))

    vertices = gerarVertices(numeroVertices)

    arestas = gerarArestas(numeroArestas)

    matriz = lerMatriz(numeroVertices, numeroArestas)

    print("| Deseja imprimir a matriz gerada?                           |")
    opcao = input("| S ou N:")
    opcao = opcao.upper()

    if opcao == 'S':
        imprimirMatriz(vertices, arestas, matriz)

    origem = escolherOrigem(vertices)

    grafo = criaGrafo(matriz, vertices, arestas)

    grafo = estruturarGrafo(grafo, vertices)

    menoresCustos = arvoreMinimaPrim(grafo, origem,vertices)
    print("|------------------------------------------------------------|")
    print("|                 ARVORE MINIMA GERADA (PRIM)                |")
    print("|------------------------------------------------------------|")
    print("|                                                            |")

    for vertice in menoresCustos.keys():

        for v, peso in menoresCustos[vertice].items():

            print("| ", vertice, "-->", v,"( com peso",peso,")")
    return True

def startKruskal():
    print("|------------------------------------------------------------|")
    print("|                    ARVORE MINIMA (KRUSKAL)                 |")
    print("|------------------------------------------------------------|")
    print("|                                                            |")
    print("| Insira a quantidade de Vertices(V) e Arestas(A) da matriz: |")
    numeroVertices = int(input("| Numero de vertices:"))
    numeroArestas = int(input("| Numero de arestas:"))
    vertices = gerarVertices(numeroVertices)
    arestas = gerarArestas(numeroArestas)
    matriz = lerMatriz(numeroVertices, numeroArestas)
    print("| Deseja imprimir a matriz gerada?                           |")
    opcao = input("| S ou N:")
    opcao = opcao.upper()

    if opcao == 'S':
        imprimirMatriz(vertices, arestas, matriz)

    grafo = criaGrafo(matriz, vertices, arestas)

    grafo = estruturarGrafo(grafo, vertices)

    menoresCustos = arvoreMinimaKruskal(grafo,vertices)
    print("|------------------------------------------------------------|")
    print("|                ARVORE MINIMA GERADA (KRUSKAL)              |")
    print("|------------------------------------------------------------|")
    print("|                                                            |")
    for u,v,p in menoresCustos:
        print("| Distancia de", u, "para", v, "=", p, "                  ")

def start():

    while(True):
        print("|------------------------------------------------------------|")
        print("|             GRAFOS E ALGORITMOS COMPUTACIONAIS             |")
        print("|------------------------------------------------------------|")
        print("| OBS:todas as entradas dos algoritmos abaixo são atraves de |")
        print("| uma matriz de incidência de um grafo não direcionado.      |")
        print("|------------------------------------------------------------|")
        print("| 1 - Bellman Ford                                           |")
        print("| 2 - Dijkstra                                               |")
        print("| 3 - Kruskal                                                |")
        print("| 4 - Prim                                                   |")
        print("| 5 - Sair                                                   |")
        print("|------------------------------------------------------------|")

        opcao = int(input("| Digite o algoritmo que deseja executar:"))

        if opcao == 1:
            startBellman_Ford()
        elif opcao == 2:
            startDijkstra()
        elif opcao == 3:
            startKruskal()
        elif opcao == 4:
            startPrim()
        elif opcao == 5:
            break
        else:
            print("| Opção invalida!                                            |")

start()

"""
4 3 1 0 0 0 0 0
4 0 0 8 -2 0 0 0
0 0 0 8 0 6 7 0
0 0 1 0 0 0 7 2
0 3 0 0 -2 6 0 2

4 3 1 0 0 0 0 0
4 0 0 8 5 0 0 0
0 0 0 8 0 6 7 0
0 0 1 0 0 0 7 2
0 3 0 0 5 6 0 2

| Distancia de v1 para v1 = 0                   
| Distancia de v1 para v2 = 4                   
| Distancia de v1 para v3 = 8                   
| Distancia de v1 para v4 = 1                   
| Distancia de v1 para v5 = 3         

grafo ={   'v1': {'v2': 4, 'v4': 1, 'v5': 3},
    'v2': {'v1': 4, 'v3': 8, 'v5': 5},
    'v3': {'v2': 8, 'v4': 7, 'v5': 6},
    'v4': {'v1': 1, 'v3': 7, 'v5': 2},
    'v5': {'v1': 3, 'v2': 5, 'v3': 6, 'v4': 2}
    }
grafo1 = [
            [4, 3, 1, 0, 0, 0, 0, 0],
            [4, 0, 0, 8, 5, 0, 0, 0],
            [0, 0, 0, 8, 0, 6, 7, 0],
            [0, 0, 1, 0, 0, 0, 7, 2],
            [0, 3, 0, 0, 5, 6, 0, 2]
        ]
v = ["v1","v2","v3","v4","v5"]
a = ["a1","a2","a3","a4","a5","a6","a7","a8"]

print(arvoreMinimaKruskal(grafo,v))
print(arvoreMinimaPrim(grafo,"v1",v))
print(caminhoBellman_Ford(grafo,"v1"))
print(caminhoDijkstra(grafo,"v1"))"""