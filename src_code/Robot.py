from Map import MapCellType, Map
import random
from ShortestPathBFS import ShortestPathBFS
from RobotSearchMode import ROBOT_SEARCH_MODE
import numpy as np
#from RobotMap import RobotMap

class Robot:
    avg_rewards = []
    def __init__(self, robot_pos, shared_map, shared_visited, robot_search_mode):
        self.discovered_map = shared_map
        self.visited = shared_visited
        self.movement_stack = []
        self.robot_current_position = robot_pos
        self.displacement_row = [-1, -1, -1, 0, 0, 1, 1, 1]
        self.displacement_col = [-1, 0, 1, -1, 1, -1, 0, 1]
        self.target_found = False
        self.num_steps = 0
        self.other_robots = None
        self.target_position = None
        self.path = None
        self.robot_search_mode = robot_search_mode
        self.dict_elements = None
        self.value = None
        self.states = [1, 4800]
        self.actions = [1, 8]
        self.q_table = np.zeros([4800, 8])
        self.alpha = 0.1
        self.gamma = 0.6
        self.epsilon = 0.1
        self.state = 0
        self.action = 0
        self.block = False
        self.help_states = []
        self.help_actions = []
        self.target_reach = 0
        self.keep_block = False
        self.rewards = []

        if robot_search_mode == ROBOT_SEARCH_MODE.FIND_SHORTEST_PATH:
            self.target_found = False
            for i in range(len(self.discovered_map)):
                for j in range(len(self.discovered_map[i])):
                    if self.discovered_map[i][j] == MapCellType.TARGET:
                        self.target_position = (i, j)
    
    # Depth-first search and Breadth-first search
    def think(self, new_area, robot_pos_in_area):
        #  1. merge new area
        #  2. find empty cell
        #  3. update position
        #  4. add displacement in movement history
        # line below: if target position is globally shared from another robot that has reached the target
        if not self.target_found and self.target_position is not None:
            unknown_cell_found = False
            for i in range(len(self.displacement_row)):
                # line below: storing row position as a result of row displacement
                row = self.robot_current_position[0] + self.displacement_row[i]
                # line below: storing column position as a result of column displacement
                col = self.robot_current_position[1] + self.displacement_col[i]
                # line below: checking if row or col is out of map bounds
                if row < 0 or col < 0 or row >= len(self.discovered_map) or col >= len(self.discovered_map[1]):
                    continue
                # line below: checking if discovered map at index (row, col) is unknown cell
                if MapCellType.UNKNOWN_CELL == self.discovered_map[row][col]:
                    unknown_cell_found = True  # setting boolean unknown_cell_found to True
                    break
            if unknown_cell_found or self.path is None:
                self.merge_area(new_area, robot_pos_in_area)  # calling merge area function
                # line below: calculating new shortest path
                self.path = ShortestPathBFS.get_shortest_path(self.discovered_map, self.robot_current_position,
                                                              self.target_position)
            if self.path is not None:  # if there is a path generated
                if len(self.path) == 1:
                    # if the length of the path is 1 means that the current robot has found the target setting
                    # its target_found boolean to True
                    self.target_found = True

                displacement = self.path[0]  # displacement due to path generated
                self.path.remove(self.path[0])  # remove the used index from the path to get the next displacement

                self.robot_current_position[0] += displacement[0]  # updating the robot_current_position row
                self.robot_current_position[1] += displacement[1]  # updating the robot_current_position column
                # setting the visited boolean matrix of the new robot_current_position (row, col) to True
                self.visited[self.robot_current_position[0]][self.robot_current_position[1]] = True
                # print(self.robot_current_position[0], self.robot_current_position[1])
            else:
                displacement = [0, 0]

        else:  # if target position has not yet been obtained meaning no robot has reached the target yet
            self.merge_area(new_area, robot_pos_in_area)  # calling the merge area function
            # check if target is found
            for i in range(len(self.displacement_row)):
                row = self.robot_current_position[0] + self.displacement_row[i]
                col = self.robot_current_position[1] + self.displacement_col[i]
                if row < 0 or col < 0 or row >= len(self.discovered_map) or col >= len(self.discovered_map[1]):
                    continue
                if MapCellType.TARGET == self.discovered_map[row][col]:
                    self.target_found = True
                    for robot in self.other_robots:
                        robot.received_target_position((row, col))

                    return [self.displacement_row[i], self.displacement_col[i]]

            empty_cell_found = False
            children = []  # initialising child node list

            for i in range(len(self.displacement_row)):
                row = self.robot_current_position[0] + self.displacement_row[i]
                col = self.robot_current_position[1] + self.displacement_col[i]
                if row < 0 or col < 0 or row >= len(self.discovered_map) or col >= len(self.discovered_map[1]):
                    continue
                if (not self.visited[row][col] or self.robot_search_mode == ROBOT_SEARCH_MODE.RANDOM) and \
                        MapCellType.EMPTY == self.discovered_map[row][col]:
                    empty_cell_found = True
                    # line below: adding displacements to children lists after checking that their resulting position
                    # is legal in the lines before
                    children.append([self.displacement_row[i], self.displacement_col[i]])

            if empty_cell_found:  # if cell not visited and empty
                random.shuffle(children)  # random shuffling all legal displacements (randomised depth-first search)
                disp_row, disp_col = children[0]  # choosing the first index (index 0) as the displacement
                row = self.robot_current_position[0] + disp_row  # storing resulting row position
                col = self.robot_current_position[1] + disp_col  # storing resulting column position
                self.robot_current_position = [row, col]  # updating the robot current position to (row, col)
                self.visited[row][col] = True  # setting visited boolean of (row, col) to True
                # line below: adding the negative of the displacement in (row, col) direction to movement stack
                self.movement_stack.append([-disp_row, -disp_col])
                displacement = [disp_row, disp_col]  # to return resulting displacement from the think function

            if not empty_cell_found:  # if cell  not(not visited) and empty
                if len(self.movement_stack) > 0:
                    # line below: backing tracking if there is a dead end, until there isn't. Reason why displacements
                    # were stored as negative in the movement stack (in order for the agent to move back accordingly
                    # to from where it came from until an empty and un-visited cell is found
                    displacement = self.movement_stack.pop()
                # else statement below (last resort case): going to an empty cell even if it is already visited.
                # This case only occurs if the movement stack is empty
                else:
                    empty_cells = []
                    for i in range(len(self.displacement_row)):
                        row = self.robot_current_position[0] + self.displacement_row[i]
                        col = self.robot_current_position[1] + self.displacement_col[i]
                        if row < 0 or col < 0 or row >= len(self.discovered_map) or col >= len(self.discovered_map[1]):
                            continue
                        if MapCellType.EMPTY == self.discovered_map[row][col]:
                            empty_cells.append((self.displacement_row[i], self.displacement_col[i]))

                    rand_index = random.randint(0, len(empty_cells)-1)
                    displacement = empty_cells[rand_index]

                self.robot_current_position[0] += displacement[0]  # updating robot_current_position accordingly
                self.robot_current_position[1] += displacement[1]  # updating robot_current_position accordingly

        self.num_steps += 1  # incrementing number of steps taken
        return displacement
    
    # Reinforcement Learning (Q-learning)
    def think_smart(self, new_area, robot_pos_in_area):
        self.help_actions = []  # emptying actions list each time robot thinks_smart
        self.target_found = False  # setting target_found boolean to False
        self.merge_area(new_area, robot_pos_in_area)  # merging the surrounding area onto global map
        displacement = 0  # initialising displacement to 0
        # line below: combing row and col positions to store position
        position = [self.robot_current_position[0], self.robot_current_position[1]]
        if position not in self.help_states:  # checking if position is not in help_states list
            # line below: adding the position to help_states list
            self.help_states.append([self.robot_current_position[0], self.robot_current_position[1]])
        for action in range(len(self.displacement_row)):  # generating the action space
            disp = [self.displacement_row[action], self.displacement_col[action]]
            self.help_actions.append(disp)  # adding each action to help_actions list

        # command on the line below acquires the index of the highest Q-value of the current state (position) row index
        # in the Q-table, which is the action index
        act_index = np.argmax(self.q_table[self.help_states.index([self.robot_current_position[0],
                                                                   self.robot_current_position[1]])])
        disp_taken = self.help_actions[act_index]  # getting the action using the act_index from the help_actions list
        row_act = disp_taken[0] + self.robot_current_position[0]  # storing the resulting row position of action
        col_act = disp_taken[1] + self.robot_current_position[1]  # storing the resulting column position of action
        post = [row_act, col_act] # combining row and col position to store combined position
        if post not in self.help_states:
            # storing the new resulting position in help_states list to be able to acquire the next_state-allActions
            # max Q-value for the current Q-value equation calculation
            self.help_states.append([row_act, col_act])

        # below is a for loop to check if the target is found in any of the surrounding cells as the due to the action
        # being dependent on the Q-table there is a chance that in the beginning the robot might pass by target and not
        # notice due to the action decision taken based on the Q-table. The chance is very slight to zero as the action
        # towards the target will have the highest reward therefore will be taken however it is better that this is
        # handled
        for i in range(len(self.displacement_row)):
            step_y = self.robot_current_position[0] + self.displacement_row[i]
            step_x = self.robot_current_position[1] + self.displacement_col[i]
            if MapCellType.TARGET == self.discovered_map[step_y][step_x]:
                row_act = step_y
                col_act = step_x

        if MapCellType.BLOCK == self.discovered_map[row_act][col_act]:
            reward = -50  # setting reward in this case to -50
            self.rewards.append(reward)
            # line below: obtaining the next state index value
            next_state = self.help_states.index([self.robot_current_position[0] + disp_taken[0],
                                                 self.robot_current_position[1] + disp_taken[1]])
            # line below: obtaining Q-value of current state-chosenAction from the Q-table
            old_value = self.q_table[self.help_states.index([self.robot_current_position[0],
                                                             self.robot_current_position[1]]),
                                     self.help_actions.index(disp_taken)]
            next_max = np.max(self.q_table[next_state])  # obtaining the next_state - allActions max. Q-value
            # line below: Q-value calculation
            q_value = ((1 - self.alpha) * old_value) + self.alpha * (reward + (self.gamma * next_max))
            # line below: assigning calculated Q-value to the current state of the Q-table
            self.q_table[self.help_states.index([self.robot_current_position[0],
                                                 self.robot_current_position[1]]),
                         self.help_actions.index(disp_taken)] = q_value
            displacement = [0, 0]  # setting the displacement to [0, 0] as the robot should not move onto the block

        elif MapCellType.EMPTY == self.discovered_map[row_act][col_act]:
            reward = -1
            self.rewards.append(reward)
            next_state = self.help_states.index([self.robot_current_position[0] + disp_taken[0],
                                                 self.robot_current_position[1] + disp_taken[1]])
            old_value = self.q_table[self.help_states.index([self.robot_current_position[0],
                                                             self.robot_current_position[1]]),
                                     self.help_actions.index(disp_taken)]
            next_max = np.max(self.q_table[next_state])
            q_value = ((1 - self.alpha) * old_value) + self.alpha * (reward + (self.gamma * next_max))
            self.q_table[self.help_states.index([self.robot_current_position[0],
                                                 self.robot_current_position[1]]),
                         self.help_actions.index(disp_taken)] = q_value
            # line below: setting the displacement to the the chosen displacement from the Q-table on line 159
            displacement = disp_taken
            # line below: incrementing the number of steps only in this condition as this is when the robot moves
            self.num_steps += 1

        elif MapCellType.TARGET == self.discovered_map[row_act][col_act]:
            self.target_found = True  # setting target_found boolean to True
            self.target_reach += 1  # increment target_reach
            print(self.target_reach)
            reward = 100
            self.rewards.append(reward)
            avg_reward = np.sum(self.rewards)/len(self.rewards)
            Robot.avg_rewards.append(avg_reward)
            next_state = self.help_states.index([self.robot_current_position[0] + disp_taken[0],
                                                 self.robot_current_position[1] + disp_taken[1]])
            old_value = self.q_table[self.help_states.index([self.robot_current_position[0],
                                                             self.robot_current_position[1]]),
                                     self.help_actions.index(disp_taken)]
            next_max = np.max(self.q_table[next_state])
            q_value = ((1 - self.alpha) * old_value) + self.alpha * (reward + (self.gamma * next_max))
            self.q_table[self.help_states.index([self.robot_current_position[0],
                                                 self.robot_current_position[1]]),
                         self.help_actions.index(disp_taken)] = q_value
            self.rewards = []
            displacement = [0, 0]

        rowz = self.robot_current_position[0] + displacement[0]  # updating current robot row position accordingly
        colz = self.robot_current_position[1] + displacement[1]  # updating current robot column position accordingly
        self.robot_current_position = [rowz, colz]  # assigning the current robot position to the updated values
        return displacement  # return the resulting displacement


    def received_target_position(self, target_position):
        self.target_position = target_position

    def merge_area(self, new_area, robot_pos_in_area):
        for i, row in enumerate(new_area):
            for j, cell in enumerate(row):
                disp_row = i - robot_pos_in_area[0]
                disp_col = j - robot_pos_in_area[1]

                cell_pos_row = disp_row + self.robot_current_position[0]
                cell_pos_col = disp_col + self.robot_current_position[1]

                if cell_pos_row < 0:
                    for _ in range(abs(cell_pos_row)):
                        self.discovered_map.insert(0, [MapCellType.UNKNOWN_CELL] * len(self.discovered_map[0]))
                        self.robot_current_position[0] += 1
                        self.visited.insert(0, [False] * len(self.visited[0]))

                if cell_pos_col < 0:
                    for _ in range(abs(cell_pos_col)):
                        for disc_map_row, visited_row in zip(self.discovered_map, self.visited):
                            disc_map_row.insert(0, MapCellType.UNKNOWN_CELL)
                            visited_row.insert(0, False)
                        self.robot_current_position[1] += 1

                if cell_pos_row >= len(self.discovered_map):
                    for _ in range(abs(disp_row)):
                        self.discovered_map.append([MapCellType.UNKNOWN_CELL] * len(self.discovered_map[0]))
                        self.visited.append([False] * len(self.visited[0]))

                if cell_pos_col >= len(self.discovered_map[0]):
                    for _ in range(abs(disp_col)):
                        for disc_map_row, visited_row in zip(self.discovered_map, self.visited):
                            visited_row.append(False)
                            disc_map_row.append(MapCellType.UNKNOWN_CELL)

                self.discovered_map[cell_pos_row][cell_pos_col] = cell






























