import pygame
from constants import *


class Board:
    def __init__(self, screen, board_type, matrix, color=COLORS.WHITE, left=10, top=10, width=5, height=5,
                 cell_size=30):
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

        self.ship_cords = (None, None)
        self.player_1_clicked = False

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self):
        pygame.draw.rect(self.screen, COLORS.WHITE, (self.left - 1, self.top - 1, self.width * self.cell_size + 2,
                                                     self.height * self.cell_size + 2))
        pygame.draw.rect(self.screen, COLORS.BLUE, (self.left, self.top, self.width * self.cell_size,
                                                    self.height * self.cell_size))
        for y in range(self.height):
            for x in range(self.width):
                if self.board_type != "ARRANGEMENT":
                    if self.board_type == 'PLAYER_1' and self.matrix[y][x] == 1:
                        square_color = COLORS.GREEN
                    elif self.matrix[y][x] == 2:
                        square_color = COLORS.RED
                    elif self.matrix[y][x] == 0:
                        square_color = self.color
                    elif self.matrix[y][x] == 3:
                        square_color = COLORS.BLUE
                    else:
                        square_color = COLORS.WHITE
                else:
                    square_color = COLORS.BLUE
                pygame.draw.rect(self.screen, square_color,
                                 (self.left + x * self.cell_size,
                                  self.top + y * self.cell_size,
                                  self.cell_size, self.cell_size))
                pygame.draw.rect(self.screen, COLORS.GRAY,
                                 (self.left + x * self.cell_size,
                                  self.top + y * self.cell_size,
                                  self.cell_size, self.cell_size), 1)

    def render_1(self):
        pass

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
        pass

    def player_1(self, cell_cords):
        pass

    def player_2(self, cell_cords):
        if self.matrix[cell_cords[1]][cell_cords[0]] == 1:
            self.matrix[cell_cords[1]][cell_cords[0]] = 2
        elif self.matrix[cell_cords[1]][cell_cords[0]] == 0:
            self.matrix[cell_cords[1]][cell_cords[0]] = 3
        self.ship_cords = (cell_cords[0], cell_cords[1])
        self.player_1_clicked = True

    def suffer(self, cords):
        if self.matrix[cords[1]][cords[0]] == 1:
            self.matrix[cords[1]][cords[0]] = 2
        elif self.matrix[cords[1]][cords[0]] == 0:
            self.matrix[cords[1]][cords[0]] = 3
        print(self.matrix)
