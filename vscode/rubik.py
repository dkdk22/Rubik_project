import heapq
import time
import random

# Solved state
FINAL_STATE = "wbr wrg wgo wob byr brw bwo boy rby ryg rgw rwb gwr gry gyo gow obw owg ogy oyb ygr yrb ybo yog"

#Used in getChildren
UPWARDS_RIGHT = {0:12, 1:13, 8:11, 9:8, 10:9, 11:10, 4:0, 5:1, 20:4, 21:5, 12:20, 13:21}
UPWARDS_LEFT = {2:14, 3:15, 6:2, 7:3, 22:6, 23:7, 16:17, 17:18, 18:19, 19:16, 14:22, 15:23}
TO_RIGHT_TOP = {0:16, 3:19, 8:0, 11:3, 4:5, 5:6, 6:7, 7:4, 21:11, 22:8, 16:22, 19:21}
TO_RIGHT_BOTTOM = {1:17, 2:18, 9:1, 10:2, 20:10, 23:9, 17:23, 18:20, 12:15, 13:12, 14:13, 15:14}
TURN_FRONT = {0:1, 1:2, 2:3, 3:0, 10:15, 11:12, 5:10, 6:11, 16:5, 17:6, 12:17, 15:16}
TURN_BACK = {8:13, 9:14, 4:9, 7:8, 20:23, 21:20, 22:21, 23:22, 18:7, 19:4, 13:18, 14:19}
DICTIONARIES = [UPWARDS_RIGHT, UPWARDS_LEFT, TO_RIGHT_TOP, TO_RIGHT_BOTTOM, TURN_FRONT, TURN_BACK]

def function_0(x):
    return 0

def function_1(x):
    return 1

def function_N(x):
    return -1

def graphSearch(inputState,function_g,function_h,maximum_depth=-1):
    start_time = time.time()
    #string_state = int(inputState)
    heap = []
    explored = {}
    parent = {}
    cost_map = {}
    heapq.heappush(heap, (function_h(inputState), inputState))
    
    cost_map[inputState] = function_h(inputState)
    heap_map = {}
    heap_map[inputState] = 1
    depth_map ={}
    depth_map[inputState] = 0
    global graphf_counter
    global graphf_path
    global graphf_cost
    global graphf_depth
    global time_graphf
    global node_counter
    global explored_counter
    global heap_counter
    global max_counter
    global open_counter
    global max_rev_counter
    
    explored_counter = 0
    heap_counter = 0
    max_counter = 0
    graphf_depth = 0
    node_counter = 1
    open_counter = 0
    max_rev_counter = 0
    
    while heap:
        node = heapq.heappop(heap)
        state = node[1]
        #string_state = getStringRepresentation(state)
        parent_cost = node[0] - function_h(state)
        #print("Parent cost: ", parent_cost)
        # handling the nodes that was renewed
        if not state in explored:
            graphf_depth = max(parent_cost, graphf_depth)
            explored_counter +=1
            print("explored nodes", explored_counter)
            open_counter -=1
        try:
            heap_map[state] -=1
            heap_counter -=1
            
        except:
            print("Error while exploring")
            
            
        explored[state] = 1
        
        if (explored_counter + heap_counter > max_counter):
            max_counter = explored_counter + heap_counter
            
        if (explored_counter + open_counter > max_rev_counter):
            max_rev_counter = explored_counter + open_counter
            
        if goalTest(state):
            path = getPath(parent, inputState)
            # printPath(path)
            graphf_path = path
            graphf_counter = (len(explored))
            graphf_cost = len(path) - 1
            time_graphf = float(time.time() - start_time)
            print(path)
            return 1
        # generating childeren
        
        if (maximum_depth==-1) or (depth_map[state]<maximum_depth):
        #if True:
            children = getChildren(state)
            for child in children:
                node_counter +=1
                new_cost = function_h(child)             
                
                if (child not in heap_map):# Completely new node
                    heapq.heappush(heap, (parent_cost + new_cost + function_g(0), child))
                    heap_map[child] = 1
                    heap_counter +=1
                    open_counter +=1
                    cost_map[child] = parent_cost + new_cost + function_g(0)
                    parent[child] = state
                    depth_map[child]=depth_map[state]+1
                    graphf_depth = max(depth_map[child], graphf_depth)
                elif (child not in explored):
                    if abs(new_cost + parent_cost + function_g(0)) < abs(cost_map[child]):
                        parent[child] = state
                        cost_map[child] = new_cost + parent_cost + function_g(0)
                        heapq.heappush(heap, (parent_cost + function_g(0) + new_cost, child))
                        depth_map[child]=depth_map[state]+1
                        heap_map[child] += 1
                        heap_counter +=1
                        graphf_depth = max(depth_map[child], graphf_depth)
                        
                else:# Is in the closed list
                    if abs(new_cost + parent_cost + function_g(0)) < abs(cost_map[child]):
                        parent[child] = state
                        cost_map[child] = new_cost + parent_cost + function_g(0)
                        heapq.heappush(heap, (parent_cost + function_g(0) + new_cost, child))
                        depth_map[child]=depth_map[state]+1
                        heap_map[child] = 1
                        heap_counter += 1
                        open_counter += 1
                        graphf_depth = max(depth_map[child], graphf_depth)
                        try:
                            del explored[child]
                            explored_counter -=1
                        except:
                            print('Deleted explored',child)
                        
                            
    graphf_cost = 0
    graphf_path = []
    graphf_counter = (len(explored))
    time_graphf = float(time.time() - start_time)
    return 0


# function to check the goal state
def goalTest(state):
    return state == FINAL_STATE

# function to generate all valid children of a certain node
def getChildren(state):
    children = []
    for dictionary in DICTIONARIES:      
        new_state = move(dictionary, state)
        
        children.append(new_state)
        #for i in range(3):
        #    new_state = state
        #    for _ in range(i+1):
        #        new_state = move(dictionary, new_state)
        #    new_words = new_state
            
        #    children.append(new_words)
    return children

# function to get the path to the goal state
def getPath(parentMap, inputState):
    path = []
    temp = FINAL_STATE
    while temp != inputState:
        path.append(temp)
        temp = parentMap[temp]
    path.append(inputState)
    path.reverse()
    return path

# performes a move given a dictionary
def move(dictionary, state):
    words = state.split()
    rearranged_words = words[:]
    for key, value in dictionary.items():
        rearranged_words[key] = words[value]
    rearranged_state = ' '.join(rearranged_words)
    return rearranged_state

def randomInitializer():
    state = FINAL_STATE
    for i in range(2):
        choice = random.randint(0, 5)
        state = move(DICTIONARIES[choice],state)
    return state
        
graphSearch(randomInitializer(),function_1,function_0)