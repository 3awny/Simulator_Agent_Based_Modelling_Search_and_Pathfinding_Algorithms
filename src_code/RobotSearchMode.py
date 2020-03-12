from enum import Enum


class ROBOT_SEARCH_MODE(Enum):
    DISCOVER_MAP = 1
    RANDOM = 2
    FIND_SHORTEST_PATH = 3
    MACHINE_LEARNING = 4

    # root_window = tk.Tk()

    # B = tk.button(root_window, text = "Robot", command=lambda: self.SetCellMode(MapCellType.ROBOT))
    # B.pack()
    # B.

    # if self.robot_search_mode == ROBOT_SEARCH_MODE.MACHINE_LEARNING:
    # if i_row in self.lst4 and i_col in self.lst5:
    #    map.set_pixel(i_col*10, i_row*10, MapCellType.BLOCK)
    # if i_row in self.lst5 and i_col in self.lst4:
    #    map.set_pixel(i_col*10, i_row*10, MapCellType.BLOCK)

    # elif i_row == 1 and i_col in self.lst:
    # cell = MapCellType.BLOCK
    #   map.set_pixel(i_col*10, i_row*10, MapCellType.BLOCK)
    # elif i_row == 2 and i_col in self.lst:
    # cell = MapCellType.BLOCK
    #    map.set_pixel(i_col*10, i_row*10, MapCellType.BLOCK)

    # if self.q_table[self.help_states.index([self.robot_current_position[0], self.robot_current_position[1]]), self.help_actions.index(disp_taken)] == 0:

    #check_zero = False
    #if np.max(self.q_table[self.help_states.index([self.robot_current_position[0],
    #                                               self.robot_current_position[1]])]) == 0 and \
    #        np.min(self.q_table[self.help_states.index([self.robot_current_position[0],
    #                                                    self.robot_current_position[1]])]) == 0:
    #    check_zero = True

    #if check_zero:
    #    self.state += 1