import pygame


class TextInput:
    def __init__(self, game, screen, color='white', left=10, top=10, width=50, height=30):
        self.game = game
        self.color = color
        self.screen = screen
        self.width = width
        self.height = height
        self.left = left
        self.top = top
        self.inactive_color = 'gray'

        self.active = False
        self.text = ''
        self.font = pygame.font.Font(None, 80)

    def get_cell(self, mouse_pos):
        x, y = mouse_pos
        if self.left <= x <= (self.left + self.width) and self.top <= y <= (self.top + self.height):
            return True

    def on_click(self):
        self.active = True

    def render(self):
        pygame.draw.rect(self.screen, self.color if self.active else self.inactive_color, (self.left, self.top, self.width, self.height))

        pic_text = self.font.render(self.text, True, (0, 0, 0))
        self.screen.blit(pic_text, (self.left, self.top))

    def get_click(self, mouse_pos):
        if self.get_cell(mouse_pos):
            self.on_click()
        else:
            self.active = False
