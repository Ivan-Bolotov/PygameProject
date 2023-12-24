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
