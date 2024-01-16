import pygame
from Server.Client import Client


class Board:
    def __init__(self, screen, board_type, matrix, draw_matrix, color='white', left=10, top=10, width=5, height=5,
                 cell_size=30):
        self.draw_matrix = draw_matrix
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
        pygame.draw.rect(self.screen, 'white', (self.left - 1, self.top - 1, self.width * self.cell_size + 2,
                                                self.height * self.cell_size + 2))
        pygame.draw.rect(self.screen, 'blue', (self.left, self.top, self.width * self.cell_size,
                                               self.height * self.cell_size))
        for y in range(len(self.draw_matrix)):
            for x in range(len(self.draw_matrix[y])):
                if self.board_type == 'PLAYER_1':
                    if self.draw_matrix[y][x] == 1:
                        square_color = 'green'
                if self.draw_matrix[y][x] == 2:
                    square_color = 'red'
                elif self.draw_matrix[y][x] == 0:
                    square_color = self.color
                elif self.draw_matrix[y][x] == 3:
                    square_color = 'gray'
                else:
                    square_color = 'white'
                pygame.draw.rect(self.screen, square_color,
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
        pass

    def player_1(self, cell_cords):
        pass

    def player_2(self, cell_cords):
        if self.draw_matrix[cell_cords[1]][cell_cords[0]]:
            self.draw_matrix[cell_cords[1]][cell_cords[0]] = 2
            self.ship_cords = (cell_cords[0], cell_cords[1])
            self.player_1_clicked = True

    def suffer(self, cords):
        if self.draw_matrix[cords[1]][cords[0]] == 1:
            self.draw_matrix[cords[1]][cords[0]] = 2
        elif self.draw_matrix[cords[1]][cords[0]] == 0:
            self.draw_matrix[cords[1]][cords[0]] = 3
