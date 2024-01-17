import pygame
from Server.Client import Client


class Button:
    def __init__(self, game, screen, button_type, color='white', left=10, top=10, width=50, height=30,
                 text='button', board=None):
        self.game = game
        self.text = text
        self.color = color
        self.screen = screen
        self.width = width
        self.height = height
        self.left = left
        self.top = top
        self.board = board
        self.button_type = button_type
        self.font = pygame.font.Font(None, 40)
        self.active = False

        self.types_of_button = {'START': self.start, 'QUIT': self.quit, 'PROFILE': self.profile,
                                'RETURN_TO_START_SCREEN': self.return_to_start_screen, 'ARR_READY': self.arr_ready,
                                'TEXT_OUT': self.text_out}

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
            pygame.mixer.music.load('Audio/button_sound.mp3')
            pygame.mixer.music.set_volume(0.2)
            pygame.mixer.music.play()
            self.game.start_screen_music_is = False

    def start(self):
        self.game.running_one = self.game.connecting
        self.game.checking_one = self.game.connecting_check

    def quit(self):
        self.game.quit_and_kill_all_processes()

    def profile(self):
        self.game.images_index += 1
        self.game.images_index = self.game.images_index % 4

    def return_to_start_screen(self):
        self.game.running_one = self.game.start_screen
        self.game.checking_one = self.game.start_screen_check

    def arr_ready(self):
        count = 0
        for i in range(-1, 11):
            for j in range(-1, 11):
                if self.board.matrix[i][j] == 1:
                    count += 1
        if count == 20:
            self.text = 'ОЖИДАНИЕ 2-ГО ИГРОКА'
            self.game.arr_ready_1 = True
            for i in range(0, 10):
                for j in range(0, 10):
                    self.game.player_1_board.matrix[i][j] = self.game.board.matrix[i][j]
            self.game.send_message(Client.sendMatrix(self.game.player_1_board.matrix))

        else:
            self.text = 'НЕВЕРНАЯ РАССТАНОВКА'

    def text_out(self):
        pass
