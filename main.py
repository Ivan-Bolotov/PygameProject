import sys
import pygame
from Classes.Board import Board
from Classes.Button import Button


class Game:
    def __init__(self):

        pygame.init()

        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Морской бой онлайн")

        image = pygame.image.load("Images/MainScreen3.jpg")
        image = pygame.transform.scale(image, self.screen.get_size())
        self.screen.blit(image, (0, 0))

        font = pygame.font.SysFont("Arial", 50)
        text = font.render("Морской бой", True, (50, 50, 175))
        text_rect = text.get_rect()
        text_rect.centerx = self.screen.get_rect().centerx
        self.screen.blit(text, text_rect)

        self.button_quit = Button(self.screen, 'QUIT', 'blue')
        self.button_start = Button(self.screen, 'START', 'red', 10, 100)

        """При запуске игры пока что будет открываться окно меню"""
        self.running_one = self.start_screen
        self.run()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                self.running_one()
            pygame.display.flip()

    def start_screen(self):
        self.button_start.render()
        self.button_quit.render()


if __name__ == "__main__":
    Game()
