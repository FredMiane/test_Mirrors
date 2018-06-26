import copy
import sys
import os
from enum import Enum
import numpy as np


class Direction(Enum):
    Xplus = 0  # unknow state at start
    Xminus = 1  # sensor initialized
    Yplus = 2  # running measurement
    Yminus = 3  # in low power mode if needed


# contants
MAX_SIZE = 1000000
MAX_MIRRORS = 200000


class Safe:
    currentDirection = Direction.Xplus
    currentX = -1
    currentY = 0

    isOpen = False

    cpt_open_45d = 0
    cpt_open_315d = 0

    maxX = 0
    maxY = 0

    firstX = 0
    firstY = 0

    safeArray = np.zeros((1, 1))

    def redirectFrom45dMirror(self):
        if self.currentDirection == Direction.Xplus:
            self.currentDirection = Direction.Yplus
        elif self.currentDirection == Direction.Xminus:
            self.currentDirection = Direction.Yminus
        elif self.currentDirection == Direction.Yplus:
            self.currentDirection = Direction.Xplus
        else:  # currentDirection == Direction.Yminus:
            self.currentDirection = Direction.Xminus

    def redirectFromd315Mirror(self):
        if self.currentDirection == Direction.Xplus:
            self.currentDirection = Direction.Yminus
        elif self.currentDirection == Direction.Xminus:
            self.currentDirection = Direction.Yplus
        elif self.currentDirection == Direction.Yplus:
            self.currentDirection = Direction.Xminus
        else:  # currentDirection == Direction.Yminus:
            self.currentDirection = Direction.Xplus

    def move(self):
        if self.currentDirection == Direction.Xplus:
            self.currentX += 1
        elif self.currentDirection == Direction.Xminus:
            self.currentX -= 1
        elif self.currentDirection == Direction.Yplus:
            self.currentY += 1
        else:  # currentDirection == Direction.Yminus:
            self.currentY -= 1

        if self.currentX == self.maxX or self.currentX < 0 or self.currentY == self.maxY or self.currentY < 0:
            return True
        return False

    def cleanArray(self):
        # clean array
        for x in range(0, self.maxX):
            for y in range(0, self.maxY):
                if self.safeArray[x][y] == 3:
                    self.safeArray[x][y] = 0

    def resolve(self):
        exit = False

        self.currentX = 0
        self.currentY = 0
        self.isOpen = False
        self.currentDirection = Direction.Xplus

        while exit is False:
            # try to move
            exit = self.move()

            if exit is False:
                if self.safeArray[self.currentX][self.currentY] == 1:
                    self.redirectFrom45dMirror()

                elif self.safeArray[self.currentX][self.currentY] == 2:
                    self.redirectFromd315Mirror()

                else:
                    self.safeArray[self.currentX][self.currentY] = 3
            else:
                # Check the beam exit to bottom left
                if self.currentX == self.maxX and self.currentY == self.maxY-1 and self.currentDirection == Direction.Xplus:
                    self.isOpen = True
                    # print("Openned!")
                else:
                    self.isOpen = False

    def run(self):
        # check if Openned without adding a mirror
        # print("Try to openned without adding mirror...")
        self.resolve()
        if self.isOpen is True:
            print("0")
            return

        # try to add a 45d mirror
        # print("try to open with adding a 45d mirror...")
        for x in range(0, self.maxX):
            for y in range(0, self.maxY):
                self.cleanArray()
                if self.safeArray[x][y] == 0:
                    self.safeArray[x][y] = 1
                    self.resolve()
                    if self.isOpen is True:
                        self.cleanArray()
                        # print("Openned with 45d mirror in x=" + repr(x) + " y=" +repr(y))
                        self.safeArray[x][y] = 0
                        self.cpt_open_45d += 1
                        self.firstX = x
                        self.firstY = y
                    else:
                        self.safeArray[x][y] = 0

        # try to add a 315d mirror
        # print("try to open with adding a 315d mirror...")
        for x in range(self.maxX):
            for y in range(self.maxY):
                self.cleanArray()
                if self.safeArray[x][y] == 0:
                    self.safeArray[x][y] = 2
                    self.resolve()
                    if self.isOpen is True:
                        self.cleanArray()
                        # print("Openned with 315d mirror in x=" + repr(x) + " y=" +repr(y))
                        self.safeArray[x][y] = 0
                        self.cpt_open_315d += 1
                    else:
                        self.safeArray[x][y] = 0

        if self.cpt_open_45d == 0 and self.cpt_open_315d == 0:
            print("impossible")
        else:
            print(repr(self.cpt_open_45d + self.cpt_open_315d) + " " + repr(self.firstX) + " " + repr(self.firstY))

    def __init__(self, input_file_path):
        with open(input_file_path, 'r') as conf:

            # read first line with r c m n
            [r, c, m, n] = conf.readline()[:-1].split(' ')
            [r, c, m, n] = [int(x) for x in [r, c, m, n]]

            # check if mirror
            if m == 0 and n == 0:
                print("impossible")
                quit()

            if r > MAX_SIZE or c > MAX_SIZE:
                print("Row or column size is incorrect.")
                quit()

            if m > MAX_MIRRORS or n > MAX_MIRRORS:
                print("Mirror position is incorrect.")
                quit()

            # redim safeArray
            self.safeArray = np.zeros((c, r))

            self.maxX = c
            self.maxY = r

            for _ in range(m):
                coordinate = conf.readline()[:-1].split(' ')
                [x, y] = [int(z) for z in coordinate]
                self.safeArray[y-1][x-1] = 2

            for _ in range(n):
                coordinate = conf.readline()[:-1].split(' ')
                [x, y] = [int(z) for z in coordinate]
                self.safeArray[y-1][x-1] = 1

            # print(self.safeArray.transpose())


if __name__ == "__main__":

    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Wrong numbers of parameters")
        quit()

    # current_file_path = __file__
    # current_file_dir = os.path.dirname(__file__)
    # input_file_path = os.path.join(current_file_dir, "input1")

    safe = Safe(sys.argv[1])
    safe.run()
