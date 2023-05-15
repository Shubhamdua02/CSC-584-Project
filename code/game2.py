import pygame
import random
import sys

from cmath import sqrt
import sys
from webbrowser import get
import heapdict
import math

BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
WINDOW_HEIGHT = 400
WINDOW_WIDTH = 400

o1 = [170, 171, 172, 152, 192, 212]
o2 = [344, 345, 346, 325, 365]
o3 = [85, 96]
obstacle_nodes = o1 + o2 + o3

class Sprite(pygame.sprite.Sprite):
    ''' genreal sprite class'''

    def __init__(self, color, height, width):
        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill((0, 0, 0))
        self.image.set_colorkey((0, 0, 0))
        
        self.width = width
        self.height = height
        self.color = color
        pygame.draw.circle(self.image, self.color, (self.width//2, self.height//2), 5)
        self.rect = self.image.get_rect()
        self.rect.x = 5
        self.rect.y = 5
    
    def reset(self):
        self.rect.x = 5 + 19 * 20
        self.rect.y = 5 + 19 * 20
    
    def update(self, x, y):
        self.rect.x = x
        self.rect.y = y

class Player(Sprite):
    '''building the character class'''
    
    def update(self, x, y):
        self.rect.x = x
        self.rect.y = y

def draw_grid(screen):
    blocksize = 20
    obs_c = 1
    for x in range(0, WINDOW_WIDTH, blocksize):
        for y in range(0, WINDOW_HEIGHT, blocksize):
            rect = pygame.Rect(y, x, blocksize, blocksize)
            if obs_c in obstacle_nodes:
                pygame.draw.rect(screen, BLACK, rect)
            else:
                pygame.draw.rect(screen, BLACK, rect, 1)
            obs_c += 1

pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()
screen.fill(WHITE)

all_sprites_list = pygame.sprite.Group()

object_1 = Player(RED, 10, 10)
all_sprites_list.add(object_1)

object_2 = Sprite(GREEN, 10, 10)
object_2.reset()
all_sprites_list.add(object_2)

# ------------------------------------------

no_nodes = 400
search = [None] * (no_nodes + 1)
g = [None] * (no_nodes * no_nodes)
h = [None] * (no_nodes * no_nodes)

pathcost = [None] * (no_nodes * no_nodes)
pathcost[0] = 0
deltah = [None] * (no_nodes * no_nodes)
deltah[0] = 0


open_list = heapdict.heapdict()
tree = {}

file1 = open('graph_test3.txt', 'r')
Lines = file1.readlines()
graph = {}
for line in Lines:
    line = line.strip()
    vals = line.split(" ")
    v1 = float(vals[0])
    v2 = float(vals[1])
    v3 = float(vals[2])
    if v1 not in graph.keys():
        graph[v1] = []
    graph.get(v1).append([v2, v3])

def getH(curr_node, goal_node, mat_dim):
    x1 = math.ceil(curr_node / mat_dim)
    y1 = curr_node % mat_dim
    if y1 == 0:
        y1 = mat_dim
    x2 = math.ceil(goal_node / mat_dim)
    y2 = goal_node % mat_dim
    if y2 == 0:
        y2 = mat_dim
    e_dist = pow((x2 - x1) , 2) + pow((y2 - y1), 2)
    e_dist = sqrt(e_dist)

    return e_dist.real

def initializeState(node, goal_node, mat_dim, counter):
    node = int(node)
    if search[node] != counter and search[node] != 0:
        #print("Initializing II ", node)
        if g[node] + h[node] < pathcost[search[node]]:
            h[node] = pathcost[search[node]] - g[node]
        h[node] = h[node] - (deltah[counter] - deltah[search[node]])
        #h[node] = max(h[node], user_heuristics[node])
        h[node] = max(h[node], getH(node, goal_node, mat_dim))
        g[node] = sys.maxsize
    
    elif search[node] == 0:
        #print("Initializing I", node)
        g[node] = sys.maxsize
        #h[node] = user_heuristics[node]
        h[node] = getH(node, goal_node, mat_dim)
        #print("Initializing I", node, " heursitics ", h[node])
    
    search[node] = counter

def computePath(goal_node, mat_dim, counter):
    goal_node = int(goal_node)
    while g[goal_node] > open_list.peekitem()[1]:
        parent = open_list.popitem()
        #print("goal_g_val ", g[goal_node])
        #print ("at top of list ", parent[0], " f-value ", parent[1])
        parent_node = parent[0] 
        if parent_node in graph.keys():
            children = graph[parent_node]
        else:
            children = []
        for child in children:
            child_node = child[0]
            child_node = int(child_node)
            child_cost = child[1]
            initializeState(child_node, goal_node, mat_dim, counter)
            #print("computing child ", child_node, " from parent ", parent_node)
            if g[child_node] > g[parent_node] + child_cost:
                g[child_node] = g[parent_node] + child_cost
                tree[child_node] = parent_node
                open_list[child_node] = g[child_node] + h[child_node]
                #print("this child has value ", g[child_node] + h[child_node])

# ------------------------------------------


locs = {}
c = 1
for i in range(1, 21):
    for j in range(1, 21):
        x = 5 + ((j - 1) * 20)
        y = 5 + ((i - 1) * 20)
        lst = []
        lst.append(x)
        lst.append(y)
        locs[c] = lst
        c += 1

counter = 1
deltah[1] = 0

start_node = 1
goal_node = 400
mat_dim = 20

for i in range(no_nodes + 1):
    search[i] = 0

random_counter = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    #-------------------------------------
    initializeState(start_node, goal_node, mat_dim, counter)
    initializeState(goal_node, goal_node, mat_dim, counter)
    g[start_node] = 0
    open_list.clear()
    open_list[start_node] = g[start_node] + h[start_node]
    #print ("added to open list", start_node, " value ", g[start_node] + h[start_node])
    computePath(goal_node, mat_dim, counter)
    if len(open_list) == 0:
        pathcost[counter] = sys.maxsize
    else:
        pathcost[counter] = g[goal_node]
    
    '''print(tree)
    print(h)
    print(g)
    print(search)
    print(pathcost)
    print(deltah)'''

    #if counter == 3:
        #break
    
    '''start_node = 3
    new_goal_node = 13

    if counter == 2:
        start_node = 8
        new_goal_node = 9'''
    
    if random_counter > 3:
        rand_pos = random.randint(1, 400)
        while rand_pos in obstacle_nodes:
            rand_pos = random.randint(0, 400)
        new_goal_node = rand_pos
        loc_rand = locs[rand_pos]
        random_counter = 0
        object_2.update(loc_rand[0], loc_rand[1])
    else:
        random_counter += 1
        new_goal_node = goal_node

    if (goal_node != new_goal_node):
        #print ("here")
        #print ("new start, new end", start_node, " ", new_goal_node)
        #for i in range(no_nodes + 1):   search[i] = 0

        initializeState(new_goal_node, goal_node, mat_dim, counter)
        if g[new_goal_node] + h[new_goal_node] < pathcost[counter]:
            h[new_goal_node] = pathcost[counter] - g[new_goal_node]
        deltah[counter + 1] = deltah[counter] + h[new_goal_node]
        goal_node = new_goal_node
    else:
        if counter > (no_nodes * no_nodes) - 1:
            break
        deltah[counter + 1] = deltah[counter]
        #print(counter)
    counter = counter + 1
    #-------------------------------------
    
    stack_path = []
    temp_goal_node = goal_node
    stack_path.append(temp_goal_node)

    while (True):
        n1 = tree[temp_goal_node]
        if (n1 == start_node):
            break
        stack_path.append(n1)
        temp_goal_node = n1
    
    pos = stack_path.pop()

    loc_pos = locs[pos]

    start_node = pos

    if start_node == goal_node:
        sys.exit()

    screen.fill(WHITE)
    draw_grid(screen)
    object_1.update(loc_pos[0], loc_pos[1])
    #object_2.update(loc_rand[0], loc_rand[1])
    all_sprites_list.draw(screen)
    pygame.display.update()
    clock.tick(10)