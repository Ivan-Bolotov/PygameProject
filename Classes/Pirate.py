import pygame


class Pirate(pygame.sprite.Sprite):
    def __init__(self, group, screen):
        super().__init__(group)
        self.screen = screen
        self.images = []

        for i in range(4):
            image = pygame.image.load(f"./Images/Pirate_{i}.png")
            image = pygame.transform.scale(image, (300, 300))
            image.set_colorkey(image.get_at((0, 0)))
            self.images.append(image.convert_alpha())

        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.centerx = self.screen.get_rect().centerx
        self.rect.centery = self.screen.get_rect().centery
        self.generator = self.next_image()

    def update(self, *args, **kwargs):
        self.image = next(self.generator)

    def next_image(self):
        while True:
            for i in range(4):
                yield self.images[i]
            for i in range(2, 0, -1):
                yield self.images[i]
