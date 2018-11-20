import math, sys, pygame, random
from math import *
from pygame import *

# Reference: https://raw.githubusercontent.com/s880367/RRT/master/rrt.py


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
blue = 0, 255, 0
green = 0, 0, 255
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


def ExpandTree(parentNode, rand, p):
	if dist(p.point,rand) <= dist(parentNode.point,rand):
		newPoint = step_from_to(p.point,rand)
		if collides(newPoint) == False:
			return True
	return False

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
	if point_circle_collision(lastNode.point, rootNode.point, GOAL_RADIUS):
		return lastNode
	else:
		nodes_path = []
		connectNode = GetConnectionNode(lastNode,nodesList)
		nodes_path.append(Node(connectNode.point,lastNode))
		while connectNode.parent != None:
			connectNode = connectNode.parent
			nodes_path.append(Node(connectNode.point, nodes_path[len(nodes_path)-1]))
		return nodes_path[len(nodes_path)-1]
				
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
				pygame.draw.line(screen,red,currNode.point,currNode.parent.point)
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
						parentNode = nodes_start[0]
						for p in nodes_start:
							if ExpandTree(parentNode,rand,p):
								foundNext = True
								parentNode = p
					else:
						parentNode = nodes_end[0]
						for p in nodes_end:
							if ExpandTree(parentNode,rand,p):
								foundNext = True
								parentNode = p


				newnode = step_from_to(parentNode.point,rand)
				pygame.draw.line(screen,cyan,parentNode.point,newnode)

				if isStartTree:
					nodes_start.append(Node(newnode, parentNode))
					if isReachedGoal(nodes_end,newnode,goalPoint):
						currentState = 'goalFound'
						goalNode = GetNodePath(nodes_start[len(nodes_start)-1], nodes_end, goalPoint)
					isStartTree = False
				else:
					nodes_end.append(Node(newnode, parentNode))
					if isReachedGoal(nodes_start,newnode,initialPoint):
						currentState = 'goalFound'
						goalNode = GetNodePath(nodes_end[len(nodes_end)-1], nodes_start, initialPoint)
					isStartTree = True

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
							pygame.draw.circle(screen, green, goalPoint.point, GOAL_RADIUS)
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
