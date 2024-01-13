import sys
import multiprocessing as mp
import websockets as ws
import websockets.sync.client as client
import pygame

from Classes.Board import Board
from Classes.Button import Button
from Classes.TextInput import TextInput
from Classes.Ship import Ship
from Server.Client import Client


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

        """Поля"""
        self.matrix_1 = [[0] * 10] * 10
        self.matrix_2 = [[0] * 10] * 10

        """Основное меню"""
        self.button_quit = Button(self, self.screen, 'QUIT', 'red', text='Выход')
        self.button_quit.set_view(200, 475, 100, 50)
        self.button_start = Button(self, self.screen, 'START', 'orange', text='Старт')
        self.button_start.set_view(350, 475, 100, 50)
        self.button_profile = Button(self, self.screen, 'PROFILE', 'white', text='Профиль')
        self.button_profile.set_view(500, 475, 100, 50)

        """Расстановка кораблей"""
        self.board = Board(self.screen, 'ARRANGEMENT', self.matrix_1, 'white', 50, 50, 10, 10, 30)
        self.group = pygame.sprite.Group()
        self.ship = Ship(self.group, self.board)

        """Ввод ID"""
        self.text_input = TextInput(self, self.screen, 'white', 100, 200, 600, 60)
        self.button_return_to_start_screen = Button(self, self.screen, 'RETURN_TO_START_SCREEN', 'red', text='Вернуться')
        self.button_return_to_start_screen.set_view(200, 475, 100, 50)
        self.button_enter = Button(self, self.screen, 'ENTER', 'green', text='Войти')
        self.button_enter.set_view(500, 475, 100, 50)

        """Игра"""
        self.button_fire = Button(self, self.screen, 'FIRE', 'red', text='Огонь')
        self.button_fire.set_view(0, 0, 100, 50)
        self.player_1_board = Board(self.screen, 'PLAYER_1', self.matrix_1, 'green', 50, 50, 10, 10, 30)
        self.player_2_board = Board(self.screen, 'PLAYER_2', self.matrix_2, 'red', 400, 50, 10, 10, 30)

        """Запуск стартового окна игры"""
        self.running_one = self.start_screen
        self.checking_one = self.start_screen_check
        self.run()

    def run(self):
        while True:
            self.running_one()
            if self.get_message() == 'Room created':
                self.running_one = self.arrangement
                self.checking_one = self.arrangement_check
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_and_kill_all_processes()

                self.checking_one(event)

            pygame.display.flip()

    def check_in(self):
        pass

    def check_in_check(self, event):
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
        self.board.render()
        self.group.draw(self.screen)

    def arrangement_check(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.ship.moving = True
            self.group.update(event)
            self.board.get_click(event.pos)
        elif event.type == pygame.MOUSEBUTTONUP:
            self.ship.moving = False
            self.group.update(event)
        elif event.type == pygame.MOUSEMOTION:
            self.group.update(event)

    def connecting(self):
        image = pygame.image.load("Images/upscale_1.jpeg")
        image = pygame.transform.scale(image, self.screen.get_size())
        self.screen.blit(image, (0, 0))

        self.text_input.render()
        self.button_return_to_start_screen.render()

    def connecting_check(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.text_input.get_click(event.pos)
            self.button_return_to_start_screen.get_click(event.pos)
            self.button_enter.get_click(event.pos)

        if event.type == pygame.KEYDOWN and self.text_input.active:
            if event.key == pygame.K_BACKSPACE:
                self.text_input.text = self.text_input.text[:-1]
            elif event.key == pygame.K_RETURN:
                send_chan.send(Client.createRoom(self.text_input.text))
                self.text_input.active = False
            else:
                self.text_input.text += event.unicode

    @staticmethod
    def get_message():
        """Returns None if there aren't any messages."""

        import queue as q

        try:
            data = queue.get(False)
            return data
        except q.Empty:
            return None

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
