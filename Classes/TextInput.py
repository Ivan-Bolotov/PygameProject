import pygame
import sys

class TextInput:
    def __init__(self, game, screen, color='white', left=10, top=10, width=50, height=30):
        self.game = game
        self.color = color
        self.screen = screen
        self.width = width
        self.height = height
        self.left = left
        self.top = top

        self.active = False
        self.text = 'qwe'
        self.font = pygame.font.Font(None, 20)

    def get_cell(self, mouse_pos):
        x, y = mouse_pos
        if self.left <= x <= (self.left + self.width) and self.top <= y <= (self.top + self.height):
            return True

    def on_click(self):
        self.active = True

    def render(self):
        pygame.draw.rect(self.screen, self.color, (self.left, self.top, self.width, self.height))

        print(self.font, self.text, self.font.render(self.text, True, (0, 0, 0)))
        self.text = self.font.render(self.text, True, (0, 0, 0))
        self.screen.blit(self.text, (self.left, self.top))

    def get_click(self, mouse_pos):
        if self.get_cell(mouse_pos):
            self.on_click()
        else:
            self.active = False
