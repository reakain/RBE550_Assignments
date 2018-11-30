import math, sys, pygame, random
from math import *
from pygame import *

# Reference: https://raw.githubusercontent.com/s880367/RRT/master/rrt.py

"""
Initial code base listed in the reference above. Initial code was single standard RRT using pygame for visualization and touch interaction. Initial code maintained and expanded for bi-directional RRT using a swap on each node addition, and checking for collisions against other node list and goal or initial point. Code then generates node list path and visualizes.
"""


XDIM = 720
YDIM = 500
windowSize = [XDIM, YDIM]
delta = 10.0
GAME_LEVEL = 1
GOAL_RADIUS = 10
MIN_DISTANCE_TO_ADD = 1.0
NUMNODES = 5000
pygame.init()
fpsClock = pygame.time.Clock()
screen = pygame.display.set_mode(windowSize)
white = 255, 255, 255
black = 0, 0, 0
red = 255, 0, 0
green = 0, 255, 0
blue = 0, 0, 255
cyan = 0,180,105


count = 0
rectObs = []

class Node(object):
    def __init__(self, point, parent):
        super(Node, self).__init__()
        self.point = point
        self.parent = parent

def dist(p1,p2):    #distance between two points
    return sqrt((p1[0]-p2[0])*(p1[0]-p2[0])+(p1[1]-p2[1])*(p1[1]-p2[1]))

def point_circle_collision(p1, p2, radius):
    distance = dist(p1,p2)
    if (distance <= radius):
        return True
    return False
	
def point_collision(p1, p2):
	if p1 == p2:
		return True
	return False
	
def step_from_to(p1,p2):
	if dist(p1,p2) < delta:
		return p2
	else:
		theta = atan2(p2[1]-p1[1],p2[0]-p1[0])
		return p1[0] + delta*cos(theta), p1[1] + delta*sin(theta)

def collides(p):    #check if point collides with the obstacle
	for rect in rectObs:
		if rect.collidepoint(p) == True:
			return True
	return False

def get_random_clear():
	while True:
		p = random.random()*XDIM, random.random()*YDIM
		noCollision = collides(p)
		if noCollision == False:
			return p


def init_obstacles(configNum):  #initialized the obstacle
	global rectObs
	rectObs = []
	print("config "+ str(configNum))
	if (configNum == 0):
		rectObs.append(pygame.Rect((XDIM / 2.0 - 50, YDIM / 2.0 - 100),(100,200)))
	if (configNum == 1):
		rectObs.append(pygame.Rect((100,50),(200,150)))
		rectObs.append(pygame.Rect((400,200),(200,100)))
	if (configNum == 2):
		rectObs.append(pygame.Rect((100,50),(200,150)))
	if (configNum == 3):
		rectObs.append(pygame.Rect((100,50),(200,150)))

	for rect in rectObs:
		pygame.draw.rect(screen, black, rect)


def ExpandTree(nodesList, rand):
	foundNext = False
	parentNode = nodesList[0]
	for p in nodesList:
		if dist(p.point,rand) <= dist(parentNode.point,rand):
			newPoint = step_from_to(p.point,rand)
			if collides(newPoint) == False:
				foundNext = True
				parentNode = p
	return (foundNext,parentNode)

def TreeCollision(p,nodesList):
	for node in nodesList:
		if point_circle_collision(p,node.point, GOAL_RADIUS):
			return True
	return False

def isReachedGoal(nodesList,p,rootNode):
	if point_circle_collision(p, rootNode.point, GOAL_RADIUS):
		return True
	elif TreeCollision(p,nodesList):
		return True
	else:
		return False
		
def GetNodePath(lastNode,nodesList,rootNode):
	# Collision occurred at goal or start point
	if point_circle_collision(lastNode.point, rootNode.point, GOAL_RADIUS):
		return lastNode
	# Collision occurred between trees
	else:
		# Draw the node where collision was found
		print(lastNode.point)
		pygame.draw.circle(screen, green, [int(lastNode.point[0]),int(lastNode.point[1])], GOAL_RADIUS)
		
		# Build new node path set for drawing goal path
		# Find the node in the tree that connects to the collision node (lastNode)
		connectNode = GetConnectionNode(lastNode,nodesList)
		# Build "first" point in expanded tree, building out from the collision node
		newNode = Node(connectNode.point,lastNode)
		while connectNode.parent != None:
			connectNode = connectNode.parent
			newNode = Node(connectNode.point, newNode)
		return newNode
				
def GetConnectionNode(lastNode,nodesList):
	for node in nodesList:
		if point_circle_collision(lastNode.point,node.point, GOAL_RADIUS):
			return node

def reset():
	global count
	screen.fill(white)
	init_obstacles(GAME_LEVEL)
	count = 0

def main():
	global count

	initPoseSet = False
	initialPoint = Node(None, None)
	goalPoseSet = False
	goalPoint = Node(None, None)
	currentState = 'init'
	isStartTree = True

	nodes_start = []
	nodes_end = []
	reset()

	while True:
		if currentState == 'init':
			print('goal point not yet set')
			pygame.display.set_caption('Select Starting Point and then Goal Point')
			fpsClock.tick(10)
		elif currentState == 'goalFound':
			currNode = goalNode.parent
			pygame.display.set_caption('Goal Reached')
			print "Goal Reached"


			while currNode.parent != None:
				pygame.draw.line(screen,green,currNode.point,currNode.parent.point)
				currNode = currNode.parent
			optimizePhase = True
		elif currentState == 'optimize':
			fpsClock.tick(0.5)
			pass
		elif currentState == 'buildTree':
			count = count+1
			pygame.display.set_caption('Performing RRT')
			if count < NUMNODES:
				foundNext = False
				while foundNext == False:
					rand = get_random_clear()
					if isStartTree:
						result = ExpandTree(nodes_start,rand)
					else:
						result = ExpandTree(nodes_end,rand)
					
					foundNext = result[0]
					parentNode = result[1]

				newnode_p = step_from_to(parentNode.point,rand)
				newNode = Node(newnode_p, parentNode)

				if isStartTree:
					nodes_start.append(newNode)
					color = red
					nodesList = nodes_end
					rootNode = goalPoint
					isStartTree = False
				else:
					nodes_end.append(newNode)
					color = blue
					nodesList = nodes_start
					rootNode = initialPoint
					isStartTree = True
					
				if isReachedGoal(nodesList,newNode.point,rootNode):
					currentState = 'goalFound'
					goalNode = GetNodePath(newNode, nodesList, rootNode)
				pygame.draw.line(screen,color,parentNode.point,newNode.point)
				
			else:
				print("Ran out of nodes... :(")
				return;

		#handle events
		for e in pygame.event.get():
			if e.type == QUIT or (e.type == KEYUP and e.key == K_ESCAPE):
				sys.exit("Exiting")
			if e.type == MOUSEBUTTONDOWN:
				print('mouse down')
				if currentState == 'init':
					if initPoseSet == False:
						nodes_start = []
						if collides(e.pos) == False:
							print('initiale point set: '+str(e.pos))

							initialPoint = Node(e.pos, None)
							nodes_start.append(initialPoint) # Start in the center
							initPoseSet = True
							pygame.draw.circle(screen, red, initialPoint.point, GOAL_RADIUS)
					elif goalPoseSet == False:
						nodes_end = []
						
						if collides(e.pos) == False:
							print('goal point set: '+str(e.pos))
							
							goalPoint = Node(e.pos,None)
							nodes_end.append(goalPoint)
							goalPoseSet = True
							pygame.draw.circle(screen, blue, goalPoint.point, GOAL_RADIUS)
							currentState = 'buildTree'
				else:
					currentState = 'init'
					initPoseSet = False
					goalPoseSet = False
					reset()

		pygame.display.update()
		fpsClock.tick(10000)



if __name__ == '__main__':
	main()
