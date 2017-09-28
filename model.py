class Model:
    def toDisplay(self):
        raise NotImplementedError

    def process(self):
        raise NotImplementedError

    def processKeys(self, keys):
        raise NotImplementedError


import random


class number:
    def __init__(self, value):
        value = int(value)
        self.v = value
        self.image = pygame.image.load('assets/' + str(self.v) + '.png').convert_alpha()

    def operate(self, n2):
        return self.v * n2.v

    def __str__(self):
        return str(self.v)

    def __eq__(self, other):
        if not other: return False
        return self.v == other.v

    def canOperate(self, n2):
        return self.v == n2.v

    def display(self):
        # fontsize = 14
        # fontcolor = (0, 0, 0)
        return self.image
        # font = pygame.font.SysFont('Andale Mono',fontsize)
        # return font.render(str(self.v), 1, fontcolor)


class grid:
    def __init__(self, size):
        self.grid = [[None for _ in range(size)] for _ in range(size)]
        self.s = size
        self.init()

    def init(self):
        # for l in range(0,1):
        #    for r in range(0,len(self.grid[l])):
        #        self.grid[l][r] = number(random.randint(1,3))
        pass

    def update(self):
        for l in range(0, len(self.grid) - 1):
            for r in range(0, len(self.grid[l])):
                if self.grid[l][r] == None and self.grid[l + 1][r] != None:
                    self.grid[l][r] = self.grid[l + 1][r]
                    self.grid[l + 1][r] = None
                    return 0
        for l in range(0, len(self.grid)):
            for r in range(0, len(self.grid[l])):
                if self.grid[l][r] != None:
                    v = self.grid[l][r].v
                    if r > 0 and r < len(self.grid[l]) - 1:
                        # print(l,r,"c",self.grid[l][r])
                        if (self.grid[l][r] == self.grid[l][r + 1] and
                                    self.grid[l][r] == self.grid[l][r - 1]):
                            # print(l,r)
                            self.grid[l][r] = None
                            self.grid[l][r + 1] = None
                            self.grid[l][r - 1] = None
                            return v * 10
                    if l > 0 and l < len(self.grid) - 1:
                        if (self.grid[l][r] == self.grid[l + 1][r] and
                                    self.grid[l][r] == self.grid[l - 1][r]):
                            self.grid[l][r] = None
                            self.grid[l + 1][r] = None
                            self.grid[l - 1][r] = None
                            return v * 10
                    if l > 0 and l < len(self.grid) - 1 and r > 0 and r < len(self.grid[l]) - 1:
                        if (self.grid[l + 1][r + 1] == self.grid[l][r] and
                                    self.grid[l - 1][r - 1] == self.grid[l][r]):
                            self.grid[l + 1][r + 1] = None
                            self.grid[l - 1][r - 1] = None
                            self.grid[l][r] = None
                            return v * 10
                        elif (self.grid[l + 1][r - 1] == self.grid[l][r] and
                                      self.grid[l][r] == self.grid[l - 1][r + 1]):
                            self.grid[l + 1][r - 1] = None
                            self.grid[l - 1][r + 1] = None
                            self.grid[l][r] = None
                            return v * 10
        return 0

    def addNumber(self, r, n):
        for l in range(len(self.grid) - 1, -1, -1):
            # for r in range(0,len(self.grid[l])):
            if self.grid[l][r] != None:
                if self.grid[l][r].canOperate(n):
                    self.grid[l][r] = number(self.grid[l][r].operate(n))
                    return True
                else:
                    if l + 1 < self.s:
                        self.grid[l + 1][r] = n
                        return True
                    else:
                        return False
            elif l == 0:
                self.grid[l][r] = n
                return True


import pygame
from pygame.locals import *
import math
from time import gmtime, strftime


class Trois(Model):
    def __init__(self):
        possibleNumbers = {1: 1, 2: 3, 4: 2, 5: 2, 16: 1, 25: 1}  # possible numbers and occurence (int)
        self.possibleNumbers = []
        for k, v in possibleNumbers.items():
            for _ in range(0, v): self.possibleNumbers.append(k)
        self.size = 6
        self.restart()

    def restart(self):
        self.g = grid(self.size)
        self.rowToInsert = 0
        self.numberToInsert = self.possibleNumbers[random.randint(0, len(self.possibleNumbers) - 1)]
        self.text = ""
        self.text2 = "Arrow to move. R to restart and save score."
        self.score = 0
        self.time = 60
        self.scorefile = 'scores'

    def insertNumber(self):
        ok = self.g.addNumber(self.rowToInsert, number(self.numberToInsert))
        if ok:
            self.numberToInsert = self.possibleNumbers[random.randint(0, len(self.possibleNumbers) - 1)]
            self.score += 1

    def process(self):
        self.time -= 1
        if self.time < 0:
            self.time = 60
            self.insertNumber()
        return True

    def processKeys(self, keysPressed):
        # if keysPressed[pygame.K_1]:
        #    ok=self.g.addNumber(self.rowToInsert,number(1))
        #    if ok: self.score+=1
        # elif keysPressed[pygame.K_2]:
        #    ok=self.g.addNumber(self.rowToInsert,number(2))
        #    if ok: self.score+=2
        # elif keysPressed[pygame.K_3]:
        #    ok=self.g.addNumber(self.rowToInsert,number(3))
        #    if ok: self.score+=3
        if keysPressed[pygame.K_DOWN]:
            self.insertNumber()
            self.time = 60
        if keysPressed[pygame.K_r]:
            f = open(self.scorefile, 'a')
            f.write(strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ' ' + str(self.score) + '\n')
            f.close()
            self.restart()
        elif keysPressed[pygame.K_LEFT]:
            self.rowToInsert = max(0, self.rowToInsert - 1)
        elif keysPressed[pygame.K_RIGHT]:
            self.rowToInsert = min(self.size-1, self.rowToInsert + 1)
        return True

    def toDisplay(self):
        rectSize = 30
        initialx = 60
        initialy = 185
        fontsize = 25
        fontcolor = (0, 0, 0)
        font = pygame.font.SysFont('Ubuntu Bold', fontsize)
        blittable = [[font.render(self.text, 1, fontcolor), (16, 250)],
                     [font.render(self.text2, 1, fontcolor), (16, 250 + fontsize)]]
        grid = self.g.grid

        self.score += self.g.update()
        self.text = "Score=" + str(self.score) + ' Time=' + str(math.ceil(self.time / 20))

        for line in range(0, len(grid)):
            for row in range(0, len(grid[line])):
                if row == self.rowToInsert:
                    blittable.append([number(self.numberToInsert).display(),
                                      (initialx + row * rectSize, initialy - (len(grid)) * rectSize)])
                if grid[line][row] != None:
                    blittable.append([grid[line][row].display(),
                                      (initialx + row * rectSize, initialy + len(grid) - line * rectSize)])
                else:
                    # +str(line)+','+str(row)
                    blittable.append([font.render(" .", 1, fontcolor),
                                      (initialx + row * rectSize, initialy + len(grid) - line * rectSize)])

        return blittable
