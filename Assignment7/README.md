Requirements to run solutions:
Python 2.7+
pygame

Usage instructions:
python main.py

Click blank space for initial point, then different blank space for goal point.

Trees and points are color-coded:
Start point in red with red tree
Goal point in blue with blue tree
Final path in green. If trees collide to make path, collision point is marked in green.

Optimization is not implemented. Uses base RRT rather than RRT*
Obstacles are hard-coded

Reference: https://raw.githubusercontent.com/s880367/RRT/master/rrt.py
Initial code base listed in the reference above. Initial code was single standard RRT using pygame for visualization and touch interaction. Initial code maintained and expanded for bi-directional RRT using a swap on each node addition, and checking for collisions against other node list and goal or initial point. Code then generates node list path and visualizes.