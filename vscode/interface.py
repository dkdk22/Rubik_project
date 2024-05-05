#!/usr/bin/python3
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox, simpledialog

import rubik2

### Global Variables to store the solution analytics ###
algorithm = None
initialState = None
statepointer = cost = counter = depth = 0
runtime = 0.0
path = []
cutDepth = 0

class InterfaceApp:

    # =============================================================================================================== #
    ###     Build the GUI     ###

    def __init__(self, master=None):

        self._job = None
        self.appFrame = ttk.Frame(master)
        self.appFrame.configure(height=600, width=850)
        self.appFrame.pack(side="top")

        self.mainlabel = ttk.Label(self.appFrame)
        self.mainlabel.configure(
            anchor="center", font="{Forte} 36 {bold}", foreground="#003e3e", justify="center", text="2x2 Rubik's Cube Solver")
        self.mainlabel.place(anchor="center", x=300, y=50)

        self.backbutton = ttk.Button(self.appFrame)
        self.img_backicon = tk.PhotoImage(file="back-icon.png")
        self.backbutton.configure(cursor="hand2", image=self.img_backicon)
        self.backbutton.place(anchor="center", height=80, width=80, x=250, y=500)
        self.backbutton.bind("<ButtonPress>", self.prevSequence)

        self.nextbutton = ttk.Button(self.appFrame)
        self.img_nexticon = tk.PhotoImage(file="next-icon.png")
        self.nextbutton.configure(cursor="hand2", image=self.img_nexticon)
        self.nextbutton.place(anchor="center", height=80, width=80, x=350, y=500)
        self.nextbutton.bind("<ButtonPress>", self.nextSequence)

        self.fastforwardbutton = ttk.Button(self.appFrame)
        self.img_fastforwardicon = tk.PhotoImage(file="fast-forward-icon.png")
        self.fastforwardbutton.configure(cursor="hand2", image=self.img_fastforwardicon)
        self.fastforwardbutton.place(anchor="center", height=80, width=80, x=450, y=500)
        self.fastforwardbutton.bind("<ButtonPress>", self.fastForward)

        self.fastbackwardbutton = ttk.Button(self.appFrame)
        self.img_fastbackwardicon = tk.PhotoImage(file="fast-backward-icon.png")
        self.fastbackwardbutton.configure(cursor="hand2", image=self.img_fastbackwardicon)
        self.fastbackwardbutton.place(anchor="center", height=80, width=80, x=150, y=500)
        self.fastbackwardbutton.bind("<ButtonPress>", self.fastBackward)

        self.stopbutton = ttk.Button(self.appFrame)
        self.img_stopicon = tk.PhotoImage(file="stop.png")
        self.stopbutton.configure(cursor="hand2", image=self.img_stopicon, state='disabled')
        self.stopbutton.place(anchor="center", height=80, width=80, x=550, y=500)
        self.stopbutton.bind("<ButtonPress>", self.stopFastForward)

        self.resetbutton = ttk.Button(self.appFrame)
        self.img_reseticon = tk.PhotoImage(file="reset-icon.png")
        self.resetbutton.configure(cursor="hand2", image=self.img_reseticon, state='disabled')
        self.resetbutton.place(anchor="center", height=80, width=80, x=50, y=500)
        self.resetbutton.bind("<ButtonPress>", self.resetStepCounter)

        self.stepCount = ttk.Label(self.appFrame)
        self.stepCount.configure(anchor="center", background="#d6d6d6",
                                 font="{@Malgun Gothic Semilight} 12 {}", justify="center", text='0 / 0')
        self.stepCount.place(anchor="center", width=200, x=300, y=440)

        self.contributorsbutton = ttk.Button(self.appFrame)
        self.contributorsbutton.configure(cursor="hand2", text='Contributors')
        self.contributorsbutton.place(anchor="n", width=150, x=700, y=510)
        self.contributorsbutton.bind("<ButtonPress>", self.showContributors)

        self.solvebutton = ttk.Button(self.appFrame)
        self.img_solveicon = tk.PhotoImage(file="solve-icon.png")
        self.solvebutton.configure(cursor="hand2", text='Solve', image=self.img_solveicon, compound="top")
        self.solvebutton.place(anchor="s", height=150, width=150, x=700, y=200)
        self.solvebutton.bind("<ButtonPress>", self.solve)

        self.gif_loading = tk.Label(self.appFrame)

        self.algorithmbox = ttk.Combobox(self.appFrame)
        self.algorithmbox.configure(cursor="hand2", state="readonly",
                                    values=('BFS','BFS + Heuristic', 'Bidirectional', 'Bidirectional + Heuristic'))
        self.algorithmbox.place(anchor="center", height=30, width=150, x=700, y=230)
        self.algorithmbox.bind("<<ComboboxSelected>>", self.selectAlgorithm)

        self.algolabel = ttk.Label(self.appFrame)
        self.algolabel.configure(anchor="center", text='   Search\nAlgorithm:')
        self.algolabel.place(anchor="center", x=590, y=229)

        self.analysisbox = ttk.Label(self.appFrame)
        self.analysisbox.configure(anchor="center", text='', background="#d6d6d6", borderwidth=3, relief="sunken")
        self.analysisbox.place(anchor="center", width=170, height=280, x=700, y=440)

        self.enterstatebutton = ttk.Button(self.appFrame)
        self.img_inputicon = tk.PhotoImage(file="input-icon.png")
        self.enterstatebutton.configure(
            cursor="hand2", text='Enter Randomness', image=self.img_inputicon, compound="left")
        self.enterstatebutton.place(anchor="n", width=150, x=700, y=250)
        self.enterstatebutton.bind("<ButtonPress>", self.enterInitialState)

        self.mainwindow = self.appFrame

        self.gif = [tk.PhotoImage(file='loading.gif', format='gif -index %i' % i) for i in range(10)]
#########################################################################################################
        
        
        
        
    def run(self):
        """
        Run the program, display the GUI
        """
        app.displayStateOnGrid("0")
        app.gif_loading.place_forget()
        self.refreshFrame()
        self.mainwindow.after(0, app.refreshGIF, 0)
        self.mainwindow.mainloop()

    # =============================================================================================================== #
    ###     Widget Methods     ###

    @staticmethod
    def refreshGIF(ind):
        """
        Refreshes the loading gif to show the next frame
        """
        frame = app.gif[ind]
        ind = (ind + 1) % 10
        app.gif_loading.configure(image=frame)
        app.appFrame.after(50, app.refreshGIF, ind)

    def prevSequence(self, event=None):
        """
        Displays the previous state on the grid
        """
        global statepointer
        if statepointer > 0:
            self.stopFastForward()
            statepointer -= 1
            self.refreshFrame()

    def nextSequence(self, event=None):
        """
        Displays the next state on the grid
        """
        global statepointer
        if statepointer < len(path) - 1:
            self.stopFastForward()
            statepointer += 1
            self.refreshFrame()

    def solve(self, event=None):
        """
        Function is invoked at pressing the solve button. Solves the puzzle with the given initialState and algorithm
        then gives a suitable response to the user
        """
        global algorithm
        app.gif_loading.place(x=600, y=125, anchor="s")
        if self.readyToSolve():
            msg = 'Algorithm: ' + str(algorithm) + '\nInitial State = ' + str(initialState)
            #messagebox.showinfo('Confirm', msg)
            self.resetGrid()
            self.solveState()
            self.refreshFrame()
        else:
            solvingerror = 'Cannot solve.\n' \
                           'Algorithm in use: ' + str(algorithm) + '\n' \
                                                                   'Initial State   : ' + str(initialState)
            messagebox.showerror('Cannot Solve', solvingerror)
        app.gif_loading.place_forget()

    def enterInitialState(self, event=None):
        """
        Invoked at pressing enter initial state button. Displays a simple dialog box for the user to enter their
        initial state. The state is validated and a suitable response it displayed to the user
        """
        global randomness, statepointer, initialState
        inputState = simpledialog.askstring('Randomness Entry', 'Please enter randomness Number')
        if inputState is not None:
            if self.validateState(inputState):
                randomness = inputState
                initialState = rubik2.randomInitializer(int(randomness))
                self.reset()
                app.displayStateOnGrid(initialState) # canviar esto a cridar al randomness
            else:
                messagebox.showerror('Input Error', 'Invalid number')

    def selectAlgorithm(self, event=None):
        """
        Invoked at activating the algorithms combobox. Associates the chosen value to the global variable 'algorithm'
        """
        global algorithm, cutDepth
        try:
            choice = self.algorithmbox.selection_get()
            self.reset()
            algorithm = choice
            if algorithm in ['DFS (Graph Search)', 'DFS (Backtracking)']:
                cutDepth = int(simpledialog.askstring('Cut depth', 'Please, enter your max depth'))
        except:
            pass

    def fastForward(self, event=None):
        """
        Invoked at pressing fast-forward button. Displays following states in rapid succession until it reaches the
        goal state or until terminated by the stopFastForward() method
        """
        global statepointer
        self.stopFastForward()
        if statepointer < cost:
            app.stopbutton.configure(state='enabled')
            statepointer += 1
            self.refreshFrame()
            ms = 100
            if 100 < cost <= 1000:
                ms = 20
            if cost > 1000:
                ms = 1
            app._job = app.stepCount.after(ms, self.fastForward)
        else:
            self.stopFastForward()

    def fastBackward(self, event=None):
        """
        Invoked at pressing fast-backward button. Displays previous states in rapid succession until it reaches the
        goal state or until terminated by the stopFastForward() method
        """
        global statepointer
        self.stopFastForward()
        if statepointer > 0:
            app.stopbutton.configure(state='enabled')
            statepointer -= 1
            ms = 50
            if cost > 1000:
                ms = 1
            app._job = app.stepCount.after(ms, self.fastBackward)
        else:
            self.stopFastForward()
        self.refreshFrame()

    @staticmethod
    def stopFastForward(event=None):
        """
        Invoked at pressing stop fast-forward/backward button. Stops fast-forward/backward
        """
        if app._job is not None:
            app.stopbutton.configure(state='disabled')
            app.stepCount.after_cancel(app._job)
            app._job = None

    def resetStepCounter(self, event=None):
        """
        Invoked at pressing reset button. Resets the grid to the initial state and the step counter to 0
        """
        global statepointer
        if statepointer > 0:
            self.stopFastForward()
            statepointer = 0
            self.refreshFrame()

    def showContributors(self, event=None):
        """
        Invoked at pressing the contributors button. Displays a message box Containing names and IDs of contributors
        """
        messagebox.showinfo('Contributors', "6744   -   Adham Mohamed Aly\n"
                                            "6905   -   Mohamed Farid Abdelaziz\n"
                                            "7140   -   Yousef Ashraf Kotp\n")

    # =============================================================================================================== #
    ###     Helper Functions     ###

    def displaySearchAnalysis(self, force_display=False):
        """
        Displays the analysis of the search algorithm after execution.
        """
        if self.solved() or force_display is True:
            analytics = 'Analysis of ' + str(algorithm) 
            #+ \ '\ninitial state = ' + str(initialState)
            if force_display:
                analytics += '\n< UNSOLVABLE >'
            analytics += '\n-------------------------------' \
                         '\n' + 'Nodes generated: \n' + str(nodes) + \
                         '\n' + 'Nodes expanded: \n' + str(counter) + \
                         '\n' + 'Max. nodes stored: \n' + str(max_stored) + \
                         '\n' + 'Solution cost: \n' + str(cost) + \
                         '\n' + 'Running Time: \n{0:.2f} s\n'.format(runtime) + \
                         '\n' + str('\n'.join(moves)) 
                             
                         
                         
                          
        else:
            analytics = ''
        app.analysisbox.configure(text=analytics)

    def displayStateOnGrid(self, state):
        """
        Display input state to the grid
        :param state: String representation of the required state
        """
        self.movesLeft = 0
        self.moveCount = None
        self.colors = {'w': 'white', 'b': 'blue', 'o': 'orange', 'g': 'green', 'r': 'red', 'y': 'yellow'}
        self.count = 0
        self.points = {0: 'white', 1: 'white', 2: 'white', 3: 'white', 4: 'red', 5: 'red', 6: 'red', 7: 'red',
                       8: 'green', 9: 'green', 10: 'green', 11: 'green', 12: 'orange', 13: 'orange', 14: 'orange',
                       15: 'orange', 16: 'blue', 17: 'blue', 18: 'blue', 19: 'blue', 20: 'yellow', 21: 'yellow',
                       22: 'yellow', 23: 'yellow'}
        if state!="0":
            if isinstance(state, tuple):
                state = state[0]
            splited = state.split()      
            self.points[0]=self.colors[splited[0][0:1]]
            self.points[1]=self.colors[splited[1][0:1]]
            self.points[2]=self.colors[splited[2][0:1]]
            self.points[3]=self.colors[splited[3][0:1]]
            
            self.points[4]=self.colors[splited[8][0:1]]
            self.points[5]=self.colors[splited[9][0:1]]
            self.points[6]=self.colors[splited[10][0:1]]
            self.points[7]=self.colors[splited[11][0:1]]
            
            self.points[8]=self.colors[splited[12][0:1]]
            self.points[9]=self.colors[splited[13][0:1]]
            self.points[10]=self.colors[splited[14][0:1]]
            self.points[11]=self.colors[splited[15][0:1]]
            
            self.points[12]=self.colors[splited[16][0:1]]
            self.points[13]=self.colors[splited[17][0:1]]
            self.points[14]=self.colors[splited[18][0:1]]
            self.points[15]=self.colors[splited[19][0:1]]
            
            self.points[16]=self.colors[splited[4][0:1]]
            self.points[17]=self.colors[splited[5][0:1]]
            self.points[18]=self.colors[splited[6][0:1]]
            self.points[19]=self.colors[splited[7][0:1]]

            self.points[20]=self.colors[splited[20][0:1]]
            self.points[21]=self.colors[splited[21][0:1]]
            self.points[22]=self.colors[splited[22][0:1]]
            self.points[23]=self.colors[splited[23][0:1]]
        else:
            self.points = {0: 'grey', 1: 'grey', 2: 'grey', 3: 'grey', 4: 'grey', 5: 'grey', 6: 'grey', 7: 'grey',
                       8: 'grey', 9: 'grey', 10: 'grey', 11: 'grey', 12: 'grey', 13: 'grey', 14: 'grey',
                       15: 'grey', 16: 'grey', 17: 'grey', 18: 'grey', 19: 'grey', 20: 'grey', 21: 'grey',
                       22: 'grey', 23: 'grey'}
        
        blueCubeFrame = tk.Frame(self.appFrame, bg='blue', highlightbackground="black", highlightthickness=3)
        blueCubeFrame.place(relx=.1, rely=.4, relheight=.2, relwidth=.2)

        _16 = tk.Frame(blueCubeFrame, bg=self.points[16], highlightbackground="black", highlightthickness=2)
        _16.place(relx=0, rely=0, relheight=.5, relwidth=.5)
        _17 = tk.Frame(blueCubeFrame, bg=self.points[17], highlightbackground="black", highlightthickness=2)
        _17.place(relx=.5, rely=0, relheight=.5, relwidth=.5)
        _18 = tk.Frame(blueCubeFrame, bg=self.points[18], highlightbackground="black", highlightthickness=2)
        _18.place(relx=.5, rely=.5, relheight=.5, relwidth=.5)
        _19 = tk.Frame(blueCubeFrame, bg=self.points[19], highlightbackground="black", highlightthickness=2)
        _19.place(relx=0, rely=0.5, relheight=.5, relwidth=.5)

        whiteCubeFrame = tk.Frame(self.appFrame, bg='white', highlightbackground="black", highlightthickness=3)
        whiteCubeFrame.place(relx=.3, rely=.4, relheight=.2, relwidth=.2)

        _0 = tk.Frame(whiteCubeFrame, bg=self.points[0], highlightbackground="black", highlightthickness=2)
        _0.place(relx=0, rely=0, relheight=.5, relwidth=.5)
        _1 = tk.Frame(whiteCubeFrame, bg=self.points[1], highlightbackground="black", highlightthickness=2)
        _1.place(relx=0.5, rely=0, relheight=.5, relwidth=.5)
        _2 = tk.Frame(whiteCubeFrame, bg=self.points[2], highlightbackground="black", highlightthickness=2)
        _2.place(relx=0.5, rely=0.5, relheight=.5, relwidth=.5)
        _3 = tk.Frame(whiteCubeFrame, bg=self.points[3], highlightbackground="black", highlightthickness=2)
        _3.place(relx=0, rely=0.5, relheight=.5, relwidth=.5)

        greenCubeFrame = tk.Frame(self.appFrame, bg='green', highlightbackground="black", highlightthickness=3)
        greenCubeFrame.place(relx=.5, rely=.4, relheight=.2, relwidth=.2)

        _8 = tk.Frame(greenCubeFrame, bg=self.points[8], highlightbackground="black", highlightthickness=2)
        _8.place(relx=0, rely=0, relheight=.5, relwidth=.5)
        _9 = tk.Frame(greenCubeFrame, bg=self.points[9], highlightbackground="black", highlightthickness=2)
        _9.place(relx=0.5, rely=0, relheight=.5, relwidth=.5)
        _10 = tk.Frame(greenCubeFrame, bg=self.points[10], highlightbackground="black", highlightthickness=2)
        _10.place(relx=0.5, rely=0.5, relheight=.5, relwidth=.5)
        _11 = tk.Frame(greenCubeFrame, bg=self.points[11], highlightbackground="black", highlightthickness=2)
        _11.place(relx=0, rely=0.5, relheight=.5, relwidth=.5)

        yellowCubeFrame = tk.Frame(self.appFrame, bg='yellow', highlightbackground="black", highlightthickness=3)
        yellowCubeFrame.place(relx=.7, rely=.4, relheight=.2, relwidth=.2)

        _20 = tk.Frame(yellowCubeFrame, bg=self.points[20], highlightbackground="black", highlightthickness=2)
        _20.place(relx=0, rely=0, relheight=.5, relwidth=.5)
        _21 = tk.Frame(yellowCubeFrame, bg=self.points[21], highlightbackground="black", highlightthickness=2)
        _21.place(relx=0.5, rely=0, relheight=.5, relwidth=.5)
        _22 = tk.Frame(yellowCubeFrame, bg=self.points[22], highlightbackground="black", highlightthickness=2)
        _22.place(relx=0.5, rely=0.5, relheight=.5, relwidth=.5)
        _23 = tk.Frame(yellowCubeFrame, bg=self.points[23], highlightbackground="black", highlightthickness=2)
        _23.place(relx=0, rely=0.5, relheight=.5, relwidth=.5)

        redCubeFrame = tk.Frame(self.appFrame, bg='red', highlightbackground="black", highlightthickness=3)
        redCubeFrame.place(relx=.3, rely=.2, relheight=.2, relwidth=.2)

        _4 = tk.Frame(redCubeFrame, bg=self.points[4], highlightbackground="black", highlightthickness=2)
        _4.place(relx=0, rely=0, relheight=.5, relwidth=.5)
        _5 = tk.Frame(redCubeFrame, bg=self.points[5], highlightbackground="black", highlightthickness=2)
        _5.place(relx=0.5, rely=0, relheight=.5, relwidth=.5)
        _6 = tk.Frame(redCubeFrame, bg=self.points[6], highlightbackground="black", highlightthickness=2)
        _6.place(relx=0.5, rely=0.5, relheight=.5, relwidth=.5)
        _7 = tk.Frame(redCubeFrame, bg=self.points[7], highlightbackground="black", highlightthickness=2)
        _7.place(relx=0, rely=0.5, relheight=.5, relwidth=.5)

        orangeCubeFrame = tk.Frame(self.appFrame, bg='orange', highlightbackground="black", highlightthickness=3)
        orangeCubeFrame.place(relx=.3, rely=.6, relheight=.2, relwidth=.2)

        _12 = tk.Frame(orangeCubeFrame, bg=self.points[12], highlightbackground="black", highlightthickness=2)
        _12.place(relx=0, rely=0, relheight=.5, relwidth=.5)
        _13 = tk.Frame(orangeCubeFrame, bg=self.points[13], highlightbackground="black", highlightthickness=2)
        _13.place(relx=0.5, rely=0, relheight=.5, relwidth=.5)
        _14 = tk.Frame(orangeCubeFrame, bg=self.points[14], highlightbackground="black", highlightthickness=2)
        _14.place(relx=0.5, rely=0.5, relheight=.5, relwidth=.5)
        _15 = tk.Frame(orangeCubeFrame, bg=self.points[15], highlightbackground="black", highlightthickness=2)
        _15.place(relx=0, rely=0.5, relheight=.5, relwidth=.5)


        orangeCubeFrame.place(relx=0.05, rely=0.35, relheight=0.16, relwidth=0.14)
        whiteCubeFrame.place(relx=0.20, rely=0.35, relheight=0.16, relwidth=0.14)
        redCubeFrame.place(relx=0.35, rely=0.35, relheight=0.16, relwidth=0.14)
        yellowCubeFrame.place(relx=0.50, rely=0.35, relheight=0.16, relwidth=0.14)
        greenCubeFrame.place(relx=0.20, rely=0.52, relheight=0.16, relwidth=0.14)
        blueCubeFrame.place(relx=0.20, rely=0.18, relheight=0.16, relwidth=0.14)



    @staticmethod
    def readyToSolve():
        """
        Checks if current state is ready to be solved by checking if the global variables 'initialState' and
        'algorithm' are not None
        :return: boolean
        """
        return initialState is not None and algorithm is not None

    @staticmethod
    def solved():
        """
        Checks if there is a solution registered in the global variables
        :return: boolean
        """
        return len(path) > 0

    @staticmethod
    def solveState():
        """
        Solves the puzzle with 'initialState' and the chosen 'algorithm'. Assumes the current state is ready to solve.
        """
    
        global path, cost, counter, depth, runtime, nodes, max_stored, memory_rep, moves
        if str(algorithm) == 'BFS':
            rubik2.graph_search(rubik2.initializer(),rubik2.function_1,rubik2.function_0)
            path, cost, counter, depth, runtime, nodes, max_stored, moves = \
                rubik2.graphf_path, rubik2.graphf_cost, rubik2.graphf_counter, rubik2.graphf_depth, rubik2.time_graphf, rubik2.node_counter, rubik2.max_counter, rubik2.moves
        elif str(algorithm) == 'BFS + Heuristic':
            rubik2.graph_search(initialState,rubik2.function_1,rubik2.mismatch_heuristic)
            path, cost, counter, depth, runtime, nodes, max_stored, moves = \
                rubik2.graphf_path, rubik2.graphf_cost, rubik2.graphf_counter, rubik2.graphf_depth, rubik2.time_graphf, rubik2.node_counter, rubik2.max_counter, rubik2.moves
        elif str(algorithm) == 'Bidirectional':
            rubik2.bidirectional_graph_search(initialState,rubik2.function_1,rubik2.function_0)
            path, cost, counter, depth, runtime, nodes, max_stored, moves = \
                rubik2.graphf_path, rubik2.graphf_cost, rubik2.graphf_counter, rubik2.graphf_depth, rubik2.time_graphf, rubik2.node_counter, rubik2.max_counter, rubik2.moves
        elif str(algorithm) == 'Bidirectional + Heuristic':
            rubik2.bidirectional_graph_search(initialState,rubik2.function_1,rubik2.mismatch_heuristic)
            path, cost, counter, depth, runtime, nodes, max_stored, moves = \
                rubik2.graphf_path, rubik2.graphf_cost, rubik2.graphf_counter, rubik2.graphf_depth, rubik2.time_graphf, rubik2.node_counter, rubik2.max_counter, rubik2.moves
                
    def resetGrid(self):
        """
        Resets the grid and step counter to the initial state
        """
        global statepointer
        statepointer = 0
        self.refreshFrame()
        app.stepCount.configure(text=self.getStepCountString())

    def reset(self):
        """
        Resets global variables and the GUI frame. Removes currently registered solution
        """
        global path, cost, counter, runtime
        cost = counter = 0
        runtime = 0.0
        path = []
        self.resetGrid()
        app.analysisbox.configure(text='')

    @staticmethod
    def getStepCountString():
        """
        Returns string representation of the step count to be displayed on the step-counter
        :return: String
        """
        return str(statepointer) + ' / ' + str(cost)

    @staticmethod
    def refreshFrame():
        """
        Refreshes the frame with all its components: grid, counter, button, etc.
        """
        if cost > 0:
            state = path[statepointer]
            app.displayStateOnGrid(state)
            app.stepCount.configure(text=app.getStepCountString())
            app.displaySearchAnalysis()
        if statepointer == 0:
            app.resetbutton.configure(state='disabled')
            app.backbutton.configure(state='disabled')
            app.fastbackwardbutton.configure(state='disabled')
        else:
            app.resetbutton.configure(state='enabled')
            app.backbutton.configure(state='enabled')
            app.fastbackwardbutton.configure(state='enabled')

        if cost == 0 or statepointer == cost:
            app.fastforwardbutton.configure(state='disabled')
            app.nextbutton.configure(state='disabled')
        else:
            app.fastforwardbutton.configure(state='enabled')
            app.nextbutton.configure(state='enabled')

    @staticmethod
    def validateState(inputState):
        """
        Validates given state
        :param inputState: String representation of state to be validated
        :return: boolean
        """
        seen = []
        if not inputState.isnumeric():
            return False
        return True




if __name__ == "__main__":
    global app
    root = tk.Tk()
    root.title("2x2 Rubik's Cube Solver")
    app = InterfaceApp(root)
    app.run()
