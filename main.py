import sys
import pygame
from Classes.Board import Board
from Classes.Button import Button


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

        self.button_quit = Button(self.screen, 'QUIT', 'red')
        self.button_quit.set_view(10, 545, 75, 45)
        self.button_start = Button(self.screen, 'START', 'blue')
        self.button_start.set_view(10, 10, 75, 45)

        """При запуске игры пока что будет открываться окно меню"""
        self.running_one = self.start_screen
        self.run()

    def run(self):
        while True:
            self.running_one()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.button_start.get_click(event.pos)
                    self.button_quit.get_click(event.pos)

            pygame.display.flip()

    def start_screen(self):
        self.button_start.render()
        self.button_quit.render()

    def check_in(self):
        pass


if __name__ == "__main__":
    Game()
