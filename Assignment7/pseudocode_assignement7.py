V = {x_init}
E = 0
i = 0
while i < N do:
	G = (V,E)
	x_rand = Sample(i)
	i = i+1
	(V,E) = Extend(G,x_rand)
	
def Extend_RRT(G, x_rand):
	dV = V
	dE = E
	x_nearest = Nearest(G,x)
	x_new = Steer(x_nearest, x)
	if ObstacleFree(x_nearest, x_new) then
		dV = dV U {x_new}
		dE = dE U {(x_nearest, x_new)}
	return dG = (dV, dE)
	
def Extend_RRG(G,x_rand):
	dV = V
	dE = E
	x_nearest = Nearest(G,x)
	x_new = Steer(x_nearest, x)
	if ObstacleFree(x_nearest, x_new) then
		dV = dV U {x_new}
		dE = dE U {(x_nearest, x_new),(x_new,x_nearest)}
		X_near = Near(G,x_new, |V|)
		for all x_near in X_near do:
			if ObstacleFree(x_new,x_near) then:
				dE = dE U {(x_near,x_new),(x_new,x_near)}
	return dG = (dV, dE)
	
def Sample(i):
		return X_free(i)

def Nearest(G,x):
	V = G[1]
	return argmin(v in V) ||x-v||

def Steer(x1, x2):
	return argmin()

def ObstacleFree(x1, x2):
	if [x1,x2] in X_free:
		return true
	else:
		return false

def Near(G,x,V):