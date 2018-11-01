"""
Assignment 3 Path planning

"""
import random	# For generating obstacles

# Generating a point definition
class Vertex:
    def __init__(self,key):
        self.id = key
        self.connectedTo = {}
        self.color = "White"
        self.discoveryTime = 0
        self.finishTime = 0
        self.predId = 0

    def addNeighbor(self,nbr,weight=0):
        self.connectedTo[nbr] = weight

    def __str__(self):
        return str(self.id) + ' connectedTo: ' + str([x.id for x in self.connectedTo])

    def getConnections(self):
        return self.connectedTo.keys()

    def getId(self):
        return self.id

    def getWeight(self,nbr):
        return self.connectedTo[nbr]

    def setColor(self,nbr):
        self.color = nbr

    def getColor(self):
        return self.color

    def setDiscovery(self,nbr):
        self.discoveryTime = nbr

    def getDiscovery(self):
        return self.discoveryTime

    def setFinish(self,nbr):
        self.finishTime = nbr

    def getFinish(self):
        return self.finishTime

    def setPred(self,nbr):
        self.predId = nbr

    def getPred(self):
        return self.predId


# Graph class definition from a list of vertexess and edge connections
class Graph(object):
    def __init__(self):
        self.vertList = {}
        self.numVertices = 0

    def addVertex(self,key):
        self.numVertices = self.numVertices + 1
        newVertex = Vertex(key)
        self.vertList[key] = newVertex
        return newVertex

    def getVertex(self,n):
        if n in self.vertList:
            return self.vertList[n]
        else:
            return None

    def __contains__(self,n):
        return n in self.vertList

    def addEdge(self,f,t,cost=0):
        if f not in self.vertList:
            nv = self.addVertex(f)
        if t not in self.vertList:
            nv = self.addVertex(t)
        self.vertList[f].addNeighbor(self.vertList[t], cost)

    def getVertices(self):
        return self.vertList.keys()

    def __iter__(self):
        return iter(self.vertList.values())

		
# Generate the DFS functional class definition
class DFSGraph(Graph):
    def __init__(self):
        super(DFSGraph, self).__init__()
        self.time = 0
        self.searchStart = 0
        self.searchEnd = 0

    def dfs(self):
        for aVertex in self:
            aVertex.setColor('white')
            aVertex.setPred(-1)
        for aVertex in self:
            if aVertex.getColor() == 'white':
                self.dfsvisit(aVertex)

    def dfsvisit(self,startVertex):
        startVertex.setColor('gray')
        self.time += 1
        startVertex.setDiscovery(self.time)
        for nextVertex in startVertex.getConnections():
            if nextVertex.getColor() == 'white':
                nextVertex.setPred(startVertex)
                self.dfsvisit(nextVertex)
            startVertex.setColor('black')
            self.time += 1
            startVertex.setFinish(self.time)

    def setSearch(self, startVertex, endVertex):
        self.searchStart = self.getVertex(startVertex)
        self.searchEnd = self.getVertex(endVertex)

    def dfsFindPath(self):
        return self.dfsVisitPath(self.searchStart, self.searchEnd)

    def dfsVisitPath(self,startVertex,endVertex,path=[]):
        path = path + [startVertex.getId()]
        if startVertex == endVertex:
            yield path
        for nextVertex in startVertex.getConnections():
            if nextVertex.getId() not in path:
                for new_path in self.dfsVisitPath(nextVertex, endVertex, path):
                    if new_path:
                        yield new_path


# Generate a grid from standard graph class
def gridGraph(gridSize):
    gGraph = Graph()
    for row in range(gridSize):
       for col in range(gridSize):
           nodeId = posToNodeId(row,col,gridSize)
           newPositions = genNeighbors(row,col,gridSize)
           for e in newPositions:
               nid = posToNodeId(e[0],e[1],gridSize)
               gGraph.addEdge(nodeId,nid)
    return gGraph

	
# Generate the DFS graph with blocked points
def blockGridGraph(gridSize, rowBlockNum):
    gGraph = DFSGraph()
    for row in range(gridSize):
        blockCells = random.sample(xrange(1, gridSize-2), rowBlockNum)
        for col in range(gridSize):
            print(col)
            if col not in blockCells:
                nodeId = posToNodeId(row,col,gridSize)
                newPositions = genNeighbors(row,col,gridSize,blockCells)
                for e in newPositions:
                    nid = posToNodeId(e[0],e[1],gridSize)
                    gGraph.addEdge(nodeId,nid)
    return gGraph
	
# Helper functions
def posToNodeId(row, column, gridSize):
    return (row * gridSize) + column

def genNeighbors(x,y,gridSize,blockCells=[]):
    newMoves = []
    moveOffsets = [(-1,0),(0,1),
                   (0,-1),(1,0)]
    for i in moveOffsets:
        newX = x + i[0]
        newY = y + i[1]
        if legalCoord(newX,gridSize,blockCells) and \
                        legalCoord(newY,gridSize,blockCells):
            newMoves.append((newX,newY))
    return newMoves

def legalCoord(x,gridSize,blockCells=[]):
    if x >= 0 and x < gridSize and x not in blockCells:
        return True
    else:
        return False



if __name__ == "__main__":
    try:
        Q_all = blockGridGraph(1000,300)
        print ("Made a graph!")
        print (Q_all.getVertex(0))
        print (Q_all.getVertex(9999))
        Q_all.setSearch(0, 9999)
        for path in (Q_all.dfsFindPath()):
            print(path)
    except BaseException:
        import sys
        print(sys.exc_info()[0])
        import traceback
        print(traceback.format_exc())
    finally:
        print("Press Enter to continue ...")
        input()

