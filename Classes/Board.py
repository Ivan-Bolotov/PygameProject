import pygame
from Classes.Button import one_ship, two_ship, three_ship, four_ship


class Board:
    def __init__(self, screen, type, color='white', left=10, top=10, width=5, height=5, cell_size=30):
        self.color = color
        self.screen = screen
        self.width = width
        self.height = height
        self.left = left
        self.top = top
        self.cell_size = cell_size
        self.type = type
        self.one_ship = one_ship
        self.two_ship = two_ship
        self.three_ship = three_ship
        self.four_ship = four_ship

        self.types = {'ARRANGEMENT': self.arrangement}

        self.board = [[0] * width for _ in range(height)]

        self.ship_cords = []

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self):
        pygame.draw.rect(self.screen, 'blue', (self.left, self.top, self.width * self.cell_size,
                                               self.height * self.cell_size))

        for y in range(len(self.board)):
            for x in range(len(self.board[y])):
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
        self.types[self.type](cell_cords)

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        if cell:
            self.on_click(cell)

    def arrangement(self, cell_cords):
        x, y = cell_cords
        print('Шедевропеременная, что с тобой не так, скажи абоба')
        if self.one_ship:
            print('Абоба')
            pygame.draw.rect(self.screen, 'green', (self.left + x * self.cell_size,
                                                    self.top + y * self.cell_size,
                                                    self.left + (x + 1) * self.cell_size,
                                                    self.top + (y + 1) * self.cell_size))





