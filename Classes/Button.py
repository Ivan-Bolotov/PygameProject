import pygame


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

        self.types_of_button = {'START': self.start(), 'QUIT': self.quit(), 'PROFILE': self.profile()}

    def set_view(self, left, top, width, height):
        self.left = left
        self.top = top
        self.width = width
        self.height = height

    def render(self):
        pygame.draw.rect(self.screen, self.color, (self.left, self.top, self.width, self.height), 2)

    def get_click(self, position):
        if all([self.left < position[0] < self.width + self.left,
                self.top < position[1] < self.height + self.top]):
            self.on_click()
        else:
            print(None)

    def on_click(self):
        self.types_of_button[self.button_type]

    def start(self):
        pass

    def quit(self):
        pass

    def profile(self):
        pass

