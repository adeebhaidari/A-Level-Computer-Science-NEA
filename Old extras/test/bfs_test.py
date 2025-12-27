import numpy as np

def bfs(maze):
    solution = []
    frontier = []
    visited = []
    costs = 0
    start_node = (1,1)
    goal_node = (19,19)
    frontier.append(start_node)
    visited.append(start_node)

    while frontier:
        selected_node = frontier.pop(0)
        #selected_node = [selected_node[0], selected_node[1]]
        
        if selected_node == goal_node:
            solution.append(selected_node)
            break
        
        solution.append(selected_node)
        
        x,y = selected_node
        
        neighbours = [(x+1,y),
                      (x-1,y),
                      (x,y+1),
                      (x,y-1)]
        
        for nx, ny in neighbours:
            if 0 < nx < 20 and 0 < ny < 20 and maze[nx][ny] == 0 and (nx,ny) not in visited:
                frontier.append((nx,ny))
                visited.append((nx,ny))
        costs += 1
        
    return solution, costs

    

maze = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,1,0,0,0,1,0,0,0,1,0,1,0,0,0,0,0,1],
    [1,0,1,1,0,1,0,1,0,1,0,1,0,1,1,1,1,1,0,1],
    [1,0,1,0,0,1,0,0,0,1,0,0,0,0,0,0,0,1,0,1],
    [1,0,1,0,1,1,1,1,0,1,1,1,1,1,0,1,0,1,0,1],
    [1,0,0,0,1,0,0,1,0,0,0,0,0,1,0,1,0,0,0,1],
    [1,1,1,0,1,0,1,1,1,1,1,1,0,1,0,1,1,1,0,1],
    [1,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0,1,0,1],
    [1,0,1,1,1,1,1,0,1,1,0,1,1,1,1,1,0,1,0,1],
    [1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,1],
    [1,1,1,1,1,1,0,1,1,0,1,1,1,1,0,1,1,1,0,1],
    [1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0,0,1,0,1],
    [1,0,1,1,0,1,1,1,1,1,1,0,1,1,1,1,0,1,0,1],
    [1,0,1,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,1],
    [1,0,1,0,1,1,1,1,0,1,0,1,1,1,0,1,1,1,0,1],
    [1,0,0,0,1,0,0,1,0,0,0,1,0,0,0,0,0,1,0,1],
    [1,1,1,0,1,0,1,1,1,1,1,1,0,1,1,1,0,1,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1],
    [1,0,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
]

coords = [(i,j) for i in range(len(maze)) for j in range(len(maze[0])) if maze[i][j] == 0]
print(coords)
marked = [False for i in range(maze.count(0))]
def bfs2(coords):
    queue = coords
    while queue > 0:
        v = queue.remove(queue[0])
        