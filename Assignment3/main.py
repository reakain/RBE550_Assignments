"""
Assignment 3 Path planning

https://eddmann.com/posts/depth-first-search-and-breadth-first-search-in-python/


"""

from pythonds.graphs import Graph

# Python program to print DFS traversal from a 
# given given graph 
from collections import defaultdict 
  
# This class represents a directed graph using 
# adjacency list representation 
class Graph: 
  
    # Constructor 
    def __init__(self): 
  
        # default dictionary to store graph 
        self.graph = defaultdict(list) 
  
    # function to add an edge to graph 
    def addEdge(self,u,v): 
        self.graph[u].append(v) 
  
    # A function used by DFS 
    def DFSUtil(self,v,visited): 
  
        # Mark the current node as visited and print it 
        visited[v]= True
        print v, 
  
        # Recur for all the vertices adjacent to this vertex 
        for i in self.graph[v]: 
            if visited[i] == False: 
                self.DFSUtil(i, visited) 
  
  
    # The function to do DFS traversal. It uses 
    # recursive DFSUtil() 
    def DFS(self,v): 
  
        # Mark all the vertices as not visited 
        visited = [False]*(len(self.graph)) 
  
        # Call the recursive helper function to print 
        # DFS traversal 
        self.DFSUtil(v,visited) 

class DFSGraph(Graph):
	def __init__(self):
		super().__init__()
		self.time = 0

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


def dfs_path(graph, start, goal):
	stack = [(start, [start])]
	while stack:
		(vertex, path) = stack.pop()

		for next in graph[vertex] - set(path):
			if next == goal:
				yield path + [next]
			else:
				stack.append((next, path + [next]))


if __name__ == "__main__"
	# Populate graph 5000x5000
	graph = 
	# Start = graph[0][0]

	# Goal = graph[4999][4999]

	list(dfs_paths(graph, 'A', 'F')) # [['A', 'C', 'F'], ['A', 'B', 'E', 'F']]
