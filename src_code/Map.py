from enum import Enum


class MapCellType(Enum):  # enum created to store cell types
    EMPTY = 1
    BLOCK = 2
    ROBOT = 3
    TARGET = 4
    UNKNOWN_CELL = 5

class Map:
    def __init__(self, height, width, cell_size):
        num_rows = height // cell_size  # dividing window height by selected cell size to get number of rows
        num_cols = width // cell_size  # dividing window width by selected cell size to get number of columns
        self.map_cells = []  # creating a empty list for the map cells
        for i in range(num_rows):  # iterating to create a list of lists
            row = [MapCellType.EMPTY]*num_cols  # each row is initialised EMPTY and length set by NO. of columns value
            self.map_cells.append(row)  # adding each row created to map cells
        self.cell_size = cell_size

    def set_pixel(self, pixel_x, pixel_y, cell_type):
        row = pixel_y//self.cell_size  # to define the position of the cell in the row
        col = pixel_x//self.cell_size  # to define the position of the cell in the column
        self.map_cells[row][col] = cell_type  # setting the cell defined to the selected cell type

    def set_position(self, row, col, cell_type):  # setting the position of the cell with the selected cell type
        self.map_cells[row][col] = cell_type

    def save_map(self, map_path="level.lvl"):  # function to save the map
        with open(map_path, 'w') as fw:
            fw.write(str(self.cell_size) + "\n")
            for map_row in self.map_cells:
                for cell in map_row:
                    fw.write(str(cell.value) + ",")
                fw.write("\n")

    def load_map(self, map_path="level.lvl"):  # function to load the map
        with open(map_path) as fr:
            self.cell_size = int(fr.readline())
            lines = fr.readlines()
        self.map_cells = []
        for line in lines:
            cells_str = line.split(',')
            row_cells = []
            for cell in cells_str:
                if cell == '\n':
                    break
                row_cells.append(MapCellType(int(cell)))
            self.map_cells.append(row_cells)
