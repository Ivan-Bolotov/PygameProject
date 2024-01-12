import pygame


class Board:
    def __init__(self, screen, board_type, matrix, color='white', left=10, top=10, width=5, height=5, cell_size=30):
        self.color = color
        self.screen = screen
        self.width = width
        self.height = height
        self.left = left
        self.top = top
        self.cell_size = cell_size
        self.board_type = board_type
        self.matrix = matrix

        self.types = {'ARRANGEMENT': self.arrangement, 'PLAYER_1': self.player_1, 'PLAYER_2': self.player_2}

        self.ship_cords = []

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self):
        pygame.draw.rect(self.screen, 'blue', (self.left, self.top, self.width * self.cell_size,
                                               self.height * self.cell_size))

        for y in range(len(self.matrix)):
            for x in range(len(self.matrix[y])):
                pygame.draw.rect(self.screen, self.color,
                                 (self.left + x * self.cell_size,
                                  self.top + y * self.cell_size,
                                  self.cell_size, self.cell_size), 1)

    def get_cell(self, mouse_pos):
        fk_x, fk_y = mouse_pos
        x = fk_x - self.left
        y = fk_y - self.top
        if x // self.cell_size > self.width - 1 or y // self.cell_size > self.height - 1 or fk_y < self.top \
                or fk_x < self.left:
            return None
        pos = (x // self.cell_size, y // self.cell_size)
        return pos

    def on_click(self, cell_cords):
        self.types[self.board_type](cell_cords)

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        if cell:
            self.on_click(cell)

    def arrangement(self, cell_cords):
        x, y = cell_cords

    def player_1(self):
        pass

    def player_2(self):
        pass
