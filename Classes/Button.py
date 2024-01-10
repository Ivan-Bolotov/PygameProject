import pygame


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
        self.font = pygame.font.Font(None, 40)
        self.active = False
        self.one_ship, self.two_ship, self.three_ship, self.four_ship = False, False, False, False

        self.types_of_button = {'START': self.start, 'QUIT': self.quit, 'PROFILE': self.profile,
                                'RETURN_TO_START_SCREEN': self.return_to_start_screen, 'ENTER': self.enter}

    def set_view(self, left, top, width, height):
        self.left = left
        self.top = top
        self.width = width
        self.height = height

    def render(self):
        pygame.draw.rect(self.screen, 'black', (self.left, self.top, self.width, self.height))
        btn_rect = pygame.draw.rect(self.screen, self.color, (self.left, self.top, self.width, self.height), 2)
        pic_text = self.font.render(self.text, True, "white")
        text_rect = pic_text.get_rect()
        text_rect.centerx = btn_rect.centerx
        text_rect.centery = btn_rect.centery
        self.screen.blit(pic_text, text_rect)

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
        self.game.running_one = self.game.arrangement
        self.game.checking_one = self.game.arrangement_check

    def quit(self):
        self.game.quit_and_kill_all_processes()

    def profile(self):
        print('profile')

    def return_to_start_screen(self):
        self.game.running_one = self.game.start_screen
        self.game.checking_one = self.game.start_screen_check

    def enter(self):
        pass

    def ship_1(self):
        self.one_ship, self.two_ship, self.three_ship, self.four_ship = True, False, False, False
        print('Нажалась')

    def ship_2(self):
        self.one_ship, self.two_ship, self.three_ship, self.four_ship = False, False, False, False

    def ship_3(self):
        self.one_ship, self.two_ship, self.three_ship, self.four_ship = False, False, False, False

    def ship_4(self):
        self.one_ship, self.two_ship, self.three_ship, self.four_ship = False, False, False, False
