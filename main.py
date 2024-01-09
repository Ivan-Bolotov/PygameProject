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

        text_image = pygame.image.load('Images/Sea_Battle_text.png')
        text_image = pygame.transform.scale(text_image, (400, 155))
        text_image_rect = text_image.get_rect()
        text_image_rect.centerx = self.screen.get_rect().centerx
        self.screen.blit(text_image, text_image_rect)

        """Основное меню"""
        self.button_quit = Button(self, self.screen, 'QUIT', 'red', text='Выход')
        self.button_quit.set_view(200, 475, 100, 50)
        self.button_start = Button(self, self.screen, 'START', 'orange', text='Старт')
        self.button_start.set_view(350, 475, 100, 50)
        self.button_profile = Button(self, self.screen, 'PROFILE', 'white', text='Профиль')
        self.button_profile.set_view(500, 475, 100, 50)

        """Расстановка кораблей"""
        self.start_positions = Board(self.screen, 'ARRANGEMENT', 'white', 50, 50, 10, 10, 50)
        self.button_one_ship = Button(self, self.screen, 'ONE_SHIP', 'white', text='1')
        self.button_one_ship.set_view(630, 100, 75, 75)
        self.button_two_ship = Button(self, self.screen, 'TWO_SHIP', 'white', text='2')
        self.button_two_ship.set_view(630, 200, 75, 75)
        self.button_three_ship = Button(self, self.screen, 'THREE_SHIP', 'white', text='3')
        self.button_three_ship.set_view(630, 300, 75, 75)
        self.button_four_ship = Button(self, self.screen, 'FOUR_SHIP', 'white', text='4')
        self.button_four_ship.set_view(630, 400, 75, 75)

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
        self.button_one_ship.render()
        self.button_two_ship.render()
        self.button_three_ship.render()
        self.button_four_ship.render()

    def arrangement_check(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.start_positions.get_click(event.pos)
            self.button_one_ship.get_click(event.pos)
            self.button_two_ship.get_click(event.pos)
            self.button_three_ship.get_click(event.pos)
            self.button_four_ship.get_click(event.pos)

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

    host, port = "localhost", 12345
    with client.connect(f"ws://{host}:{port}") as conn:
        ID = conn.recv()
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
