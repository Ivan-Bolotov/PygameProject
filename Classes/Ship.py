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
            self.image = pygame.Surface((60, 30), masks=(255, 0, 0))
            self.rect = pygame.Rect(*pos, 60, 30)
        elif self.size == 3:
            self.image = pygame.Surface((90, 30), masks=(255, 0, 0))
            self.rect = pygame.Rect(*pos, 90, 30)
        elif self.size == 4:
            self.image = pygame.Surface((120, 30), masks=(255, 0, 0))
            self.rect = pygame.Rect(*pos, 120, 30)

    def update(self, *args, **kwargs):
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and self.moving:
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

                if self.size == 4:
                    try:
                        for i in range(x_cords - 1, x_cords + 5):
                            for j in range(y_cords - 1, y_cords + 2):
                                if self.board.matrix[j][i] != 0:
                                    nice = False
                                    break
                            if not nice:
                                break
                    except IndexError:
                        pass
                    if nice:
                        self.rect.top = y_cords * self.board.cell_size + self.board.top
                        self.rect.left = x_cords * self.board.cell_size + self.board.left
                        try:
                            for i in range(4):
                                self.board.matrix[y_cords][x_cords + i] = 1
                        except IndexError:
                            self.moving = False
                            self.rect.left, self.rect.top = self.start_pos
                    else:
                        self.moving = False
                        self.rect.left, self.rect.top = self.start_pos

                elif self.size == 3:
                    try:
                        for i in range(x_cords - 1, x_cords + 4):
                            for j in range(y_cords - 1, y_cords + 2):
                                if self.board.matrix[j][i] != 0:
                                    nice = False
                                    break
                            if not nice:
                                break
                    except IndexError:
                        pass
                    if nice:
                        self.rect.top = y_cords * self.board.cell_size + self.board.top
                        self.rect.left = x_cords * self.board.cell_size + self.board.left
                        try:
                            for i in range(3):
                                self.board.matrix[y_cords][x_cords + i] = 1
                        except IndexError:
                            self.moving = False
                            self.rect.left, self.rect.top = self.start_pos
                    else:
                        self.moving = False
                        self.rect.left, self.rect.top = self.start_pos

                elif self.size == 2:
                    try:
                        for i in range(x_cords - 1, x_cords + 3):
                            for j in range(y_cords - 1, y_cords + 2):
                                if self.board.matrix[j][i] != 0:
                                    nice = False
                                    break
                            if not nice:
                                break
                    except IndexError:
                        pass
                    if nice:
                        self.rect.top = y_cords * self.board.cell_size + self.board.top
                        self.rect.left = x_cords * self.board.cell_size + self.board.left
                        try:
                            for i in range(2):
                                self.board.matrix[y_cords][x_cords + i] = 1
                        except IndexError:
                            self.moving = False
                            self.rect.left, self.rect.top = self.start_pos
                    else:
                        self.moving = False
                        self.rect.left, self.rect.top = self.start_pos

                elif self.size == 1:
                    try:
                        for i in range(x_cords - 1, x_cords + 2):
                            for j in range(y_cords - 1, y_cords + 2):
                                if self.board.matrix[j][i] != 0:
                                    nice = False
                                    break
                            if not nice:
                                break
                    except IndexError:
                        pass
                    if nice:
                        self.rect.top = y_cords * self.board.cell_size + self.board.top
                        self.rect.left = x_cords * self.board.cell_size + self.board.left
                        try:
                            for i in range(1):
                                self.board.matrix[y_cords][x_cords + i] = 1
                        except IndexError:
                            self.moving = False
                            self.rect.left, self.rect.top = self.start_pos
                    else:
                        self.moving = False
                        self.rect.left, self.rect.top = self.start_pos

        elif args and (args[0].type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(args[0].pos))\
                and (self.rect.left < args[0].pos[0] < self.rect.right
                     and self.rect.top < args[0].pos[1] < self.rect.bottom):
            if self.rect.left != self.start_pos[0] and self.rect.top != self.start_pos[1]:
                x_cords = (args[0].pos[0] - self.board.left) // self.board.cell_size
                y_cords = (args[0].pos[1] - self.board.top) // self.board.cell_size
                for i in range(self.size):
                    self.board.matrix[y_cords][x_cords] = 0
                    x_cords += 1
            self.moving = True

        if self.moving:
            self.rect.centerx = args[0].pos[0]
            self.rect.centery = args[0].pos[1]