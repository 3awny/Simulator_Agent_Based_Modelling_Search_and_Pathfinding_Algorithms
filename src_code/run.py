# importing needed libraries
import os
import pygame
from Map import Map
from Map import MapCellType
from RobotMap import RobotMap
import pickle
from RobotSearchMode import ROBOT_SEARCH_MODE
import time
import matplotlib.pyplot as plt
import numpy as np
from Robot import Robot


class Simulation:
    # initialisations
    def __init__(self, map, w=800, h=600):
        self.map = map
        self.screen = pygame.display.set_mode((w, h))
        self.simulation_started = False
        self.robots = []
        self.robot_search_mode = ROBOT_SEARCH_MODE.DISCOVER_MAP
        self.clock_times = []
        self.start_time_ML = None
        self.start_time_DM = None
        self.clk = False
        self.lst = list(range(80))
        self.lst2 = []
        for i in range(30):
            self.lst2.append(i)
        for j in range(50, 80):
            self.lst2.append(j)
        self.lst3 = list(range(3, 57))
        self.num_steps_reach = 0
        self.lst4 = [17, 18, 19]
        self.lst5 = list(range(3, 20))
        self.lst6 = list(range(0, 42))

    # "draw_map" function below: function that draws cells onto map accordingly
    # the map has been made smaller than the pygame window for to reduce simulation time
    def draw_map(self):
        for i_row, map_row in enumerate(self.map.map_cells):
            for i_col, cell in enumerate(map_row):
                if i_row in self.lst6 and i_col in self.lst:
                    map.set_pixel(i_col*10, i_row*10, MapCellType.BLOCK)
                elif i_row in self.lst3 and i_col in self.lst2:
                    map.set_pixel(i_col*10, i_row*10, MapCellType.BLOCK)
                elif i_row == 57 and i_col in self.lst:
                    map.set_pixel(i_col*10, i_row*10, MapCellType.BLOCK)
                elif i_row == 58 and i_col in self.lst:
                    map.set_pixel(i_col*10, i_row*10, MapCellType.BLOCK)
                elif i_row == 59 and i_col in self.lst:
                    map.set_pixel(i_col*10, i_row*10, MapCellType.BLOCK)
                if cell == MapCellType.BLOCK:
                    color = (0, 0, 0)
                elif cell == MapCellType.EMPTY:
                    color = (255, 255, 255)
                    if self.simulation_started and self.robot_search_mode == ROBOT_SEARCH_MODE.DISCOVER_MAP:
                        if not self.robots[0].robot.visited[i_row][i_col]:
                            color = (130, 130, 130)
                elif cell == MapCellType.ROBOT:
                    color = (0, 255, 0)
                elif cell == MapCellType.TARGET:
                    color = (255, 0, 0)
                rect = pygame.Rect(i_col*cell_size, i_row*cell_size,
                                   cell_size, cell_size)
                pygame.draw.rect(self.screen, color, rect)

    # "run_simulation" function below: contains the while running loop calling most of the functions created in
    # the other files to display effect on interface accordingly
    def run_simulation(self):

        pygame.init()

        clock = pygame.time.Clock()
        running = True
        mode = MapCellType.BLOCK

        self.simulation_started = False

        self.robots = []

        while running:
            # root_window.update()
            pygame_event_list = pygame.event.get()

            for event in pygame_event_list:
                # line below: checking if user quit using the standard "x" button or using escape
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    running = False  # setting running to False if user quit
            if self.simulation_started:  # checking if the simulation has started
                # inside if statement below: to handle machine learning agent
                if self.robot_search_mode == ROBOT_SEARCH_MODE.MACHINE_LEARNING:
                    # inside if statement below: to time machine learning robot agent
                    if self.clk:
                        self.start_time_ML = time.time()
                        self.clk = False
                    # self.start_time = time.time()
                    # line below: for loop to iterate on robot objects (in machine learning case there is only 1
                    for robot in self.robots:
                        # if statement below: checks if robot is stopped to handle what is done after
                        if robot.stopped:
                            x = []
                            for i in range(300):
                                x.append(i)
                            y = self.clock_times
                            y2 = np.array(y)
                            avg_rewards = np.array(Robot.avg_rewards)
                            # inside for loop below: plot graph results with matplotlib upon user pressing "p" key
                            for event in pygame_event_list:
                                if event.type == pygame.KEYDOWN:
                                    if event.key == pygame.K_p:
                                        plt.figure(1)
                                        plt.subplot(211)
                                        plt.plot(x, y2)
                                        plt.xlabel('Number of times the target is reached')
                                        plt.ylabel('Time Taken (Seconds)')
                                        plt.subplot(212)
                                        plt.plot(x, avg_rewards)
                                        plt.xlabel('Number of times the target is reached')
                                        plt.ylabel('Average Reward')
                                        plt.tight_layout()
                                        plt.show()
                            continue
                        # line below: calling function to execute at return number of steps
                        num_steps = robot.update_robot_position()  # while simulation is running update the robot pos.
                        if num_steps is not None:
                            print("Robot found the target after {} steps".format(num_steps))
                            time_since_k = time.time() - self.start_time_ML  # timing robot
                            message = 'Seconds to reach target:' + str(time_since_k)
                            print(message)
                            self.clock_times.append(time_since_k)
                            self.start_time_ML = 0
                            self.start_time_ML = time.time()
                            robot.num_steps = 0
                # inside elif statement below: handline discover_map mode robot agents
                elif self.robot_search_mode == ROBOT_SEARCH_MODE.DISCOVER_MAP:
                    for robot in self.robots:
                        if robot.stopped:
                            continue
                        num_steps = robot.update_robot_position()  # while simulation is running update the robot pos.
                        if num_steps is not None:
                            self.num_steps_reach += 1
                            print("Robot {} found the target after {} steps".format(self.num_steps_reach, num_steps))
                            if self.num_steps_reach == len(self.robots):
                                time_taken = time.time() - self.start_time_DM
                                print("Robot {} reached target after {} seconds".format(self.num_steps_reach, time_taken))

            else:
                # inside for loop below: handling user key presses to change cell types, change robot search mode or to
                # start the simulation
                for event in pygame_event_list:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_b:
                            mode = MapCellType.BLOCK
                        elif event.key == pygame.K_e:
                            mode = MapCellType.EMPTY
                        elif event.key == pygame.K_r:
                            mode = MapCellType.ROBOT
                        elif event.key == pygame.K_t:
                            mode = MapCellType.TARGET
                        elif event.key == pygame.K_s:
                            self.map.save_map()
                        elif event.key == pygame.K_l:
                            self.map.load_map()
                            if os.path.isfile("robot_shared_map.pkl") and os.path.isfile("robot_shared_visited.pkl"):
                                shared_map = pickle.load(open("robot_shared_map.pkl", "rb"))
                                shared_visited = pickle.load(open("robot_shared_visited.pkl", "rb"))
                                for i in range(len(self.map.map_cells)):
                                    for j in range(len(self.map.map_cells[i])):
                                        if shared_map[i][j] == MapCellType.ROBOT:
                                            shared_map[i][j] = MapCellType.EMPTY
                                        if self.map.map_cells[i][j] == MapCellType.ROBOT:
                                            shared_map[i][j] = MapCellType.ROBOT

                                self.init_robot_shared_objects(shared_map, shared_visited,
                                                               ROBOT_SEARCH_MODE.FIND_SHORTEST_PATH)
                        elif event.key == pygame.K_m:
                            if self.robot_search_mode == ROBOT_SEARCH_MODE.MACHINE_LEARNING:
                                self.robot_search_mode = ROBOT_SEARCH_MODE.DISCOVER_MAP
                                print("Robot Search Mode is now DISCOVER_MAP")
                            elif self.robot_search_mode == ROBOT_SEARCH_MODE.DISCOVER_MAP:
                                self.robot_search_mode = ROBOT_SEARCH_MODE.MACHINE_LEARNING
                                print("Robot Search Mode is now MACHINE_LEARNING")
                        elif event.key == pygame.K_RETURN:
                            self.simulation_started = True
                            self.start_time_DM = time.time()
                            self.clk = True

                            self.map.save_map()

                            # inside if statement below: initialising shared_map to unknown and shared_visited to False
                            if len(self.robots) == 0:
                                shared_map = []
                                shared_visited = []
                                for i in range(len(self.map.map_cells)):
                                    shared_map_row = []
                                    shared_visited_row = []
                                    for j in range(len(self.map.map_cells[0])):
                                        shared_map_row.append(MapCellType.UNKNOWN_CELL)
                                        shared_visited_row.append(False)
                                    shared_map.append(shared_map_row)
                                    shared_visited.append(shared_visited_row)

                                self.init_robot_shared_objects(shared_map, shared_visited, self.robot_search_mode)

                # inside if statement below: handling mouse press and setting pixel with cell type chosen (mode)
                if pygame.mouse.get_pressed()[0]:
                    x, y = pygame.mouse.get_pos()
                    self.map.set_pixel(x, y, mode)

            clock.tick(60)
            self.draw_map()
            pygame.display.flip()


        if len(self.robots) > 0:
            robot_shared_map_file = open("robot_shared_map.pkl", "wb")
            robot_shared_visited_file = open("robot_shared_visited.pkl", "wb")
            pickle.dump(self.robots[0].robot.discovered_map, robot_shared_map_file)
            pickle.dump(self.robots[0].robot.visited, robot_shared_visited_file)
            robot_shared_map_file.close()
            robot_shared_visited_file.close()

    # sharing instances with each robot class object
    def init_robot_shared_objects(self, shared_map, shared_visited, robot_search_mode):
        other_robots = []

        for i, row in enumerate(self.map.map_cells):
            for j, cell in enumerate(row):
                if cell == MapCellType.ROBOT:
                    self.robots.append(RobotMap([i, j], self.map, shared_map, shared_visited, robot_search_mode))
                    other_robots.append(self.robots[-1].robot)
                    shared_map[i][j] = MapCellType.EMPTY
                    shared_visited[i][j] = True

        for i in range(len(self.robots)):
            self.robots[i].set_other_robots(other_robots)

# main function is called
if __name__ == '__main__':
    width = 800
    height = 600
    cell_size = 10

    map = Map(height, width, cell_size)
    simulation = Simulation(map, width, height)
    simulation.run_simulation()