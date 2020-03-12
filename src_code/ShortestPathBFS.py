import random
from Map import MapCellType


class ShortestPathBFS:

    @staticmethod   # graph = discovered_map # start_node = robot_current_position # end_node = target_position
    def get_shortest_path(graph, start_node, end_node):
        displacement_row = [-1, -1, -1, 0, 0, 1, 1, 1]
        displacement_col = [-1, 0, 1, -1, 1, -1, 0, 1]
        visited = ShortestPathBFS.init_list(graph, False)  # created a visited 2-D matrix with init_list function
        # line below: initialising queue to start_node, which is robot_current_position as passed in the robot file call
        queue = [start_node]
        visited[start_node[0]][start_node[1]] = True
        # line below: generates a 2-D matrix the size of graph, which is discovered_map as passed in the robot file call
        # using the init_list function that was created for this purpose. This matrix will be used to keep track of the
        # parent_nodes of all child nodes respectively
        path = ShortestPathBFS.init_list(graph)

        while len(queue) > 0:
            parent_current_position = queue[0]  # assigning index 0 of queue to paren_current_position
            queue.remove(queue[0])  # removing index 0 from queue

            if parent_current_position == end_node:  # end node = target position
                return ShortestPathBFS.get_path(path, parent_current_position)  # get path to target (get_path function)

            children = []  # initialise children list for child nodes

            for i in range(len(displacement_row)):
                # line below: store row position as a result of displacement_row[i]
                child_row = displacement_row[i] + parent_current_position[0]
                # line below: store column position as a result of displacement_col[i]
                child_col = displacement_col[i] + parent_current_position[1]

                # condition below: check if the resulting position is legal
                if child_row < 0 or child_col < 0 or child_row >= len(graph) or child_col >= len(graph[0]) \
                        or visited[child_row][child_col] or graph[child_row][child_col] == MapCellType.BLOCK \
                        or graph[child_row][child_col] == MapCellType.ROBOT:
                    continue
                children.append([child_row, child_col])  # if it is legal add (row, col) position to children list

            random.shuffle(children)  # random shuffle children list

            for (child_row, child_col) in children: # iterate over children list
                visited[child_row][child_col] = True  # set visited boolean matrix at index (row, col) to True
                queue.append((child_row, child_col))  # add (row, col) position to queue
                # line below: assign parent_current_position to path matrix at index (row, col)
                path[child_row][child_col] = parent_current_position

    @staticmethod  # list1 = graph = discovered_map
    def init_list(list1, init_val=None):
        ret_list = []
        for i in range(len(list1)):
            list_row = []
            for j in range(len(list1[0])):
                list_row.append(init_val)
            ret_list.append(list_row)
        return ret_list

    @staticmethod
    def get_path(path, pos):  # path matrix is passed in along with pos, which is the target position
        movement_list = []  # movement list initialised
        # loop until there is no more parent_nodes meaning that the start_node (robot position is reached and indeed
        # the robot position does not have any parent nodes as it is the stare so the loop will end
        while pos is not None:
            new_pos = path[pos[0]][pos[1]]  # parent position of current parent position is acquired with path matrix
            if new_pos is None:
                break
            # line below: positions subtracted to get displacement to previous parent
            disp = [pos[0] - new_pos[0], pos[1] - new_pos[1]]
            movement_list.append(disp)  # displacement is added to movement list
            # line below: assigning new_pos obtained to pos to keep acquiring the previous parent_nodes (essentially
            # parents of parents
            pos = new_pos
        return movement_list[::-1]  # reversing the movement list
        # the movement list is reversed as it is initially stored from target to robot position and reversing it
        # will get the path from the robot position to the target which will then be executed








