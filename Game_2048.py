import random
from typing import List, Tuple, Optional
import pygame
from pygame.locals import (KEYDOWN,
                           KEYUP,
                           K_LEFT,
                           K_RIGHT,
                           K_UP,
                           K_DOWN,
                           K_ESCAPE)


class Game:
    """Game class for 2048
    """
    board: List[List[int]]
    score: int

    def __init__(self):
        self.board = []
        for _ in range(4):
            lst = [0, 0, 0, 0]
            self.board.append(lst)
        self.score = 0

    def __str__(self):
        s = ''
        for row in self.board:
            for col in row:
                s += f'{str(col) :<5}'
            s += '\n'

        return s

    # def find_space(self, x: int) -> Optional[Tuple[int, int]]:
    #     """
    #     >>> g = Game()
    #     >>> g.find_space(15)
    #     (3, 3)
    #     >>> g.board = [[16, 8, 0, 0], [4, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    #     >>> g.find_space(13)
    #     (0, 2)
    #     >>> g.board = [[0, 4, 32, 2],
    #     ...            [4, 2, 4, 64],
    #     ...            [16, 256, 8, 2],
    #     ...            [2, 4, 8, 4]]
    #     >>> g.find_space(13)
    #     (0, 0)
    #     """
    #     init_val = x
    #     b = self.board
    #     i = 0
    #     assert x >= 0  # x should be a non-negative integer
    #     while i < len(b):
    #         j = 0
    #         while j < len(b):
    #             if b[i][j] == 0:
    #                 if x > 0:
    #                     x -= 1
    #                 elif x == 0:
    #                     return i, j
    #             j += 1
    #         i += 1
    #         if (i, j) == (4, 4):
    #             if x == init_val:
    #                 return None
    #             elif x >= 0:
    #                 i, j = 0, 0

    def get_index_zero(self, lst):
        list_ = []
        for i in range(len(lst)):
            if lst[i] == 0:
                list_.append(i)

        return list_

    def spawn(self) -> bool:
        counter = random.choice([2, 4])
        found = False
        avail_choice = [0, 1, 2, 3]
        while not found and len(avail_choice) > 0:
            x = random.choice(avail_choice)
            if 0 in self.board[x]:
                y = random.choice(self.get_index_zero(self.board[x]))
                self.board[x][y] = counter
                self.score += counter
                found = True
            else:
                avail_choice.remove(x)

        return found

        # x = random.randint(0, 15)
        # print(x)
        # pos = self.find_space(x)
        # try:
        #     self.board[pos[0]][pos[1]] = counter
        #     self.score += counter
        #     return True
        # except TypeError:
        #     return False

    def shift(self, action):
        """Return whether the original is changed
        """
        b = self.board
        changed = False

        if action == 'l':
            row = 0
            while row < 4:
                if shift_all(b[row]):
                    changed = True
                row += 1

        elif action == 'r':
            row = 0
            while row < 4:
                new_lst = [b[row][3], b[row][2], b[row][1], b[row][0]]
                if shift_all(new_lst):
                    changed = True
                for i in range(4):
                    b[row][i] = new_lst[3 - i]
                row += 1

        elif action == 'u':
            col = 0
            while col < 4:
                new_lst = [b[0][col], b[1][col], b[2][col], b[3][col]]
                if shift_all(new_lst):
                    changed = True
                for i in range(4):
                    b[i][col] = new_lst[i]
                col += 1

        elif action == 'd':
            col = 0
            while col < 4:
                new_lst = [b[3][col], b[2][col], b[1][col], b[0][col]]
                if shift_all(new_lst):
                    changed = True
                for i in range(4):
                    b[i][col] = new_lst[3 - i]
                col += 1

        # print(self)
        return changed

    def start(self):
        # cont = True
        print(self)
        while True:
            action = input('Enter l, r, u, d to perform an action:')
            if self.shift(action):
                if self.fail_fast():
                    return 'GameOver'
                self.spawn()

    def fail_fast(self):
        find_zero = False
        for row in self.board:
            for col in row:
                if col == 0:
                    find_zero = True
        if find_zero:
            return False

        if not find_zero:
            fail = True
            for i in range(3):
                for j in range(3):
                    val = self.board[i][j]
                    if self.board[i][j + 1] == val or \
                            self.board[i + 1][j] == val:
                        fail = False

            for j_ in range(3):
                if self.board[3][j_] == self.board[3][j_ + 1]:
                    fail = False

            for i_ in range(3):
                if self.board[i_][3] == self.board[i_ + 1][3]:
                    fail = False

            return fail

    # def count_score(self):
    #     s = 0
    #     for i in self.board:
    #         for j in i:
    #             s += j
    #
    #     return j


# def move_piece(lst, pos):
# if lst[pos] == 0:
#     return None
# elif pos == 0:
#     return None
# elif lst[pos - 1] == 0:
#     lst[pos - 1], lst[pos] = lst[pos], 0
#     move_piece(lst, pos - 1)
# elif lst[pos - 1] == lst[pos]:
#     lst[pos - 1], lst[pos] = lst[pos] * 2, 0
#     move_piece(lst, pos - 1)


def shift_all(lst):
    """
    >>> lst = [0, 10, 20, 10]
    >>> shift_all(lst)
    True
    >>> lst
    [10, 20, 10, 0]
    >>> lst1 = [0, 0, 10, 10]
    >>> shift_all(lst1)
    True
    >>> lst1
    [20, 0, 0, 0]
    >>> lst2 = [0, 20, 10, 10]
    >>> shift_all(lst2)
    True
    >>> lst2
    [20, 20, 0, 0]
    >>> lst3 = [10, 5, 5, 1]
    >>> shift_all(lst3)
    True
    >>> lst3
    [10, 10, 1, 0]
    >>> lst4 = [1, 2, 3, 4]
    >>> shift_all(lst4)
    False
    >>> lst4
    [1, 2, 3, 4]
    """
    i = 1
    lst_copy = lst[:]
    merged = set()
    while i < 4:
        prev = i - 1
        while lst[prev] == 0 and prev > 0:
            prev -= 1
        if lst[prev] == 0:
            lst[prev], lst[i] = lst[i], 0
        elif lst[prev] == lst[i] and prev not in merged:
            lst[prev], lst[i] = 2 * lst[i], 0
            merged.add(prev)
        elif prev + 1 != i:
            lst[prev + 1], lst[i] = lst[i], 0
        i += 1

    return lst != lst_copy


g = Game()
g.spawn()

pygame.init()
WIDTH = 605
HEIGHT = 705
screen = pygame.display.set_mode([WIDTH, HEIGHT])
screen.fill((0, 75, 100))

color_dic = {
    0: (255, 255, 255),
    2: (240, 249, 145),
    4: (255, 255, 179),
    8: (225, 225, 34),
    16: (111, 169, 124),
    32: (168, 168, 16),
    64: (56, 160, 166),
    128: (153, 148, 194),
    256: (239, 53, 111),
    512: (249, 149, 51),
    1024: (153, 153, 255),
    2048: (255, 255, 204)
}

white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 128)
black = (0, 0, 0)
scale = 150
width_rect = 146
font = pygame.font.SysFont('calibri', 35)


def disp(lst):
    for i in range(4):
        for j in range(4):
            # print(lst[i][j])
            color = color_dic[lst[i][j]]
            pygame.draw.rect(screen, color,
                             pygame.Rect(5 + scale * j, 105 + scale * i,
                                         width_rect, width_rect))
            if lst[i][j] != 0:
                text = font.render(str(lst[i][j]), True, black, color)
                textRect = text.get_rect()
                textRect.center = (5 + scale * j + width_rect // 2,
                                   105 + scale * i + width_rect // 2)
                screen.blit(text, textRect)


def game_over():
    font = pygame.font.SysFont('calibri', 70)
    text = font.render('Game Over', True, black, white)
    textRect = text.get_rect()
    textRect.center = (WIDTH // 2, 50 + HEIGHT // 2)
    screen.blit(text, textRect)


running = True
LOSE = False
while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
            elif event.key == K_LEFT:
                if g.shift('l'):
                    g.spawn()
                    if g.fail_fast():
                        LOSE = True
            elif event.key == K_RIGHT:
                if g.shift('r'):
                    g.spawn()
                    if g.fail_fast():
                        LOSE = True
            elif event.key == K_UP:
                if g.shift('u'):
                    g.spawn()
                    if g.fail_fast():
                        LOSE = True
            elif event.key == K_DOWN:
                if g.shift('d'):
                    g.spawn()
                    if g.fail_fast():
                        LOSE = True
        elif event.type == pygame.QUIT:
            pygame.quit()

        text = font.render(f'Score: {g.score}', True, white, (0, 75, 100))
        textRect = text.get_rect()
        textRect.center = (WIDTH // 2, 100 // 2)
        screen.blit(text, textRect)

        disp(g.board)

        if LOSE:
            game_over()

        pygame.display.update()


if __name__ == '__main__':
    import doctest

    doctest.testmod()
