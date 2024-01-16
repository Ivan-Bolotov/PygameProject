import pygame


class Ship(pygame.sprite.Sprite):
    def __init__(self, screen, group, board, size=1, pos=(0, 0)):
        super().__init__(group)
        self.screen = screen
        self.vertical = False
        self.board = board
        self.cords_on_board = (None, None)
        self.start_pos = pos
        self.size = size
        self.moving = False

        self.image = pygame.Surface((self.size * 30, 30))
        self.image.fill((255, 0, 0))
        self.rect = pygame.Rect(*pos, self.size * 30, 30)
        self.board_rect = pygame.Rect(
            self.board.left, self.board.top,
            self.board.width * self.board.cell_size,
            self.board.width * self.board.cell_size
        )

    def update(self, *args, **kwargs):
        if not args:
            return

        event = args[0]

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.moving:
                    self.moving = False

                    if not self.board_rect.collidepoint(*args[0].pos):
                        self.rect.left, self.rect.top = self.start_pos
                        self.cords_on_board = (None, None)
                    else:
                        nice = True

                        x_cords = (args[0].pos[0] - self.board.left) // self.board.cell_size
                        y_cords = (args[0].pos[1] - self.board.top) // self.board.cell_size
                        self.cords_on_board = (x_cords, y_cords)

                        if not self.vertical:
                            for i in range(x_cords - 1, x_cords + self.size + 1):
                                for j in range(y_cords - 1, y_cords + 2):
                                    if i > 10 or j > 10 or self.board.matrix[j][i] != 0:
                                        nice = False
                                        break
                                if not nice:
                                    break

                            if nice:
                                self.rect.top = y_cords * self.board.cell_size + self.board.top
                                self.rect.left = x_cords * self.board.cell_size + self.board.left

                                for i in range(self.size):
                                    self.board.matrix[y_cords][x_cords + i] = 1

                            else:
                                self.rect.left, self.rect.top = self.start_pos

                        else:
                            for i in range(x_cords - 1, x_cords + 2):
                                for j in range(y_cords - 1, y_cords + self.size + 1):
                                    if i > 10 or j > 10 or self.board.matrix[j][i] != 0:
                                        nice = False
                                        break
                                if not nice:
                                    break

                            if nice:
                                self.rect.top = y_cords * self.board.cell_size + self.board.top
                                self.rect.left = x_cords * self.board.cell_size + self.board.left

                                for i in range(self.size):
                                    self.board.matrix[y_cords + i][x_cords] = 1

                            else:
                                self.rect.left, self.rect.top = self.start_pos
                                self.cords_on_board = (None, None)

                elif self.rect.collidepoint(args[0].pos):
                    self.moving = True

                    if self.cords_on_board != (None, None):
                        x_cords, y_cords = self.cords_on_board

                        if not self.vertical:
                            for i in range(self.size):
                                self.board.matrix[y_cords][x_cords + i] = 0

                        else:
                            for i in range(self.size):
                                self.board.matrix[y_cords + i][x_cords] = 0

            elif event.button == 3 and self.rect.collidepoint(args[0].pos) and not self.moving \
                    and not self.board_rect.collidepoint(*args[0].pos):

                if self.vertical:
                    self.vertical = False
                    self.image = pygame.Surface((self.size * 30, 30))
                    self.image.fill((255, 0, 0))
                    self.rect = pygame.Rect(*self.start_pos, self.size * 30, 30)

                else:
                    self.vertical = True
                    self.image = pygame.Surface((30, self.size * 30))
                    self.image.fill((255, 0, 0))
                    self.rect = pygame.Rect(*self.start_pos, 30, self.size * 30)

        if self.moving:
            self.rect.centerx, self.rect.centery = event.pos
