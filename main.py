#!/usr/bin/python
# -*- encoding: utf-8 -*-
#
# Copyright 2014 - Irving Prog
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://github.com/irvingprog/snake
import random

import pygame as pg


class Snake(object):

    def __init__(self):
        super(Snake, self).__init__()

        rect = pg.Rect(20, 20, 10, 10)
        self.head = Head(rect)
        self.body = []
        self.body.append(self.head)
        self.dire = self.head.dir

        self.positions = [(20, 20)]

    def get_dir(self):
        return self.head.dir

    def set_dir(self, n_dir):
        self.head.dir = n_dir

    dire = property(get_dir, set_dir)

    def control(self, key):
        if key == pg.K_DOWN and not self.dire == 'up':
            self.dire = "down"
        elif key == pg.K_UP and not self.dire == 'down':
            self.dire = "up"
        elif key == pg.K_LEFT and not self.dire == 'right':
            self.dire = "left"
        elif key == pg.K_RIGHT and not self.dire == 'left':
            self.dire = "right"

    def update(self, food):
        self.head.update()

        for index, b in enumerate(self.body):
            if index < len(self.body) - 1:
                self.body[index+1].rect.x = b.anterior['x']
                self.body[index+1].rect.y = b.anterior['y']

            b.anterior['x'] = b.rect.x
            b.anterior['y'] = b.rect.y

        for f in reversed(food):
            if self.head.rect.colliderect(f):
                food.remove(f)
                self.add_part()

    def add_part(self):
        if self.dire == 'down':
            x = self.body[-1].rect.x
            y = self.body[-1].rect.y - 10
        elif self.dire == 'up':
            x = self.body[-1].rect.x
            y = self.body[-1].rect.y + 10
        elif self.dire == 'left':
            x = self.body[-1].rect.x + 10
            y = self.body[-1].rect.y
        elif self.dire == 'right':
            x = self.body[-1].rect.x - 10
            y = self.body[-1].rect.y

        rect = pg.Rect(x, y, 10, 10)
        part = Cell(rect)
        self.body.append(part)

    def draw(self, screen):
        for b in self.body:
            b.draw(screen)


class Cell(object):
    def __init__(self, rect):
        super(Cell, self).__init__()
        self.color = (0, 0, 0)
        self.rect = rect
        self.anterior = {'x': rect.x, 'y': rect.x}

    def draw(self, screen):
        pg.draw.rect(screen, self.color, self.rect)


class Head(Cell):
    def __init__(self, rect):
        super(Head, self).__init__(rect)
        self.velocity = 1
        self.dir = "right"

    def update(self):
        if self.dir == 'down':
            self.rect.y += self.velocity * self.rect.width
        elif self.dir == "up":
            self.rect.y -= self.velocity * self.rect.width
        elif self.dir == "right":
            self.rect.x += self.velocity * self.rect.width
        elif self.dir == "left":
            self.rect.x -= self.velocity * self.rect.width


class GameScene(object):

    def __init__(self):
        self.cells = []

        for row in xrange(60):
            for column in xrange(100):
                rect = pg.Rect(column*10, row*10, 10, 10)
                self.cells.append(rect)

        self.snake = Snake()

        self.food = []

    def update(self):
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    exit()
                elif event.key == pg.K_c:
                    self.put_food()

                self.snake.control(event.key)

        self.snake.update(self.food)

    def put_food(self):
        x = random.randint(1, 80)
        y = random.randint(1, 60)
        rect = pg.Rect(x*10, y*10, 10, 10)
        self.food.append(rect)

    def draw(self, screen):
        for cell in self.cells:
            pg.draw.rect(screen, (255, 255, 255), cell)
            pg.draw.rect(screen, (0, 0, 0), cell, 1)

        self.snake.draw(screen)

        for f in self.food:
            pg.draw.rect(screen, (0, 0, 0), f)

        pg.display.flip()


def main():
    screen = pg.display.set_mode((800, 600))
    pg.display.set_caption('Snake')
    pg.init()
    clock = pg.time.Clock()

    scene = GameScene()

    while True:
        scene.update()
        scene.draw(screen)
        clock.tick(10)

if __name__ == '__main__':
    main()