import pygame


class Ship(pygame.sprite.Sprite):
    def __init__(self, screen, group, board, size=1, pos=(0, 0)):
        super().__init__(group)
        self.screen = screen
        self.vertical = False
        self.board = board
        self.start_pos = pos
        self.size = size
        self.moving = False

        self.image = pygame.Surface((self.size * 30, 30), masks=(255, 0, 0))
        self.rect = pygame.Rect(*pos, self.size * 30, 30)

    def update(self, *args, **kwargs):
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and args[0].button == 1 and self.moving:
            if self.screen.get_at(args[0].pos) != (255, 255, 255):

                if not self.rect.colliderect(
                        pygame.Rect(
                            self.board.left, self.board.top,
                            self.board.width * self.board.cell_size,
                            self.board.width * self.board.cell_size
                        )):
                    self.moving = False
                    self.rect.left, self.rect.top = self.start_pos

                else:
                    self.moving = False
                    nice = True

                    x_cords = (args[0].pos[0] - self.board.left) // self.board.cell_size
                    y_cords = (args[0].pos[1] - self.board.top) // self.board.cell_size

                    if not self.vertical:
                        if x_cords + self.size - 1 < 10:
                            for i in range(x_cords - 1, x_cords + self.size + 1):
                                for j in range(y_cords - 1, y_cords + 2):
                                    print(i, j)
                                    if self.board.matrix[j][i] != 0:
                                        nice = False
                                        break
                                if not nice:
                                    break
                            if nice:
                                self.rect.top = y_cords * self.board.cell_size + self.board.top
                                self.rect.left = x_cords * self.board.cell_size + self.board.left
                                for i in range(self.size):
                                    if x_cords + i > 9:
                                        self.moving = False
                                        self.rect.left, self.rect.top = self.start_pos
                                        nice = False
                                        break
                                    else:
                                        nice = True
                                if nice:
                                    for i in range(self.size):
                                        self.board.matrix[y_cords][x_cords + i] = 1
                                else:
                                    self.moving = False
                                    self.rect.left, self.rect.top = self.start_pos
                            else:
                                self.moving = False
                                self.rect.left, self.rect.top = self.start_pos
                        else:
                            self.moving = False
                            self.rect.left, self.rect.top = self.start_pos

                    else:
                        if y_cords + self.size - 1 < 10:
                            for i in range(x_cords - 1, x_cords + 2):
                                for j in range(y_cords - 1, y_cords + self.size + 1):
                                    print(i, j)
                                    if self.board.matrix[j][i] != 0:
                                        nice = False
                                        break
                                if not nice:
                                    break
                            if nice:
                                self.rect.top = y_cords * self.board.cell_size + self.board.top
                                self.rect.left = x_cords * self.board.cell_size + self.board.left
                                for i in range(self.size):
                                    if y_cords + i > 9:
                                        self.moving = False
                                        self.rect.left, self.rect.top = self.start_pos
                                        nice = False
                                        break
                                    else:
                                        nice = True
                                if nice:
                                    for i in range(self.size):
                                        self.board.matrix[y_cords + i][x_cords] = 1
                                else:
                                    self.moving = False
                                    self.rect.left, self.rect.top = self.start_pos
                            else:
                                self.moving = False
                                self.rect.left, self.rect.top = self.start_pos
                        else:
                            self.moving = False
                            self.rect.left, self.rect.top = self.start_pos
            else:
                self.moving = False
                self.rect.left, self.rect.top = self.start_pos

        elif args and (args[0].type == pygame.MOUSEBUTTONDOWN and args[0].button == 1
                       and self.rect.collidepoint(args[0].pos)):
            if self.board.left < args[0].pos[0] < self.board.left + self.board.cell_size * self.board.width and \
                    self.board.top < args[0].pos[1] < self.board.top + self.board.cell_size * self.board.height:
                x_cords = (args[0].pos[0] - self.board.left) // self.board.cell_size
                y_cords = (args[0].pos[1] - self.board.top) // self.board.cell_size

                if not self.vertical:
                    for i in range(self.size):
                        self.board.matrix[y_cords][x_cords] = 0
                        x_cords += 1
                else:
                    for i in range(self.size):
                        self.board.matrix[y_cords][x_cords] = 0
                        y_cords += 1

            self.moving = True

        elif args and (args[0].type == pygame.MOUSEBUTTONDOWN and args[0].button == 3
                       and self.rect.collidepoint(args[0].pos)) and not self.moving\
                and not self.vertical:
            if not (self.board.left < args[0].pos[0] < self.board.left + self.board.cell_size * self.board.width and \
                    self.board.top < args[0].pos[1] < self.board.top + self.board.cell_size * self.board.height):
                self.vertical = True
                self.image = pygame.Surface((30, self.size * 30), masks=(255, 0, 0))
                self.rect = pygame.Rect(*self.start_pos, 30, self.size * 30)

        elif args and (args[0].type == pygame.MOUSEBUTTONDOWN and args[0].button == 3
                       and self.rect.collidepoint(args[0].pos)) and not self.moving\
                and self.vertical:
            if not (self.board.left < args[0].pos[0] < self.board.left + self.board.cell_size * self.board.width and \
                    self.board.top < args[0].pos[1] < self.board.top + self.board.cell_size * self.board.height):
                self.vertical = False
                self.image = pygame.Surface((self.size * 30, 30), masks=(255, 0, 0))
                self.rect = pygame.Rect(*self.start_pos, self.size * 30, 30)

        if self.moving:
            self.rect.centerx = args[0].pos[0]
            self.rect.centery = args[0].pos[1]