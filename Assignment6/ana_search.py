from mapping import PriorityQueue
from PIL import Image

class ANAStarSearch:
	def __init__(self, graph, start, goal, mapFile):
		self.graph = graph
		self.start = start
		self.end = goal
		self.preds = {}
		self.h = 0.25
		self.difficulty = mapFile

	def StartSearch(self):
		# Initialize on new search
		self.G = float('inf')
		self.E = float('inf')
		self.g = {}
		self.e = {}
		self.g[self.start] = 0
		self.OPEN = PriorityQueue()
		self.preds = {}
		
		self.e[self.start] = (self.G-self.g[self.start])/self.h
		self.OPEN.put(self.start,self.e[self.start])
		
		while not self.OPEN.empty():
			self.expanded = {}
			self.frontier = {}
			self.frontier.update({self.start:True})
			self.expanded.update({self.start:True})
		
			self.ImproveSolution()
			self.visualize_search()
			newOpen = PriorityQueue()
			while not self.OPEN.empty():
				s = self.OPEN.get()
				if (self.g[s] + self.h < self.G):
					newOpen.put(s,self.e[s])
			self.OPEN = newOpen
		self.visualize_search("out.gif")
	
	def ImproveSolution(self):
		while not self.OPEN.empty():
			s = self.OPEN.get()
			self.expanded.update({s:True})
			self.frontier.update({s:False})

			#if (self.e[s] < self.E):
			#	self.E = self.e[s]
				
			if (s == self.end):
				self.G = self.g[s]
				return
			
			for next in self.graph.neighbors(s):
				self.frontier.update({next:True})
				new_g = self.g[s] + 1 # self.graph.cost(s, next)
				if next not in self.g or new_g < self.g[next]:
					self.g[next] = new_g
					self.preds[next] = s
					if self.g[next] + self.h < self.G:
						self.e[next] = (self.G-self.g[next])/self.h
						self.OPEN.put(next,self.e[next])						
						
	def GetPath(self, reverse = True, addStart = False):
		current = self.end
		path = []
		while current != self.start:
			path.append(current)
			current = self.preds[current]
		if addStart:
			path.append(self.start) # optional
		if reverse:
			path.reverse() # optional
		return path
		
	def visualize_search(self, save_file="do_not_save.png"):
		"""
		:param save_file: (optional) filename to save image to (no filename given means no save file)
		"""
		
		NEON_GREEN = (0, 255, 0)
		PURPLE = (85, 26, 139)
		LIGHT_GRAY = (50, 50, 50)
		DARK_GRAY = (100, 100, 100)
		path = self.GetPath()
		expanded = self.expanded
		frontier = self.frontier
		difficulty = self.difficulty
		start = self.start
		end = self.end
		
		im = Image.open(difficulty).convert("RGB")
		pixel_access = im.load()

		# draw start and end pixels
		pixel_access[start[0], start[1]] = NEON_GREEN
		pixel_access[end[0], end[1]] = NEON_GREEN

		# draw path pixels
		for pixel in path:
			pixel_access[pixel[0], pixel[1]] = PURPLE

		# draw frontier pixels
		for pixel in frontier.keys():
			pixel_access[pixel[0], pixel[1]] = LIGHT_GRAY

		# draw expanded pixels
		for pixel in expanded.keys():
			pixel_access[pixel[0], pixel[1]] = DARK_GRAY

		# display and (maybe) save results
		im.show()
		if(save_file != "do_not_save.png"):
			im.save(save_file)

		im.close()