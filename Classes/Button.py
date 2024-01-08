import pygame
import sys


class Button:
    def __init__(self, game, screen, button_type, color='white', left=10, top=10, width=50, height=30, text='button'):
        self.game = game
        self.text = text
        self.color = color
        self.screen = screen
        self.width = width
        self.height = height
        self.left = left
        self.top = top
        self.button_type = button_type
        self.active = False

        self.types_of_button = {'START': self.start, 'QUIT': self.quit, 'PROFILE': self.profile,
                                'RETURN_TO_START_SCREEN': self.return_to_start_screen, 'ENTER': self.enter}

    def set_view(self, left, top, width, height):
        self.left = left
        self.top = top
        self.width = width
        self.height = height

    def render(self):
        pygame.draw.rect(self.screen, 'black', (self.left, self.top, self.width, self.height))
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
            return True
        return False  # Теперь из основной программы известно, нажата кнопка или нет

    def start(self):
        self.game.running_one = self.game.arrangement
        self.game.checking_one = self.game.arrangement_check

    def quit(self):
        # pygame.quit()
        # sys.exit()
        pass
        # Здесь пусто т.к. выход нужно делать из main.py

    def profile(self):
        print('profile')

    def return_to_start_screen(self):
        self.game.running_one = self.game.start_screen
        self.game.checking_one = self.game.start_screen_check

    def enter(self):
        pass

    def ship_1(self):
        pass

    def ship_2_v(self):
        pass

    def ship_3_v(self):
        pass

    def ship_4_v(self):
        pass

    def ship_2_h(self):
        pass

    def ship_3_h(self):
        pass

    def ship_4_h(self):
        pass
