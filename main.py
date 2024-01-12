import sys
import multiprocessing as mp
import websockets as ws
import websockets.sync.client as client
import pygame

from Classes.Board import Board
from Classes.Button import Button
from Classes.TextInput import TextInput


class Game:
    def __init__(self):

        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Морской бой онлайн")

        image = pygame.image.load("Images/upscale_1.jpeg")
        image = pygame.transform.scale(image, self.screen.get_size())
        self.screen.blit(image, (0, 0))

        self.text_image = pygame.image.load('./Images/Sea_Battle_text.png')
        self.text_image = pygame.transform.scale(self.text_image, (400, 155))
        self.text_image_rect = self.text_image.get_rect()
        self.text_image_rect.centerx = self.screen.get_rect().centerx
        self.screen.blit(self.text_image, self.text_image_rect)

        self.label_with_id = (pygame.font.Font(None, 32)
                              .render("Твой ID: " + queue.get().split(":")[1],
                                      False, "#ff9900"))
        self.label_with_id_rect = self.label_with_id.get_rect()
        self.label_with_id_rect.bottom = self.screen.get_rect().bottom - 20
        self.label_with_id_rect.centerx = self.screen.get_rect().centerx
        self.screen.blit(self.label_with_id, self.label_with_id_rect)

        """Основное меню"""
        self.button_quit = Button(self, self.screen, 'QUIT', 'red', text='Выход')
        self.button_quit.set_view(200, 475, 100, 50)
        self.button_start = Button(self, self.screen, 'START', 'orange', text='Старт')
        self.button_start.set_view(350, 475, 100, 50)
        self.button_profile = Button(self, self.screen, 'PROFILE', 'white', text='Профиль')
        self.button_profile.set_view(500, 475, 100, 50)

        """Расстановка кораблей"""
        self.start_positions = Board(self.screen, 'ARRANGEMENT', 'white', 50, 50, 10, 10, 40)

        self.button_remove = Button(self, self.screen, 'REMOVE', 'white', text='Переставить')
        self.button_remove.set_view(150, 500, 50, 50)

        self.g_one_ship_select, self.g_two_ship_select = False, False
        self.g_three_ship_select, self.g_four_ship_select = False, False
        self.v_one_ship_select, self.v_two_ship_select = False, False
        self.v_three_ship_select, self.v_four_ship_select = False, False

        self.v_one_ship_draw, self.v_two_ship_draw = False, False
        self.v_three_ship_draw, self.v_four_ship_draw = False, False
        self.g_one_ship_draw, self.g_two_ship_draw = False, False
        self.g_three_ship_draw, self.g_four_ship_draw = False, False

        self.ready_one_ships, self.ready_two_ships = False, False
        self.ready_three_ships, self.ready_four_ships = False, False

        self.count_one_ships, self.count_two_ships, self.count_three_ships, self.count_four_ships = 4, 3, 2, 1

        self.new_position = None

        self.select_positions = []

        """Ввод ID"""
        self.text_input = TextInput(self, self.screen, 'white', 100, 200, 600, 60)
        self.button_return_to_start_screen = Button(self, self.screen, 'RETURN_TO_START_SCREEN', 'red', text='Вернуться')
        self.button_return_to_start_screen.set_view(200, 475, 100, 50)
        self.button_enter = Button(self, self.screen, 'ENTER', 'green', text='Войти')
        self.button_enter.set_view(500, 475, 100, 50)

        """Запуск стартового окна игры"""
        self.running_one = self.start_screen
        self.checking_one = self.start_screen_check
        self.run()

    def run(self):
        while True:
            self.running_one()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_and_kill_all_processes()

                self.checking_one(event)

            pygame.display.flip()

    def check_in(self):
        pass

    def check_in_check(self):
        pass

    def start_screen(self):
        image = pygame.image.load("Images/upscale_1.jpeg")
        image = pygame.transform.scale(image, self.screen.get_size())
        self.screen.blit(image, (0, 0))
        self.screen.blit(self.text_image, self.text_image_rect)
        self.screen.blit(self.label_with_id, self.label_with_id_rect)

        self.button_start.render()
        self.button_quit.render()
        self.button_profile.render()

    def start_screen_check(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.button_start.get_click(event.pos)
            self.button_profile.get_click(event.pos)
            self.button_quit.get_click(event.pos)

    def arrangement(self):
        image = pygame.image.load("Images/upscale_1.jpeg")
        image = pygame.transform.scale(image, self.screen.get_size())
        self.screen.blit(image, (0, 0))

        self.start_positions.render()
        self.button_remove.render()

        '''Г Четырехпалубные'''

        pygame.draw.rect(self.screen, 'white', (500, 50, 40 * 4, 40))
        if not self.g_four_ship_select:
            pygame.draw.rect(self.screen, 'red', (501, 51, 40 * 4 - 2, 40 - 2))
            if self.g_four_ship_draw and not self.count_four_ships:
                pygame.draw.rect(self.screen, 'red',
                                 (self.start_positions.left + self.new_position[0] * self.start_positions.cell_size + 1,
                                  self.start_positions.top + self.new_position[1] * self.start_positions.cell_size + 1,
                                  40 * 4 - 2, 40 - 2))
        else:
            if self.g_four_ship_draw:
                pygame.draw.rect(self.screen, 'red',
                                 (self.start_positions.left + self.new_position[0] * self.start_positions.cell_size + 1,
                                  self.start_positions.top + self.new_position[1] * self.start_positions.cell_size + 1,
                                  40 * 4 - 2, 40 - 2))
            pygame.draw.rect(self.screen, 'green', (501, 51, 40 * 4 - 2, 40 - 2))

        '''Г Трехпалубные'''

        pygame.draw.rect(self.screen, 'white', (500, 130, 40 * 3, 40))
        if not self.g_three_ship_select:
            pygame.draw.rect(self.screen, 'red', (501, 131, 40 * 3 - 2, 40 - 2))
            if self.g_three_ship_draw and not self.count_three_ships:
                pygame.draw.rect(self.screen, 'red',
                                 (self.start_positions.left + self.new_position[0] * self.start_positions.cell_size + 1,
                                  self.start_positions.top + self.new_position[1] * self.start_positions.cell_size + 1,
                                  40 * 3 - 2, 40 - 2))
        else:
            if self.g_three_ship_draw:
                pygame.draw.rect(self.screen, 'red',
                                 (self.start_positions.left + self.new_position[0] * self.start_positions.cell_size + 1,
                                  self.start_positions.top + self.new_position[1] * self.start_positions.cell_size + 1,
                                  40 * 3 - 2, 40 - 2))
            pygame.draw.rect(self.screen, 'green', (501, 131, 40 * 3 - 2, 40 - 2))

        '''Г Двухпалубные'''

        pygame.draw.rect(self.screen, 'white', (500, 210, 40 * 2, 40))
        if not self.g_two_ship_select:
            pygame.draw.rect(self.screen, 'red', (501, 211, 40 * 2 - 2, 40 - 2))
            if self.g_two_ship_draw and not self.count_two_ships:
                pygame.draw.rect(self.screen, 'red',
                                 (self.start_positions.left + self.new_position[0] * self.start_positions.cell_size + 1,
                                  self.start_positions.top + self.new_position[1] * self.start_positions.cell_size + 1,
                                  40 * 2 - 2, 40 - 2))
        else:
            if self.g_two_ship_draw:
                pygame.draw.rect(self.screen, 'red',
                                 (self.start_positions.left + self.new_position[0] * self.start_positions.cell_size + 1,
                                  self.start_positions.top + self.new_position[1] * self.start_positions.cell_size + 1,
                                  40 * 2 - 2, 40 - 2))
            pygame.draw.rect(self.screen, 'green', (501, 211, 40 * 2 - 2, 40 - 2))

        '''Г Однопалубные'''

        pygame.draw.rect(self.screen, 'white', (500, 290, 40 * 1, 40))
        if not self.g_one_ship_select:
            pygame.draw.rect(self.screen, 'red', (501, 291, 40 * 1 - 2, 40 - 2))
            if self.g_one_ship_draw and not self.count_one_ships:
                pygame.draw.rect(self.screen, 'red',
                                 (self.start_positions.left + self.new_position[0] * self.start_positions.cell_size + 1,
                                  self.start_positions.top + self.new_position[1] * self.start_positions.cell_size + 1,
                                  40 * 1 - 2, 40 - 2))
        else:
            if self.g_one_ship_draw:
                pygame.draw.rect(self.screen, 'red',
                                 (self.start_positions.left + self.new_position[0] * self.start_positions.cell_size + 1,
                                  self.start_positions.top + self.new_position[1] * self.start_positions.cell_size + 1,
                                  40 * 1 - 2, 40 - 2))
            pygame.draw.rect(self.screen, 'green', (501, 291, 40 * 1 - 2, 40 - 2))

        '''В Четырехпалубные'''

        pygame.draw.rect(self.screen, 'white', (500, 370, 40, 40 * 4))
        if not self.v_four_ship_select:
            pygame.draw.rect(self.screen, 'red', (501, 371, 40 - 2, 40 * 4 - 2))
            if self.v_four_ship_draw and not self.count_four_ships:
                pygame.draw.rect(self.screen, 'red',
                                 (self.start_positions.left + self.new_position[0] * self.start_positions.cell_size + 1,
                                  self.start_positions.top + self.new_position[1] * self.start_positions.cell_size + 1,
                                  40 - 2, 40 * 4 - 2))
        else:
            if self.v_four_ship_draw:
                pygame.draw.rect(self.screen, 'red',
                                 (self.start_positions.left + self.new_position[0] * self.start_positions.cell_size + 1,
                                  self.start_positions.top + self.new_position[1] * self.start_positions.cell_size + 1,
                                  40 - 2, 40 * 4 - 2))
            pygame.draw.rect(self.screen, 'green', (501, 371, 40 - 2, 40 * 4 - 2))

        '''В Трехпалубные'''

        pygame.draw.rect(self.screen, 'white', (580, 370, 40, 40 * 3))
        if not self.v_three_ship_select:
            pygame.draw.rect(self.screen, 'red', (581, 371, 40 - 2, 40 * 3 - 2))
            if self.v_three_ship_draw and not self.count_three_ships:
                pygame.draw.rect(self.screen, 'red',
                                 (self.start_positions.left + self.new_position[0] * self.start_positions.cell_size + 1,
                                  self.start_positions.top + self.new_position[1] * self.start_positions.cell_size + 1,
                                  40 - 2, 40 * 3 - 2))
        else:
            if self.v_three_ship_draw:
                pygame.draw.rect(self.screen, 'red',
                                 (self.start_positions.left + self.new_position[0] * self.start_positions.cell_size + 1,
                                  self.start_positions.top + self.new_position[1] * self.start_positions.cell_size + 1,
                                  40 - 2, 40 * 3 - 2))
            pygame.draw.rect(self.screen, 'green', (581, 371, 40 - 2, 40 * 3 - 2))

        '''В Двухпалубные'''

        pygame.draw.rect(self.screen, 'white', (660, 370, 40, 40 * 2))
        if not self.v_two_ship_select:
            pygame.draw.rect(self.screen, 'red', (661, 371, 40 - 2, 40 * 2 - 2))
            if self.v_two_ship_draw and not self.count_two_ships:
                pygame.draw.rect(self.screen, 'red',
                                 (self.start_positions.left + self.new_position[0] * self.start_positions.cell_size + 1,
                                  self.start_positions.top + self.new_position[1] * self.start_positions.cell_size + 1,
                                  40 - 2, 40 * 2 - 2))
        else:
            if self.v_two_ship_draw:
                pygame.draw.rect(self.screen, 'red',
                                 (self.start_positions.left + self.new_position[0] * self.start_positions.cell_size + 1,
                                  self.start_positions.top + self.new_position[1] * self.start_positions.cell_size + 1,
                                  40 - 2, 40 * 2 - 2))
            pygame.draw.rect(self.screen, 'green', (661, 371, 40 - 2, 40 * 2 - 2))

        '''В Однопалубные'''

        pygame.draw.rect(self.screen, 'white', (740, 370, 40, 40 * 1))
        if not self.v_one_ship_select:
            pygame.draw.rect(self.screen, 'red', (741, 371, 40 - 2, 40 * 1 - 2))
            if self.v_one_ship_draw and not self.count_one_ships:
                pygame.draw.rect(self.screen, 'red',
                                 (self.start_positions.left + self.new_position[0] * self.start_positions.cell_size + 1,
                                  self.start_positions.top + self.new_position[1] * self.start_positions.cell_size + 1,
                                  40 - 2, 40 * 1 - 2))
        else:
            if self.v_one_ship_draw:
                pygame.draw.rect(self.screen, 'red',
                                 (self.start_positions.left + self.new_position[0] * self.start_positions.cell_size + 1,
                                  self.start_positions.top + self.new_position[1] * self.start_positions.cell_size + 1,
                                  40 - 2, 40 * 1 - 2))
            pygame.draw.rect(self.screen, 'green', (741, 371, 40 - 2, 40 * 1 - 2))

    def arrangement_check(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.start_positions.get_click(event.pos)

            if self.g_four_ship_select and 50 < event.pos[0] < 450 and 50 < event.pos[1] < 450:
                if self.count_four_ships > 0:
                    self.select_positions.append(self.start_positions.get_cell(event.pos))
                    self.new_position = self.start_positions.get_cell(event.pos)
                    self.g_four_ship_select = False
                    print(self.new_position)
                    if self.new_position[0] < 7:
                        self.g_four_ship_draw = True
                        self.count_four_ships -= 1
                        if self.count_four_ships == 0:
                            self.ready_four_ships = True
            if 500 < event.pos[0] < 660 and 50 < event.pos[1] < 90:
                if self.g_four_ship_select:
                    self.g_four_ship_select = False
                else:
                    self.g_one_ship_select, self.g_two_ship_select = False, False
                    self.g_three_ship_select, self.g_four_ship_select = False, True
                    self.v_one_ship_select, self.v_two_ship_select = False, False
                    self.v_three_ship_select, self.v_four_ship_select = False, False

            if self.g_three_ship_select and 50 < event.pos[0] < 450 and 50 < event.pos[1] < 450:
                if self.count_three_ships > 0:
                    self.select_positions.append(self.start_positions.get_cell(event.pos))
                    self.new_position = self.start_positions.get_cell(event.pos)
                    self.g_three_ship_select = False
                    print(self.new_position)
                    if self.new_position[0] < 8:
                        self.g_three_ship_draw = True
                        self.count_three_ships -= 1
                        if self.count_three_ships == 0:
                            self.ready_three_ships = True
            if 500 < event.pos[0] < 620 and 130 < event.pos[1] < 170:
                if self.g_three_ship_select:
                    self.g_three_ship_select = False
                else:
                    self.g_one_ship_select, self.g_two_ship_select = False, False
                    self.g_three_ship_select, self.g_four_ship_select = True, False
                    self.v_one_ship_select, self.v_two_ship_select = False, False
                    self.v_three_ship_select, self.v_four_ship_select = False, False

            if self.g_two_ship_select and 50 < event.pos[0] < 450 and 50 < event.pos[1] < 450:
                if self.count_two_ships > 0:
                    self.select_positions.append(self.start_positions.get_cell(event.pos))
                    self.new_position = self.start_positions.get_cell(event.pos)
                    self.g_two_ship_select = False
                    print(self.new_position)
                    if self.new_position[0] < 9:
                        self.g_two_ship_draw = True
                        self.count_two_ships -= 1
                        if self.count_two_ships == 0:
                            self.ready_two_ships = True
            if 500 < event.pos[0] < 580 and 210 < event.pos[1] < 250:
                if self.g_two_ship_select:
                    self.g_two_ship_select = False
                else:
                    self.g_one_ship_select, self.g_two_ship_select = False, True
                    self.g_three_ship_select, self.g_four_ship_select = False, False
                    self.v_one_ship_select, self.v_two_ship_select = False, False
                    self.v_three_ship_select, self.v_four_ship_select = False, False

            if self.g_one_ship_select and 50 < event.pos[0] < 450 and 50 < event.pos[1] < 450:
                if self.count_one_ships > 0:
                    self.select_positions.append(self.start_positions.get_cell(event.pos))
                    self.new_position = self.start_positions.get_cell(event.pos)
                    self.g_one_ship_select = False
                    print(self.new_position)
                    if self.new_position[0] < 10:
                        self.g_one_ship_draw = True
                        self.count_one_ships -= 1
                        if self.count_one_ships == 0:
                            self.ready_one_ships = True
            if 500 < event.pos[0] < 540 and 290 < event.pos[1] < 330:
                if self.g_one_ship_select:
                    self.g_one_ship_select = False
                else:
                    self.g_one_ship_select, self.g_two_ship_select = True, False
                    self.g_three_ship_select, self.g_four_ship_select = False, False
                    self.v_one_ship_select, self.v_two_ship_select = False, False
                    self.v_three_ship_select, self.v_four_ship_select = False, False

            if self.v_four_ship_select and 50 < event.pos[0] < 450 and 50 < event.pos[1] < 450:
                if self.count_four_ships > 0:
                    self.select_positions.append(self.start_positions.get_cell(event.pos))
                    self.new_position = self.start_positions.get_cell(event.pos)
                    self.v_four_ship_select = False
                    print(self.new_position)
                    if self.new_position[1] < 7:
                        self.v_four_ship_draw = True
                        self.count_four_ships -= 1
                        if self.count_four_ships == 0:
                            self.ready_four_ships = True
            if 500 < event.pos[0] < 540 and 370 < event.pos[1] < 530:
                if self.v_four_ship_select:
                    self.v_four_ship_select = False
                else:
                    self.g_one_ship_select, self.g_two_ship_select = False, False
                    self.g_three_ship_select, self.g_four_ship_select = False, False
                    self.v_one_ship_select, self.v_two_ship_select = False, False
                    self.v_three_ship_select, self.v_four_ship_select = False, True

            if self.v_three_ship_select and 50 < event.pos[0] < 450 and 50 < event.pos[1] < 450:
                if self.count_three_ships > 0:
                    self.select_positions.append(self.start_positions.get_cell(event.pos))
                    self.new_position = self.start_positions.get_cell(event.pos)
                    self.v_three_ship_select = False
                    print(self.new_position)
                    if self.new_position[1] < 8:
                        self.v_three_ship_draw = True
                        self.count_three_ships -= 1
                        if self.count_three_ships == 0:
                            self.ready_three_ships = True
            if 580 < event.pos[0] < 620 and 370 < event.pos[1] < 490:
                if self.v_three_ship_select:
                    self.v_three_ship_select = False
                else:
                    self.g_one_ship_select, self.g_two_ship_select = False, False
                    self.g_three_ship_select, self.g_four_ship_select = False, False
                    self.v_one_ship_select, self.v_two_ship_select = False, False
                    self.v_three_ship_select, self.v_four_ship_select = True, False

            if self.v_two_ship_select and 50 < event.pos[0] < 450 and 50 < event.pos[1] < 450:
                if self.count_two_ships > 0:
                    self.select_positions.append(self.start_positions.get_cell(event.pos))
                    self.new_position = self.start_positions.get_cell(event.pos)
                    self.v_two_ship_select = False
                    print(self.new_position)
                    if self.new_position[1] < 9:
                        self.g_two_ship_draw = True
                        self.count_two_ships -= 1
                        if self.count_two_ships == 0:
                            self.ready_two_ships = True
            if 660 < event.pos[0] < 700 and 370 < event.pos[1] < 450:
                if self.v_two_ship_select:
                    self.v_two_ship_select = False
                else:
                    self.g_one_ship_select, self.g_two_ship_select = False, False
                    self.g_three_ship_select, self.g_four_ship_select = False, False
                    self.v_one_ship_select, self.v_two_ship_select = False, True
                    self.v_three_ship_select, self.v_four_ship_select = False, False

            if self.v_one_ship_select and 50 < event.pos[0] < 450 and 50 < event.pos[1] < 450:
                if self.count_one_ships > 0:
                    self.select_positions.append(self.start_positions.get_cell(event.pos))
                    self.new_position = self.start_positions.get_cell(event.pos)
                    self.v_one_ship_select = False
                    print(self.new_position)
                    if self.new_position[1] < 10:
                        self.v_one_ship_draw = True
                        self.count_one_ships -= 1
                        if self.count_one_ships == 0:
                            self.ready_one_ships = True
            if 740 < event.pos[0] < 780 and 370 < event.pos[1] < 410:
                if self.v_one_ship_select:
                    self.v_one_ship_select = False
                else:
                    self.g_one_ship_select, self.g_two_ship_select = False, False
                    self.g_three_ship_select, self.g_four_ship_select = False, False
                    self.v_one_ship_select, self.v_two_ship_select = True, False
                    self.v_three_ship_select, self.v_four_ship_select = False, False

    def connecting(self):
        image = pygame.image.load("Images/upscale_1.jpeg")
        image = pygame.transform.scale(image, self.screen.get_size())
        self.screen.blit(image, (0, 0))

        self.text_input.render()
        self.button_return_to_start_screen.render()
        self.button_enter.render()

    def connecting_check(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.text_input.get_click(event.pos)
            self.button_return_to_start_screen.get_click(event.pos)
            self.button_enter.get_click(event.pos)

        if event.type == pygame.KEYDOWN and self.text_input.active:
            if event.key == pygame.K_BACKSPACE:
                self.text_input.text = self.text_input.text[:-1]

            else:
                self.text_input.text += event.unicode

    @staticmethod
    def quit_and_kill_all_processes():
        pygame.quit()
        send_chan.send("quit")
        sys.exit()


def client_process(recv_ch, queue):
    import threading as th

    host, port = "26.234.107.47", 12345
    with client.connect(f"ws://{host}:{port}") as conn:
        ID = conn.recv()
        queue.put(ID)
        print(ID)

        def sender():
            print("Sender started")
            while True:
                data = recv_ch.recv()
                if data == "quit":
                    conn.close()
                    return
                conn.send(data)
                print(f"Sent: `{data}`")

        def receiver():
            print("Receiver started")
            while True:
                try:
                    data = conn.recv()
                except ws.ConnectionClosedOK:
                    print("Close connection.")
                    return
                queue.put(data)
                print(f"Got: `{data}`")

        threads = [th.Thread(target=sender, name="thr-1"), th.Thread(target=receiver, name="thr-2")]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()


if __name__ == "__main__":
    send_chan, recv_chan = mp.Pipe()
    queue = mp.Queue()
    ps = mp.Process(target=client_process, name="ps-1", args=(recv_chan, queue))
    ps.start()
    Game()
