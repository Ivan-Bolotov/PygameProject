import sys
import time
import json
import queue as q
import multiprocessing as mp
import websockets as ws
import websockets.sync.client as client
import pygame

from Classes.Board import Board
from Classes.Button import Button
from Classes.TextInput import TextInput
from Classes.Ship import Ship
from Server.Client import Client

from constants import *


class Game:
    def __init__(self):

        pygame.init()
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
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
                                      False, COLORS.WHITE))
        self.label_with_id_rect = self.label_with_id.get_rect()
        self.label_with_id_rect.bottom = self.screen.get_rect().bottom - 20
        self.label_with_id_rect.centerx = self.screen.get_rect().centerx
        self.screen.blit(self.label_with_id, self.label_with_id_rect)

        """Поля"""
        self.matrix_1 = [[0 for _ in range(10)] for _ in range(10)]
        self.matrix_2 = [[0 for _ in range(10)] for _ in range(10)]

        """Основное меню"""
        self.button_quit = Button(self, self.screen, 'QUIT', COLORS.RED, text='Выход')
        self.button_quit.set_view(190, 475, 120, 50)
        self.button_start = Button(self, self.screen, 'START', COLORS.GREEN, text='Старт')
        self.button_start.set_view(350, 475, 100, 50)
        self.button_profile = Button(self, self.screen, 'PROFILE', COLORS.WHITE, text='Профиль')
        self.button_profile.set_view(480, 475, 140, 50)

        pygame.mixer.music.load("Audio/super_krutaya_battle_music.mp3")
        pygame.mixer.music.set_volume(0.2)
        self.start_screen_music_is = False

        """Расстановка кораблей"""
        matrix = {}
        for i in range(-1, 11):
            matrix[i] = {}
            for j in range(-1, 11):
                matrix[i][j] = 0

        self.board = Board(self.screen, 'ARRANGEMENT', matrix,
                           COLORS.WHITE, 50, 50, 10, 10, 30)
        self.group = pygame.sprite.Group()

        self.arr_ready_button = Button(self, self.screen, 'ARR_READY', color=COLORS.GREEN, left=200, top=400,
                                       width=150, height=50, text='ГОТОВО', board=self.board)

        self.ship_4 = Ship(self.screen, self.group, self.board, 4, (400, 50))
        self.ship_3_1 = Ship(self.screen, self.group, self.board, 3, (550, 50))
        self.ship_3_2 = Ship(self.screen, self.group, self.board, 3, (670, 50))
        self.ship_2_1 = Ship(self.screen, self.group, self.board, 2, (400, 200))
        self.ship_2_2 = Ship(self.screen, self.group, self.board, 2, (490, 200))
        self.ship_2_3 = Ship(self.screen, self.group, self.board, 2, (580, 200))
        self.ship_1_1 = Ship(self.screen, self.group, self.board, 1, (400, 290))
        self.ship_1_2 = Ship(self.screen, self.group, self.board, 1, (460, 290))
        self.ship_1_3 = Ship(self.screen, self.group, self.board, 1, (520, 290))
        self.ship_1_4 = Ship(self.screen, self.group, self.board, 1, (580, 290))

        self.flag_send = True
        self.flag_recv = True

        """Ввод ID"""
        self.text_input = TextInput(self, self.screen, COLORS.WHITE, 100, 200, 600, 60)

        self.button_return_to_start_screen = Button(self, self.screen,
                                                    'RETURN_TO_START_SCREEN', COLORS.RED, text='Вернуться')
        self.button_return_to_start_screen.set_view(175, 475, 150, 50)

        self.button_enter = Button(self, self.screen, 'ENTER', COLORS.GREEN, text='Войти')
        self.button_enter.set_view(500, 475, 100, 50)

        self.arr_ready_1 = False

        """Игра"""
        self.player_1_turn = False

        text_out = 'ход 1 игрока' if self.player_1_turn else 'ход 2 игрока'
        self.button_fire = Button(self, self.screen, 'FIRE', COLORS.RED, text=text_out)
        self.button_fire.set_view(500, 500, 100, 50)

        self.player_1_board = Board(self.screen, 'PLAYER_1', self.matrix_1,
                                    COLORS.WHITE, 50, 50, 10, 10, 30)

        self.player_2_board = Board(self.screen, 'PLAYER_2', self.matrix_2,
                                    COLORS.WHITE, 400, 50, 10, 10, 30)

        """Установка таймера для FPS"""
        self.timer = pygame.time.Clock()

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
            self.timer.tick(FPS)

    def start_screen(self):
        image = pygame.image.load("Images/main_screen.jpg")
        image = pygame.transform.scale(image, self.screen.get_size())

        if not self.start_screen_music_is:
            time.sleep(0.3)
            pygame.mixer.music.load("Audio/super_krutaya_battle_music.mp3")
            pygame.mixer.music.play(-1)
            self.start_screen_music_is = True

        self.screen.blit(image, (0, 0))
        self.screen.blit(self.text_image, self.text_image_rect)
        self.screen.blit(self.label_with_id, self.label_with_id_rect)

        self.button_start.render()
        self.button_quit.render()
        self.button_profile.render()

    def start_screen_check(self, event):
        if self.get_message() == 'Room created':
            self.running_one = self.arrangement
            self.checking_one = self.arrangement_check

        if event.type == pygame.MOUSEBUTTONDOWN:
            self.button_start.get_click(event.pos)
            self.button_profile.get_click(event.pos)
            self.button_quit.get_click(event.pos)

    def arrangement(self):
        image = pygame.image.load("Images/main_screen.jpg")
        image = pygame.transform.scale(image, self.screen.get_size())
        self.screen.blit(image, (0, 0))
        self.board.render()
        self.arr_ready_button.render()
        self.group.draw(self.screen)

        if self.start_screen_music_is:
            # self.start_screen_music.stop()
            self.start_screen_music_is = False

    def arrangement_check(self, event):
        message = self.get_message()

        if self.arr_ready_1 and self.flag_send:
            self.flag_send = False
            self.send_message(Client.sendReady())

        if message:
            if message == "Ready":
                if self.flag_recv:
                    self.flag_recv = False
            else:
                arr = message.split()
                t = arr[0]
                msg = ""
                for i in arr[1:]:
                    msg += i
                if t == "Matrix":
                    print("Переопределение матрицы!!!!!!!!!")
                    self.player_2_board.matrix = self.matrix_2 = json.loads(msg)

        if not self.flag_recv and not self.flag_send:
            self.running_one = self.game
            self.checking_one = self.game_check

        if event.type == pygame.MOUSEBUTTONDOWN:
            self.group.update(event)
            self.board.get_click(event.pos)
            self.arr_ready_button.get_click(event.pos)
        elif event.type == pygame.MOUSEBUTTONUP:
            self.group.update(event)
        elif event.type == pygame.MOUSEMOTION:
            self.group.update(event)

    def connecting(self):
        image = pygame.image.load("Images/main_screen.jpg")
        image = pygame.transform.scale(image, self.screen.get_size())
        self.screen.blit(image, (0, 0))

        self.text_input.render()
        self.button_return_to_start_screen.render()

    def connecting_check(self, event):
        if self.get_message() == 'Room created':
            self.running_one = self.arrangement
            self.checking_one = self.arrangement_check

        if event.type == pygame.MOUSEBUTTONDOWN:
            self.text_input.get_click(event.pos)
            self.button_return_to_start_screen.get_click(event.pos)
            self.button_enter.get_click(event.pos)

        if event.type == pygame.KEYDOWN and self.text_input.active:
            if event.key == pygame.K_BACKSPACE:
                self.text_input.text = self.text_input.text[:-1]
            elif event.key == pygame.K_RETURN:
                self.player_1_turn = True
                self.text_input.active = False
                self.send_message(Client.createRoom(self.text_input.text))
            else:
                self.text_input.text += event.unicode

    def game(self):
        image = pygame.image.load("Images/main_screen.jpg")
        image = pygame.transform.scale(image, self.screen.get_size())
        self.screen.blit(image, (0, 0))

        self.player_1_board.render()
        self.player_2_board.render()

    def game_check(self, event):
        message = self.get_message()

        if event.type == pygame.MOUSEBUTTONDOWN:
            print('clicked')
            if self.player_1_turn:
                self.player_1_board.get_click(event.pos)
                self.player_2_board.get_click(event.pos)
                print(self.player_1_turn)
                print(self.player_2_board.ship_cords)
                print(self.player_2_board.player_1_clicked)

            if self.player_2_board.player_1_clicked and self.player_1_turn:
                self.player_1_turn = False
                self.player_2_board.player_1_clicked = False
                print('sent')
                self.send_message(Client.sendCords(*self.player_2_board.ship_cords))

        if message is None:
            return

        message = message.split(':')
        if message[0] == 'Cords':
            self.player_1_turn = True
            self.player_1_board.suffer((int(message[1]), int(message[2])))
            print(message[1], message[2])

    @staticmethod
    def get_message():
        """Returns None if there aren't any messages."""
        try:
            data = queue.get(False)
            return data
        except q.Empty:
            return None

    @staticmethod
    def send_message(msg: str):
        """Sends message to server anyway."""
        send_chan.send(msg)

    def quit_and_kill_all_processes(self):
        pygame.quit()
        self.send_message("quit")
        sys.exit()


def client_process(recv_ch, queue):
    import threading as th
    from Server.get_server_ip import get_server_ip

    host, port = get_server_ip("./Server/ip.txt"), 12345
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
