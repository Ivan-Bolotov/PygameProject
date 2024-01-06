import pygame
import sys

class Button:
    def __init__(self, screen, button_type, color='white', left=10, top=10, width=50, height=30, text='button'):
        self.text = text
        self.color = color
        self.screen = screen
        self.width = width
        self.height = height
        self.left = left
        self.top = top
        self.button_type = button_type

        self.types_of_button = {'START': self.start, 'QUIT': self.quit, 'PROFILE': self.profile}

    def set_view(self, left, top, width, height):
        self.left = left
        self.top = top
        self.width = width
        self.height = height

    def render(self):
        pygame.draw.rect(self.screen, self.color, (self.left, self.top, self.width, self.height), 2)

    def get_cell(self, mouse_pos):
        x, y = mouse_pos
        if self.left <= x <= (self.left + self.width) and self.top <= y <= (self.top + self.height):
            return True

    def on_click(self):
        self.types_of_button[self.button_type]()

    def get_click(self, mouse_pos):
        if self.get_cell(mouse_pos):
            self.on_click()

    def start(self):
        game.running_one = game.arrangement()

    def quit(self):
        pygame.quit()
        sys.exit()

    def profile(self):
        print('profile')
