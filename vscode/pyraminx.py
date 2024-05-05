import heapq
import time
import random

# One posible final state
ONE_FINAL_STATE = '111111111222222222333333333444444444'
################# 'rrrrrrrrrgggggggggbbbbbbbbbyyyyyyyyy'
MOVES = ["U","UInv","L","LInv","R","RInv","F","FInv","u","uInv","l","lInv","r","rInv","f","fInv"]
OPPOSITE_MOVEMENTS = {
    "U":"UInv", "UInv":"U",
    "L":"LInv", "LInv":"L",
    "R":"RInv", "RInv":"R",
    "F":"FInv", "FInv":"F",
    "u":"uInv", "uInv":"u",
    "l":"lInv", "lInv":"l",
    "r":"rInv", "rInv":"r",
    "f":"fInv", "fInv":"f"
}
MOVES_DICTIONARIES = {'u':{0:9,9:18,18:0},
            'l':{4:31,17:4,31:17},
            'f':{8:22,22:35,35:8},
            'r':{27:13,13:26,26:27},
            'U':{19:1,20:2,21:3,1:10,2:11,3:12,10:19,11:20,12:21},
            'L':{1:33,33:15,15:1,5:32,32:16,16:5,6:28,28:12,12:6},
            'F':{6:19,7:23,3:24,19:30,23:34,24:33,30:6,34:7,33:3},
            'R':{28:24,24:19,19:28,29:25,25:23,23:24,30:21,21:24,24:30}
            }

graphf_path = []
graphf_cost = 0
graphf_counter  = 0
graphf_depth = 0
time_graphf = 0.0
node_counter = 0
max_counter = 0
moves = []


def function_0(x,y):
    return 0

def function_1(x):
    return 1

def function_N(x):
    return -1

#graphSearch
def graph_search(input_state, function_g, function_h, goal_state=ONE_FINAL_STATE, maximum_depth=-1):
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
    start_time = time.time()
    heap = []
    explored = set()
    parent = {}
    parentMove = {}
    cost = {input_state: 0}
    depth = {input_state: 0}
    node_counter = 0  # Count all nodes generated
    max_counter = 0   # Max nodes stored at one time

    # Initialize the heap
    initial_cost = function_h(input_state, goal_state)
    heapq.heappush(heap, (initial_cost, input_state))
    node_counter += 1
    max_counter = max(max_counter, len(heap))

    while heap:
        current_cost, state = heapq.heappop(heap)


        if goalTest(state):
            path = get_path(parent,parentMove, state)
            time_graphf = time.time() - start_time
            graphf_path = path
            print("##################################################################################################")
            for state, move in path:
                print(move)
            print("##################################################################################################")
            graphf_cost = cost[state]
            graphf_counter = len(explored)
            graphf_depth = depth[state]
            return {
                "graphf_path": graphf_path,
                "graphf_cost": graphf_cost,
                "graphf_counter": graphf_counter,
                "graphf_depth": graphf_depth,
                "time_graphf": time_graphf,
                "node_counter": node_counter,
                "max_counter": max_counter,
                "moves": [p[1] for p in path]  # Extracting move info from path tuples
            }

        explored.add(state)
        if maximum_depth == -1 or depth[state] < maximum_depth:
            for child, move in getChildren(state):
                new_cost = cost[state] + function_g(state)
                if child not in cost or new_cost < cost[child]:
                    cost[child] = new_cost
                    parent[child] = state
                    parentMove[child] = move
                    depth[child] = depth[state] + 1
                    heapq.heappush(heap, (new_cost + function_h(child,goal_state), child))
                    node_counter += 1
                    max_counter = max(max_counter, len(heap))

    # If no path is found
    time_graphf = time.time() - start_time
    return {
        "path": [],
        "cost": float('inf'),
        "time": time_graphf,
        "explored": len(explored),
        "depth": max(depth.values(), default=0),
        "max_heap_size": max_counter
    }


def get_path(parent, parentMove, end_state):
    path = []
    state = end_state
    while state in parent:
        path.append((state, parentMove[state])) 
        state = parent[state]
    path.append((state,"INITIAL")) 
    path.reverse()  
    return path


# function to check the goal state
def goalTest(state):
    return state==ONE_FINAL_STATE


# function to generate all valid children of a certain node
def getChildren(state):
    children = []
    for move in MOVES:
        new_state = apply_move(state,move)
        children.append((new_state,move))
    return children




def apply_move(state, move):
    if move.endswith("Inv"):
        move = move[:-len("Inv")]
        state = apply_move(state,move)
    char_list = list(state)
    move_map = MOVES_DICTIONARIES[move]
    temp_elements = {key: char_list[key] for key in move_map.keys()}
    for key, new_position in move_map.items():
        char_list[new_position] = temp_elements[key]
    return ''.join(char_list)








def bidirectional_graph_search(initial_state, function_g, function_h, goal_state=ONE_FINAL_STATE, maximum_depth=-1):
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
    global max_counterB
    global max_counterF
    start_time = time.time()
    node_counter = 0
    max_counterB = 0
    max_counterF = 0
    # Forward search initialization
    heap_forward = []
    explored_forward = set()
    parent_forward = {}
    parent_move_forward = {}
    cost_forward = {initial_state: 0}
    depth_forward = {initial_state: 0}
    heapq.heappush(heap_forward, (function_h(initial_state,goal_state), initial_state))
    state_f = initial_state
    node_counter = 0  

    # Backward search initialization
    heap_backward = []
    explored_backward = set()
    parent_backward = {}
    parent_move_backward = {}
    cost_backward = {goal_state: 0}
    depth_backward = {goal_state: 0}
    heapq.heappush(heap_backward, (function_h(goal_state,initial_state), goal_state))
    state_b = goal_state

    while heap_forward and heap_backward:
        # Process forward search
        if heap_forward:
            current_cost_f, state_f = heapq.heappop(heap_forward)
            if state_f in explored_backward:
                return reconstruct_path(state_f, parent_forward, parent_backward, start_time, explored_forward, explored_backward, node_counter,depth_forward,depth_backward, parent_move_forward, parent_move_backward)
            process_state(state_f, heap_forward, explored_forward, parent_forward, cost_forward, depth_forward, function_g, function_h, maximum_depth,parent_move_forward,goal_state)
            max_counterF = max(max_counterF, len(heap_forward))

        # Process backward search
        if heap_backward:
            current_cost_b, state_b = heapq.heappop(heap_backward)
            if state_b in explored_forward:
                return reconstruct_path(state_b, parent_forward, parent_backward, start_time, explored_forward, explored_backward, node_counter,depth_forward,depth_backward,parent_move_forward, parent_move_backward)
            process_state(state_b, heap_backward, explored_backward, parent_backward, cost_backward, depth_backward, function_g, function_h, maximum_depth,parent_move_backward,initial_state)
            max_counterB = max(max_counterB, len(heap_backward))

    return {
        "path": [],
        "cost": float('inf'),
        "time": time.time() - start_time,
        "explored": len(explored_forward) + len(explored_backward),
        "node_processed": node_counter  
    }

def process_state(state, heap, explored, parent, cost, depth, function_g, function_h, maximum_depth, parentMove, goal_state):
    global node_counter
    explored.add(state)
    if maximum_depth == -1 or depth[state] < maximum_depth:
        for child, move in getChildren(state):
            new_cost = cost[state] + function_g(state)
            if child not in cost or new_cost < cost[child]:
                cost[child] = new_cost
                parent[child] = state
                parentMove[child] = move
                depth[child] = depth[state] + 1
                heapq.heappush(heap, (new_cost + function_h(child, goal_state), child))
                node_counter += 1
                

def reconstruct_path(meet_state, parent_forward, parent_backward, start_time, explored_forward, explored_backward, node_counter,depth_forward,depth_backward, parentMove_forward, parentMove_backward):
    global time_graphf, graphf_path, graphf_cost, graphf_depth, max_counter, graphf_counter, max_counterB, max_counterF
    time_graphf = time.time() - start_time
    path_forward = get_path(parent_forward, parentMove_forward, meet_state)
    path_backward = get_path(parent_backward,parentMove_backward, meet_state)

    path_backward[-1]=path_forward[-1]

    for i in range(len(path_backward)-1):
        s,m =path_backward[i]
        s1, m1 = path_backward[i+1]
        if m1.endswith("Inv"):
            m1 = m1[:-len("Inv")]
        else:
            m1 = m1 + "Inv"
        path_backward[i] = s, m1
    path_backward.reverse()
    
    total_path = path_forward + path_backward
    length_first = len(total_path)
    i = 0
    while i < len(total_path) - 1:
        if total_path[i+1][1] == OPPOSITE_MOVEMENTS.get(total_path[i][1]):
            del total_path[i:i+2]  # Elimina ambos movimientos opuestos
        else:
            i += 1
    if len(total_path)==length_first: total_path = path_forward[:-1] + path_backward
    graphf_path = total_path
    print("##################################################################################################")
    for state, move in total_path:
        print(move)
    print("##################################################################################################")
    graphf_depth = graphf_cost = len(total_path) - 1
    max_counter = max_counterB + max_counterF
    graphf_counter = len(explored_forward) + len(explored_backward)
    graphf_depth = depth_backward[meet_state] +  depth_forward[meet_state] - 1
    return {
        "graphf_path": graphf_path,
        "graphf_cost": graphf_cost,
        "graphf_counter": graphf_counter,
        "graphf_depth": graphf_depth,
        "time_graphf": time_graphf,
        "node_counter": node_counter,
        "max_counter": max_counter,
        "moves": [p[1] for p in total_path]
        }


#function to initialize manually the pyramix (made just for testing)
def initialize_pyraminx():
    state = ONE_FINAL_STATE
    state = apply_move(state, 'L')  
    print(state)
    state = apply_move(state, 'LInv')
    print(state)
    state = apply_move(state, 'L')  
    print(state)
    return state

#random Initializes the input state
def initialize_pyraminx_randomly():
    num_moves = random.randint(10, 30)  
    state = ONE_FINAL_STATE
    for _ in range(num_moves):
        move = random.choice(MOVES)
        state = apply_move(state, move)  
    return state


def mismatch_heuristic(state, goal_state):
    return sum(1 for x, y in zip(state, goal_state) if x != y)/9



