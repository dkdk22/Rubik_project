import heapq
import time
import random

# One posible final state
ONE_FINAL_STATE = "wbr wrg wgo wob byr brw bwo boy rby ryg rgw rwb gwr gry gyo gow obw owg ogy oyb ygr yrb ybo yog"
    
#Used in getChildren
FRONT_TWIST = {0: 1, 1: 2, 2: 3, 3: 0, 6: 11, 7: 8, 8: 13, 11: 12, 12: 17, 13: 18, 17: 6, 18: 7}
RIGHT_TWIST = {1: 5, 2: 6, 6: 20, 5: 23, 20: 14, 23: 13, 14: 2, 13: 1, 8: 9, 9: 10, 10: 11, 11: 8}
LEFT_TWIST = {0: 12, 3: 15, 12: 22, 15: 21, 22: 4, 21: 7, 4: 0, 7: 3, 16: 17, 17: 18, 18: 19,19: 16}
TOP_TWIST = {4: 5, 5: 6, 6: 7, 7: 4, 1: 17, 0: 16, 17: 21, 16: 20, 21: 9, 20: 8, 9: 1, 8: 0}
BOTTOM_TWIST = {12: 13, 13: 14, 14: 15, 15: 12, 3: 11, 2: 10, 11: 23, 10: 22, 23: 19, 22: 18, 19: 3,18: 2}
BACK_TWIST = {20: 21, 21: 22, 22: 23, 23: 20, 10: 5, 9: 4, 5: 16, 4: 19, 16: 15, 19: 14, 15: 10,14: 9}

# Annotating dictionaries with labels for moves
DICTIONARIES = [
    (FRONT_TWIST, "FRONT_TWIST_"),
    (RIGHT_TWIST, "RIGHT_TWIST_"), 
    (LEFT_TWIST, "LEFT_TWIST_"),
    (TOP_TWIST, "TOP_TWIST_"),
    (BOTTOM_TWIST, "BOTTOM_TWIST_"), 
    (BACK_TWIST,"BACK_TWIST_")
]

OPPOSITE_MOVEMENTS = {
        'FRONT_TWIST_CLOCKWISE': 'FRONT_TWIST_COUNTERCLOCKWISE',
        'FRONT_TWIST_COUNTERCLOCKWISE': 'FRONT_TWIST_CLOCKWISE',
        'FRONT_TWIST_HALF': 'FRONT_TWIST_HALF',
        'RIGHT_TWIST_CLOCKWISE': 'RIGHT_TWIST_COUNTERCLOCKWISE',
        'RIGHT_TWIST_COUNTERCLOCKWISE': 'RIGHT_TWIST_CLOCKWISE',
        'RIGHT_TWIST_HALF': 'RIGHT_TWIST_HALF',
        'LEFT_TWIST_CLOCKWISE': 'LEFT_TWIST_COUNTERCLOCKWISE',
        'LEFT_TWIST_COUNTERCLOCKWISE': 'LEFT_TWIST_CLOCKWISE',
        'LEFT_TWIST_HALF': 'LEFT_TWIST_HALF',
        'TOP_TWIST_CLOCKWISE': 'TOP_TWIST_COUNTERCLOCKWISE',
        'TOP_TWIST_COUNTERCLOCKWISE': 'TOP_TWIST_CLOCKWISE',
        'TOP_TWIST_HALF': 'TOP_TWIST_HALF',
        'BOTTOM_TWIST_CLOCKWISE': 'BOTTOM_TWIST_COUNTERCLOCKWISE',
        'BOTTOM_TWIST_COUNTERCLOCKWISE': 'BOTTOM_TWIST_CLOCKWISE',
        'BOTTOM_TWIST_HALF': 'BOTTOM_TWIST_HALF',
        'BACK_TWIST_CLOCKWISE': 'BACK_TWIST_COUNTERCLOCKWISE',
        'BACK_TWIST_COUNTERCLOCKWISE': 'BACK_TWIST_CLOCKWISE',
        'BACK_TWIST_HALF': 'BACK_TWIST_HALF'
    }


graphf_path = []
graphf_cost = 0
graphf_counter  = 0
graphf_depth = 0
time_graphf = 0.0
node_counter = 0
max_counter = 0
moves = []



#Helper functions
def stringToSet(input_string):
    words = input_string.split()
    return {' '.join(words[i:i+4]) for i in range(0, len(words), 4)}

def setToString(set):
    return ' '.join(set)

def rotate_string(s, times):
    parts = s.split()
    rotation = times % len(parts)
    return ' '.join(parts[-rotation:] + parts[:-rotation])

def rotate_set_strings(original_set):
    return [{rotate_string(s, i) for s in original_set} for i in range(4)]

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
    initial_cost = function_h(input_state,goal_state)
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
                "moves": [p[1] for p in path]
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
    if isinstance(state, tuple):
        state = state[1]  # Return the first element of the tuple(state,move)
    return areEqual(state,ONE_FINAL_STATE)

# function to check if two states are equal
def areEqual(state,second_state):
    state_set = stringToSet(state)
    second_state_set = stringToSet(second_state)
    rotated_states = rotate_set_strings(state_set)
    
    for rotated_set in rotated_states:
        if rotated_set == second_state_set:
            return True
    return False

# function to generate all valid children of a certain node
def getChildren(state):
    children = []
    if isinstance(state, tuple):
        state = state[0]
    for dictionary, move_label in DICTIONARIES:      
        new_state = move(dictionary, state)
        new_state = move(dictionary, new_state)
        children.append((new_state, move_label+"HALF"))
    for dictionary, move_label in DICTIONARIES:      
        new_state = move(dictionary, state)
        children.append((new_state, move_label+"CLOCKWISE"))
    for dictionary, move_label in DICTIONARIES:      
        new_state = move(dictionary, state)
        new_state = move(dictionary, new_state)
        new_state = move(dictionary, new_state)
        children.append((new_state, move_label+"COUNTERCLOCKWISE"))
    return children




# performes a move given a dictionary
def move(dictionary, state):
    words = state.split()
    rearranged_words = words[:]
    for key, value in dictionary.items():
        rearranged_words[key] = words[value]
    rearranged_state = ' '.join(rearranged_words)
    return rearranged_state

#random Initializes the input state
def randomInitializer(x):
    state = ONE_FINAL_STATE
    for _ in range(x):
        choice = random.randint(0,5)  
        dictionary, move_label = DICTIONARIES[choice]  
        state = move(dictionary, state)  
    return state




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
        "node_processed": node_counter  # Return total nodes processed
    }

def process_state(state, heap, explored, parent, cost, depth, function_g, function_h, maximum_depth, parentMove, goal):
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
                heapq.heappush(heap, (new_cost + function_h(child, goal), child))
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
        if m1.endswith("COUNTERCLOCKWISE"):
            m1 = m1[:-len("COUNTERCLOCKWISE")] + "CLOCKWISE"
        elif m1.endswith("CLOCKWISE"):
            m1 = m1[:-len("CLOCKWISE")] + "COUNTERCLOCKWISE"
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

    

def state_to_position_dict(state):
    """Converts a state string to a dictionary of positions keyed by the color."""
    color_positions = {}
    colors = state.split()
    for index, color in enumerate(colors):
        for c in color:
            if c not in color_positions:
                color_positions[c] = []
            color_positions[c].append(index)
    return color_positions

def mismatch_heuristic(state,goal_state):
    """Computes a simplified 'Manhattan-like' heuristic for the Rubik's cube."""
    goal_positions = state_to_position_dict(goal_state)
    current_positions = state_to_position_dict(state)
    heuristic_cost = 0

    # Compute the cost based on color position differences
    for color in current_positions:
        if color in goal_positions:
            # Simple version: count the number of pieces not in place
            heuristic_cost += len(set(current_positions[color]) - set(goal_positions[color]))
    
    return heuristic_cost*3/40

