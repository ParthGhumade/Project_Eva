import time
import heapq
import sys
import math
from localisation.localisation_module import VisionEngine as VE
from brain.engine import RobotEngine as RE
from display_app import Display as dsp

engine = RE()
vision = VE()

centerPos = None

# direction is 1 for clockwise and 0 for anti-clockwise
# floorMap = {
# 	10: [0.0, 0.0, [(11, (0.0, 0))]],
# 	11: [0.0, 10.0, [(12, (0.0, 0)), (10, (180.0, 0))]],
# 	12: [0.0, 20.0, [(13, (90.0, 0)), (14, (90.0, 1)), (11, 180.0, 0)]],
# 	13: [-10.0, 20.0, [(12, (180.0, 0))]],
# 	14: [10.0, 20.0, [(12, (90.0, 0)), (15, (90.0, 1))]],
# 	15: [20.0, 20.0, [(14, (180.0, 0))]]
# }
floorMap = {
	10: [0.0, 0.0, [11], (0.0, 0)],
	11: [0.0, 10.0, [12, 10], (0.0, 0)],
	12: [0.0, 20.0, [13, 14, 11], (0.0, 0)],
	13: [-10.0, 20.0, [12], (90, 0)],
	14: [10.0, 20.0, [12, 15], (0.0, 0)],
	15: [20.0, 20.0, [14], (90, 1)]
}

def convertToAdjacencyList(adj):
	adjacencyList = {}
	for i in adj:
		adjacencyList[i] = [(j, math.sqrt((adj[i][0] - adj[j][0])**2+(adj[i][1] - adj[j][1])**2)) for j in adj[i][2]]
	return adjacencyList

floorMapIndexed = convertToAdjacencyList(floorMap)

def searchAlgo(adj, src, target):
	dist = {node: sys.maxsize for node in adj}
	dist[src] = 0
	parents = {node: None for node in adj}
	pq = [(0, src)]

	while pq:
		d, u = heapq.heappop(pq)
		if u == target:
			break
		if d > dist[u]:
			continue
		for v, w in adj[u]:
			if dist[u] + w < dist[v]:
				dist[v] = dist[u] + w
				parents[v] = u
				heapq.heappush(pq, (dist[v], v))

	path = []
	curr = target
	while curr is not None:
		path.append(curr)
		curr = parents[curr]

	return path[::-1]

def move(m1, m2):
	if m2 == -1:
		engine.stop()
	else:
		mark1, mark2 = floorMap[m1], floorMap[m2]
		# consider direction the robot is facing currently (fetched from current pos aruco)
		engine.moveForward(100)
		t_init = time.time()
		while time.time() - t_init < 5 and vision.getLatestMarker()[0] != m2:
			pass
		engine.stop()

def goToDestination(room):
	# i am thinking of a graph to act as a floor-map for navigation
	# it will use djikstra's to get the shortest path in the graph and then to go to the next node (marker) the robot will try to face in that marker's direction and then move forward until it reaches there
	centerPos = vision.getLatestPos()
	(marker, direction) = vision.getLatestMarker()
	path = searchAlgo(floorMapIndexed, marker, 13) # hardcoded for now to test

	t_init = time.time()
	reached = False
	while not reached:
		if time.time() - t_init > 10:
			break
		marker = vision.getLatestMarker()
		if marker[0] == path[-1]:
			reached = True
		
		if not marker[0] in path:
			goToDestination(room)
			break

		counter = 0
		next = -1
		for i in path:
			if i == marker[0]:
				next = path[counter + 1]
			counter += 1

		move(marker[0], next)
	
	engine.stop()
		

def navigate(room):
	# goToLift()
	# callLift()
	# goInsideLift()
	# pressFloor()
	# wait()
	# goOutsideLift()
	goToDestination(room)
	engine.stop()
	# faceDoor()

# while True:
# 	if dsp.isActive():
# 		navigate(dsp.getRoom())

# goToDestination(10)