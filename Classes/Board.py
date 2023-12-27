import pygame


class Board:
    def __init__(self, width, height, cell_size=30):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.left = 10
        self.top = 10
        self.cell_size = cell_size

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        for i in range(self.height):
            for j in range(self.width):
                coords = ((j + 1) * self.cell_size + self.left,
                          (i + 1) * self.cell_size + self.top,
                          self.cell_size, self.cell_size)
                pygame.draw.rect(screen, "white", coords, width=1)

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
        pass

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        if cell:
            self.on_click(cell)
