from Robot import Robot
from Map import MapCellType
import numpy as np
import random
from RobotSearchMode import ROBOT_SEARCH_MODE


class RobotMap:

    def __init__(self, robot_position, world_map, shared_map, shared_visited, robot_search_mode):
        self.robot = Robot([robot_position[0], robot_position[1]], shared_map, shared_visited, robot_search_mode)
        self.robot_current_position_in_world_map = [robot_position[0], robot_position[1]]
        self.world_map = world_map
        self.timestep = 11
        self.TOTAL_WAITING_TIME = 10
        self.stopped = False

    def set_other_robots(self, other_robots):
        self.robot.other_robots = []

        for robot in other_robots:
            if robot == self.robot:
                continue
            else:
                self.robot.other_robots.append(robot)

    def get_robot_area(self, rows=3, cols=3):  # of the 3 by 3 robot map (search area)
        row_start, row_end, col_start, col_end = self.robot_current_position_in_world_map[0]-rows//2, \
                                                self.robot_current_position_in_world_map[0]+rows//2 + 1, \
                                                self.robot_current_position_in_world_map[1]-cols//2, \
                                                self.robot_current_position_in_world_map[1]+rows//2 + 1
        robot_position_in_area = [rows//2, cols//2]  # which is always (1, 1) as the map is [(0, 2),(0, 2)]
        if row_start < 0:
            robot_position_in_area[0] -= abs(row_start)  # to disregard area out of bounds
            row_start = 0
        if col_start < 0:
            robot_position_in_area[1] -= abs(col_start)  # to disregard area out of bounds
            col_start = 0
        if row_end > len(self.world_map.map_cells):  # to disregard area out of bounds
            row_end = len(self.world_map.map_cells)
        if col_end > len(self.world_map.map_cells[0]):  # to disregard area out of bounds
            col_end = len(self.world_map.map_cells[0])

        area = np.array(self.world_map.map_cells)  # storing world map cells information
        area = area[row_start:row_end, col_start:col_end]  # area of robot map with world map information
        return area.tolist(), robot_position_in_area

    def update_robot_position(self):
        if self.timestep <= self.TOTAL_WAITING_TIME:
            self.timestep += 10
            return
        self.timestep = 1
        area, robot_position_in_area = self.get_robot_area()
        # line below: checking if the search mode is Machine Learning
        if self.robot.robot_search_mode == ROBOT_SEARCH_MODE.MACHINE_LEARNING:
            # line below: think(area, robot_position_in_area), think while the position is updated and pass on new areas
            d_row, d_col = self.robot.think_smart(area, robot_position_in_area)

            if self.robot.target_found:  # checking if target_found boolean is true
                if self.robot.target_reach == 300:  # checking number of time the target has been reach is 200
                    self.stopped = True  # stop the robot boolean
                # line below: setting current map cell to Empty on Interface
                self.world_map.set_position(int(self.robot_current_position_in_world_map[0]),
                                            int(self.robot_current_position_in_world_map[1]), MapCellType.EMPTY)
                # line below: choosing random index position in world map row
                self.robot_current_position_in_world_map[0] = random.randint(3, 16)
                # line below: choosing random index position in world map column
                self.robot_current_position_in_world_map[1] = random.randint(3, 16)
                # line below: updating robot row index position in robot class accordingly
                self.robot.robot_current_position[0] = self.robot_current_position_in_world_map[0]
                # line below: updating robot column index position in robot class accordingly
                self.robot.robot_current_position[1] = self.robot_current_position_in_world_map[1]

                # below is while loop checking if new random position is a block or target,
                # keep generating random index position until it is not a block or target
                while self.world_map.map_cells[self.robot_current_position_in_world_map[0]][self.robot_current_position_in_world_map[1]] \
                        == MapCellType.BLOCK or \
                        self.world_map.map_cells[self.robot_current_position_in_world_map[0]][self.robot_current_position_in_world_map[1]] \
                        == MapCellType.TARGET:
                    self.robot_current_position_in_world_map[0] = random.randint(42, 57)
                    self.robot_current_position_in_world_map[1] = random.randint(30, 50)
                    self.robot.robot_current_position[0] = self.robot_current_position_in_world_map[0]
                    self.robot.robot_current_position[1] = self.robot_current_position_in_world_map[1]
                # line below: update robot to the new random position on Interface
                self.world_map.set_position(int(self.robot_current_position_in_world_map[0]),
                                            int(self.robot_current_position_in_world_map[1]), MapCellType.ROBOT)
                self.robot.target_found = False  # setting target_found boolean back to False
                return self.robot.num_steps
            # the below method is how the robot position on the interface will be updated if the target is not found yet
            self.world_map.set_position(int(self.robot_current_position_in_world_map[0]),
                                        int(self.robot_current_position_in_world_map[1]), MapCellType.EMPTY)
            self.robot_current_position_in_world_map[0] += d_row  # position update: d_row from think_smart function
            self.robot_current_position_in_world_map[1] += d_col  # position update: d_col from think_smart function
            self.world_map.set_position(int(self.robot_current_position_in_world_map[0]),
                                        int(self.robot_current_position_in_world_map[1]), MapCellType.ROBOT)
        # line below: Checking if the search mode is Discover_Map (Randomised Depth-First Search)
        elif self.robot.robot_search_mode == ROBOT_SEARCH_MODE.DISCOVER_MAP:
            # line below: think while the position is updated and pass on new robot map area
            d_row, d_col = self.robot.think(area, robot_position_in_area)
            if self.robot.target_found:
                self.stopped = True
                return self.robot.num_steps
            self.world_map.set_position(int(self.robot_current_position_in_world_map[0]),
                                        int(self.robot_current_position_in_world_map[1]), MapCellType.EMPTY)
            self.robot_current_position_in_world_map[0] += d_row
            self.robot_current_position_in_world_map[1] += d_col
            self.world_map.set_position(int(self.robot_current_position_in_world_map[0]),
                                        int(self.robot_current_position_in_world_map[1]), MapCellType.ROBOT)


