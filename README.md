# Simulator_for_Agent_Based_Modelling_of_Search_and_Pathfinding_Algorithms
Depth-first search, Breadth-first search and Reinforcement Q-learning in the context of 2D Software Robot Agents

How to use the software

1. Running the “run” file

In order to compile the code, download all the .py files and place them into 1 folder. The “run.py” file must be opened in a python editor (IDLE or PyCharm) and pygame, numpy, matplotlib modules must be installed. To start the program, run the “run” file and the pygame window will pop-up displaying the initial map seen in white at the bottom of the window. The rest of the window has been set to “blocks” in black to reduce the size of the map as shown for purposes of shorter simulation times.

2. Choosing the simulation mode

After the running the “run” file and the white map can be seen near the bottom of the pygame window, the search mode is originally on “DISCOVER_MAP”, which is the Depth-first search (DFS) and Breadth-first search (BFS) algorithms simulation. In this mode you can generate an obstacle course, by inserting as many “blocks” as needed, place one target and put as many robot agents as needed. However, to change the search mode to “MACHINE_LEARNING”, the keyboard key (m) must be pressed. Keep track of output terminal shell after the key (m) is pressed where there will be a print of what search mode the system has changed to. A print with the expression “Robot Search Mode is now MACHINE_LEARNING” should be seen, which in this case will be ready to simulate reinforcement learning. If the key (m) is pressed again the search mode will change back to “DISCOVER_MAP”, where a print of “Robot Search Mode is now DISCOVER_MAP” should be seen. In the “MACHINE_LEARNING” search mode only one robot agent should be placed in the map, one “target” and any number of blocks can be inserted to create the preferred obstacle course.

3. Choosing the type of cell to insert

		Cell Type Keyboard Press
			Block  ——>  b
			Target ——>  t
			Robot  ——>  r
			Empty  ——>  e

After the cell type is chosen mouse click on the preferred location of the map (white area) to place the
object. Notice keypress (e) is to erase a any cell to blank e.g. If you want to remove a block, target or robot.

4. Starting the simulation

Once the search mode is chosen and the map environment is created, the (Enter) key on the
keyboard should be pressed to start the simulation. Keep track of the output terminal shell as
there will be relevant information displayed there for each search mode.

5. Once the simulation has ended

If in the “MACHINE_LEARNING” mode, once the simulation has ended, meaning the robot
agent has stopped (after the defined 300 trials), plotting the evidence of learning graphs can be done by pressing the key (p) on the keyboard and the graphs will pop-up. If in the “DISCOVER_MAP” mode, once the simulation has ended, meaning all robots have reached
the target, information of the number of steps taken for each robot to reach the target will be displayed in the output terminal shell. For the last robot, the time taken will also be displayed along with the number of steps. For both modes, if a new simulation is needed, the user must close current pygame window and re-run the “run” file and customise a new map environment.
