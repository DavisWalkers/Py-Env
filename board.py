#
#   Definitions:
#       0 - empty space, 1 - player, 2 - wall, 3 - pit, 4 - end point
#   Actions:
#       0 - down, 1 - right, 2 - up, 3 - left

import random
import numpy as np


class BoardException(Exception):

    def __init__(self, msg="Cannot create a board with current conditions"):
        self.msg = msg


class Board(object):

    def __init__(self, size=(4, 3), walls=2, pits=1):
        self.walls = walls
        self.pits = pits
        self.done = False
        self.size = size
        self.board = None
        self.player_pos = None
        self.end_pos = None
        self.reward = 0
        self.max_iter = 10000

    def new_board(self):
        self.done = False
        self.board = np.zeros((self.size[0], self.size[1]), dtype=int)

        free_cells = [(i, j) for i in range(self.size[0]) for j in range(self.size[1])]

        if len(free_cells) < (self.walls + self.pits + 2):
            raise BoardException()

        player_cell = random.choice(free_cells)
        self.board[player_cell] = 1
        free_cells.remove(player_cell)
        self.player_pos = player_cell

        end_point_cell = random.choice(free_cells)

        while np.math.dist(player_cell, end_point_cell) < (min(self.size[0], self.size[1]) - 1) / 2:
            end_point_cell = random.choice(free_cells)
        else:
            self.board[end_point_cell] = 4
            self.end_pos = end_point_cell
            free_cells.remove(end_point_cell)

        num_iter = 0
        cell = None
        for wall in range(self.walls):
            cell = random.choice(free_cells)
            self.board[cell] = 2
            if self.__valid_board__():
                free_cells.remove(cell)
                self.board[cell] = 2
                num_iter = 0
                continue
            else:
                self.board[cell] = 0
                wall -= 1
                if wall < 0:
                    wall = 0
            num_iter += 1
            if num_iter > self.max_iter:
                raise BoardException()

        num_iter = 0
        for pit in range(self.pits):
            cell = random.choice(free_cells)
            self.board[cell] = 3
            if self.__valid_board__():
                free_cells.remove(cell)
                self.board[cell] = 3
                num_iter = 0
                continue
            else:
                self.board[cell] = 0
                pit -= 1
                if pit < 0:
                    pit = 0
            num_iter += 1
            if num_iter > self.max_iter:
                raise BoardException()

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
                    self.reward = 0
                elif self.board[pos_y, pos_x] == 4:
                    self.board[pos_y, pos_x] = 1
                    self.board[self.player_pos] = 0
                    self.player_pos = (pos_y, pos_x)
                    self.done = True
                    self.reward = 1
                elif self.board[pos_y, pos_x] == 3:
                    self.board[pos_y, pos_x] = 1
                    self.board[self.player_pos] = 0
                    self.player_pos = (pos_y, pos_x)
                    self.done = True
                    self.reward = -1

        return self.reward, self.done

    def state(self):
        return self.player_pos

    def copy(self, other):
        if (self.size[0] == other.size[0]) and (self.size[1] == other.size[1]):
            self.board = np.zeros((other.size[0], other.size[1]), dtype=int)
            for i in range(other.size[0]):
                for j in range(other.size[1]):
                    self.board[i, j] = other.board[i, j]
            self.player_pos = other.player_pos
            self.end_pos = other.end_pos
        else:
            raise BoardException(msg="Sizes are not the same")

    def __valid_board__(self):
        num_vertices = self.size[0] * self.size[1]
        graph = np.zeros((num_vertices, num_vertices), dtype=int)

        vertices = [(i, j) for i in range(self.size[0]) for j in range(self.size[1])]

        for vert_1 in range(num_vertices - 1):
            for vert_2 in range(vert_1 + 1, num_vertices):
                if vert_1 == vert_2:
                    continue
                elif (abs((vertices[vert_1][0] + vertices[vert_1][1]) -
                          (vertices[vert_2][0] + vertices[vert_2][1])) == 1) \
                        and ((abs(vertices[vert_1][0] - vertices[vert_2][0]) == 1)
                             or (abs(vertices[vert_1][0] - vertices[vert_2][0]) == 0)) \
                        and ((abs(vertices[vert_1][1] - vertices[vert_2][1]) == 1)
                             or (abs(vertices[vert_1][1] - vertices[vert_2][1]) == 0)):
                    if (self.board[vertices[vert_1]] != 2) and (self.board[vertices[vert_2]] != 2)\
                            and (self.board[vertices[vert_1]] != 3) and (self.board[vertices[vert_2]] != 3):
                        graph[vert_1, vert_2] = 1
                        graph[vert_2, vert_1] = 1

        end_vert = [i for i, vert in enumerate(vertices)
                    if (vert[0] == self.end_pos[0]) and (vert[1] == self.end_pos[1])][0]

        player_vert = [i for i, vert in enumerate(vertices)
                       if (vert[0] == self.player_pos[0]) and (vert[1] == self.player_pos[1])][0]

        queue = [player_vert]
        visited = [player_vert]

        while queue:
            node = queue.pop(0)

            for vert in range(num_vertices):
                if vert not in visited:
                    if graph[vert, node] == 1:
                        if vert == end_vert:
                            return True
                        visited.append(vert)
                        queue.append(vert)

        return False
