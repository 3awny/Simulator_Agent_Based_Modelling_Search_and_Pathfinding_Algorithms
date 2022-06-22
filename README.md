# Simulator_for_Agent_Based_Modelling_of_Search_and_Pathfinding_Algorithms
Depth-first search, Breadth-first search and Reinforcement Q-learning in the context of 2D Software Robot Agents. I have created my own simulation environment using Pygame.

**HOW-TO**

**1. Starting the software**

- install python 3.8.9
- `python3 venv -m venv` -- create virtual environment named venv
- `source venv/bin/activate` -- activate virtual environment
- `pip install -r requirments.txt` -- install packages
- `python3 run.py`-- starts the software, continue with step 2 below


**2. Choosing the simulation mode**

After the starting the software and the white map can be seen near the bottom of the pygame window, the search mode is originally on “DISCOVER_MAP”, which is the Depth-first search (DFS) and Breadth-first search (BFS) algorithms simulation. In this mode you can generate an obstacle course, by inserting as many blocks as preferred, place * **one** * target and put as many robot agents as preferred. 
To change the search mode to “MACHINE_LEARNING”, press the keyboard key (m). Keep track of shell output after the key is pressed where there will be a print notification of what search mode has changed to. A print with the expression “Robot Search Mode is now MACHINE_LEARNING” should be seen. In this case the environment is ready to simulate reinforcement Q-learning. If the key (m) is pressed again the search mode will change back to “DISCOVER_MAP”, where a print of “Robot Search Mode is now DISCOVER_MAP” should be seen in the shell output. In the “MACHINE_LEARNING” search mode only * **one** * robot agent should be placed in the map, * **one** * target and any number of blocks can be inserted to create the preferred obstacle course.

**3. Choosing the type of cell to insert**

		Cell Type Keyboard Press
			Block  ——>  b
			Target ——>  t
			Robot  ——>  r
			Empty  ——>  e

After the cell type is chosen mouse click on the preferred location of the map (white area) to place the
object. The Block will appear as a black cell, Target as a red cell and Robot as a green cell. Notice keypress (e) is to erase any cell to empty (back to white) e.g. If you want to remove a block, target or robot agent.

**4. Starting the simulation**

Once the search mode is chosen and the map environment is created, the return (Enter) key on the
keyboard should be pressed to start the simulation. Keep track of the output shell as
there will be relevant information displayed there for each search mode.

**5. Once the simulation has ended**

If in the “MACHINE_LEARNING” mode, once the simulation has ended, meaning the robot agent has stopped (after the defined 300 trials, which will be seen counting in the output shell), plotting the learning curve graphs is done by pressing the key (p) on the keyboard and the graphs will pop-up. If in the “DISCOVER_MAP” mode, once the simulation has ended, meaning all robots have reached the target, information of the number of steps taken for each robot to reach the target will be displayed in the output shell. For the last robot, the time taken will also be displayed along with the number of steps. For both modes, if a new simulation is needed, the user must close current pygame window, re-run the “run.py” file and customise a new map environment.
