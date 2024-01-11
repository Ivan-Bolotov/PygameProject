import pygame


class Ship(pygame.sprite.Sprite):
    def __init__(self, group, board, size=1, pos=(0, 0)):
        super().__init__(group)
        self.board = board
        self.start_pos = pos
        self.size = size
        self.moving = False
        if self.size == 1:
            self.image = pygame.Surface((30, 30), masks=(255, 0, 0))
            self.rect = pygame.Rect(*pos, 30, 30)
        elif self.size == 2:
            self.image = pygame.Surface((30, 60), masks=(255, 0, 0))
            self.rect = pygame.Rect(*pos, 30, 60)
        elif self.size == 3:
            self.image = pygame.Surface((30, 90), masks=(255, 0, 0))
            self.rect = pygame.Rect(*pos, 30, 90)
        elif self.size == 4:
            self.image = pygame.Surface((30, 120), masks=(255, 0, 0))
            self.rect = pygame.Rect(*pos, 30, 120)

    def update(self, *args, **kwargs):
        if args and (args[0].type == pygame.MOUSEBUTTONDOWN and \
                     self.rect.collidepoint(args[0].pos) or self.moving):
            self.rect.centerx = args[0].pos[0]
            self.rect.centery = args[0].pos[1]
        elif args and args[0].type == pygame.MOUSEBUTTONUP:
            if not self.rect.colliderect(
                    pygame.Rect(
                        self.board.left, self.board.top,
                        self.board.width * self.board.cell_size,
                        self.board.width * self.board.cell_size
                    )):
                self.rect.left, self.rect.right = self.start_pos
