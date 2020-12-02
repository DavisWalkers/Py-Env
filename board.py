#
#   Definitions:
#       0 - empty space, 1 - player, 2 - wall, 3 - pit, 4 - end point
#   Actions:
#       0 - down, 1 - right, 2 - up, 3 - left

import random
import numpy as np


class Board(object):

    def __init__(self, size=(4, 3), walls=2, pits=1):
        self.walls = walls
        self.pits = pits
        self.done = False
        self.win = False
        self.size = size
        self.board = None
        self.player_pos = None

    def new_board(self):
        self.board = np.zeros((self.size[0], self.size[1]), dtype=int)

        num_walls = self.walls
        while num_walls:
            pos_x = random.randint(0, self.size[1] - 1)
            pos_y = random.randint(0, self.size[0] - 1)

            if self.board[pos_y, pos_x] == 0:
                self.board[pos_y, pos_x] = 2
                num_walls -= 1
            else:
                continue

        num_pits = self.pits
        while num_pits:
            pos_x = random.randint(0, self.size[1] - 1)
            pos_y = random.randint(0, self.size[0] - 1)

            if self.board[pos_y, pos_x] == 0:
                self.board[pos_y, pos_x] = 3
                num_pits -= 1
            else:
                continue

        player_pos_x = random.randint(0, self.size[1] - 1)
        player_pos_y = random.randint(0, self.size[0] - 1)

        while self.board[player_pos_y, player_pos_x] != 0:
            player_pos_x = random.randint(0, self.size[1] - 1)
            player_pos_y = random.randint(0, self.size[0] - 1)
        else:
            self.board[player_pos_y, player_pos_x] = 1
            self.player_pos = (player_pos_y, player_pos_x)

        end_pos_x = random.randint(0, self.size[1] - 1)
        end_pos_y = random.randint(0, self.size[0] - 1)

        while (np.sqrt((end_pos_x - player_pos_x) ** 2 +
                       (end_pos_y - player_pos_y) ** 2) < abs(self.size[0] - self.size[1])) or \
              (self.board[end_pos_y, end_pos_x] != 0):
            end_pos_x = random.randint(0, self.size[1] - 1)
            end_pos_y = random.randint(0, self.size[0] - 1)
        else:
            self.board[end_pos_y, end_pos_x] = 4

    def show(self):
        if self.board is not None:
            for i in range(-1, self.size[0] + 1):
                if i == -1 or i == self.size[0]:
                    for j in range(self.size[1] + 2):
                        if j == 0 or j == self.size[1] + 1:
                            print("+", end=" ")
                        else:
                            print("-", end=" ")
                else:
                    for j in range(-1, self.size[1] + 1):
                        if j == -1 or j == self.size[1]:
                            print("|", end=" ")
                        else:
                            if self.board[i, j] == 0:
                                print(" ", end=" ")
                            elif self.board[i, j] == 1:
                                print("P", end=" ")
                            elif self.board[i, j] == 2:
                                print("#", end=" ")
                            elif self.board[i, j] == 3:
                                print("O", end=" ")
                            elif self.board[i, j] == 4:
                                print("$", end=" ")
                print()
        else:
            print("The board has not been created")

    def step(self, action):
        if not self.done:
            if action == 0:
                pos_x = self.player_pos[1]
                pos_y = self.player_pos[0] + 1
                if pos_y == self.size[0]:
                    pos_y -= 1
            elif action == 1:
                pos_x = self.player_pos[1] + 1
                pos_y = self.player_pos[0]
                if pos_x == self.size[1]:
                    pos_x -= 1
            elif action == 2:
                pos_x = self.player_pos[1]
                pos_y = self.player_pos[0] - 1
                if pos_y == -1:
                    pos_y += 1
            elif action == 3:
                pos_x = self.player_pos[1] - 1
                pos_y = self.player_pos[0]
                if pos_x == -1:
                    pos_x += 1
            else:
                raise Exception("Wrong action")

            if self.board is not None:
                if self.board[pos_y, pos_x] == 0:
                    self.board[pos_y, pos_x] = 1
                    self.board[self.player_pos] = 0
                    self.player_pos = (pos_y, pos_x)
                elif self.board[pos_y, pos_x] == 4:
                    self.board[pos_y, pos_x] = 1
                    self.board[self.player_pos] = 0
                    self.player_pos = (pos_y, pos_x)
                    self.done = True
                    self.win = True
                elif self.board[pos_y, pos_x] == 3:
                    self.board[pos_y, pos_x] = 1
                    self.board[self.player_pos] = 0
                    self.player_pos = (pos_y, pos_x)
                    self.done = True
                    self.win = False

        return self.player_pos, self.done, self.win
