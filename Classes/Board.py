import pygame


class Board:
    def __init__(self, screen, color='white', left=10, top=10, width=5, height=5, cell_size=30):
        self.color = color
        self.screen = screen
        self.width = width
        self.height = height
        self.left = left
        self.top = top
        self.cell_size = cell_size

        self.board = [[0] * width for _ in range(height)]

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self):
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
        print(pos)
        return pos

    def on_click(self, cell_coords):
        pass

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        if cell:
            self.on_click(cell)