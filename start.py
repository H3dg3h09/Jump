#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/12/31 17:55
# @Author  : Aries
# @Site    :
# @File    : start.py
# @Software: PyCharm
from __future__ import unicode_literals
from pygame.locals import *
from random import randint, choice
from sys import exit
import time
import pygame
import math
class Game():

    def __init__(self):
        global WIDTH, HEIGHT, MIN_DIS, MAX_DIS
        WIDTH, HEIGHT = 640, 480
        MIN_DIS, MAX_DIS =  20, 120

        pygame.init()
        pygame.display.set_caption("JUMP")

        self.font = pygame.font.SysFont("fangsong", 24)
        self._is_GameOver = 0
        self.center_position = (WIDTH/2, HEIGHT*2/3)
        self.screen_size = (WIDTH, HEIGHT)
        self.screen = pygame.display.set_mode(self.screen_size, 0, 32)
        self.core = 0


        self.direction = -1
        self.next_p = Platform.init_pla(self.screen, self.center_position)
        self.stand_p = Platform.init_pla(self.screen, (self.center_position[0] + 60, self.center_position[1] + 60))
        self.init_position = [self.stand_p.position,self.stand_p.center]
        self.d = 60
        self.c =  Cir.init_cir(self.screen, (self.center_position[0] + self.stand_p.size / 2 + 60 , self.center_position[1] + self.stand_p.size/2 + 60)) #40是第二个方块的位移差

    def start(self):
        self.init_game()

        while True:
            event = pygame.event.wait()

            if event.type == QUIT:
                exit()
            if event.type == MOUSEBUTTONDOWN and event.dict['button'] == 1 and not self._is_GameOver:#鼠标左键:1
                t0 = time.time()
            if event.type == MOUSEBUTTONUP and event.dict['button'] == 1 and not self._is_GameOver:
                t1 = time.time()
                t = 10*(t1 - t0)
                print "time : %.1fs" % round(t,1)

                self.c.jump(t, self.direction)
                # 判定是否能继续游戏

                if not self.next_p.is_inside(self.c.postion):
                    self._is_GameOver = 1
                    self.gameover()

                if self.direction != self.c.old_direction:
                    self.c.postion = self.next_p.center


                self.core += 1
                self.create_new_plat(self.next_p.position) #生成一个新的平台，并将新平台画出来

            pygame.display.update()

    def create_new_plat(self, po):

        size = randint(0, 3)
        nx = randint(MIN_DIS, MAX_DIS)
        while nx < self.stand_p.get_size() + MIN_DIS:
            nx = randint(MIN_DIS, MAX_DIS)

        ny = -nx
        self.direction = choice([-1, 1])
        if self.direction == -1:  # 生成方向,-1:left, 1:right
            nx *= -1

        new_position = (po[0] + nx, po[1] + ny)

        self.stand_p.renovate_position(self.next_p.position)
        self.next_p.renovate_position(new_position)

        self.next_p.move_self(new_position, relative=False)
        self.next_p.draw_self(size ,auto_color=True)
        self.c.direction = self.direction



    def init_game(self):
        self.screen.fill((0,0,0))
        self.stand_p.draw_self()
        self.next_p.draw_self()
        self.c.draw_self()

    def gameover(self):

        font_height = self.font.get_linesize()
        text = "Game Over!"
        self.screen.blit(self.font.render(text, True, (255,255,255)),(WIDTH/3, HEIGHT/2))
        text = "Your core : %d" % self.core
        self.screen.blit(self.font.render(text, True, (255, 255, 255)), (WIDTH / 3, HEIGHT / 2 + font_height))


class Cir():
    def __init__(self, screen, position):
        """
        半径、(水平)速度、颜色、坐标
        :param radius: int
        :param v: int
        :param position: tuple
        """
        self.screen = screen
        self._radius = 8
        self.v0 = 4 #初始速度
        self.a = 2 #水平加速度
        self.v = self.v0 #当前速度
        self.postion = position #目前所在位置
        self.color = (255,255,255)
        self.old_direction = -1 #第一次向左跳
        self.direction = -1

    @classmethod
    def init_cir(cls, screen, position):
        """
        :param position: tuple
        """
        return cls(screen, position)

    def jump(self, t, direction):
        """
            根据跳跃时间、初始位置、跳跃方向，更新新的位置
            跳跃方向: 0:left , 1 :right
        """

        g = 9.8
        self.v = self.v0 + (self.a * t)/3
        jump_t = self.v*2 / g #跳跃的时间
        distance = self.v * jump_t
        temp = math.ceil(math.sqrt(2)*distance/2)
        new_x = temp if self.direction else -1*temp
        new_y = temp if self.direction else -1*temp

        self.move_self((new_x, new_y))
        self.old_direction = self.direction

    def move_self(self, m):
        new_x = int(math.ceil(self.postion[0] + m[0]))
        p = self.postion[0]

        for _ in xrange(abs(new_x - p)):
            self.postion = (self.postion[0] + self.direction*10, self.postion[1] - 1*10)
        self.draw_self()

    def draw_self(self):
        pygame.draw.circle(self.screen, self.color, self.postion, self._radius)


class Platform():
    def __init__(self, screen, pos_l, color):
        """
        坐标, size = one of [0,1,2,3]
        :param screen:
        :param position:
        :param color:
        """
        self.size = 30 + 2**4
        self.center = ((pos_l[0]+self.size)/2, (pos_l[1]+self.size)/2)
        self.screen = screen
        self.color = color
        self.position = pos_l

    def renovate_position(self, pos):
        self.center = ((self.position[0] + self.size) / 2, (self.position[1] + self.size) / 2)
        self.position = pos

    @classmethod
    def init_pla(cls, screen, pos_l):
        color = (randint(10,240), randint(10,240), randint(10,240))
        return cls(screen, pos_l, color)

    def draw_self(self, size=2, auto_color=False):
        self.size = 30 + 2**(size+2)

        color = (randint(10, 240), randint(10, 240), randint(10, 240)) \
                if auto_color else self.color

        self.rect = Rect(self.position, (self.size, self.size))
        pygame.draw.rect(self.screen, color, self.rect)

    def move_self(self, m, relative=True):
        if not relative:
            dx = m[0] - self.position[0]
            dy = m[1] - self.position[1]
        else:
            dx = m[0]
            dy = m[1]
            #相对移动
        self.rect = self.rect.move(dx, dy)

    def get_size(self):
        return  self.size

    @property
    def is_out(self):

        self._is_outsid = 0

        if self.rect.left > WIDTH or self.rect.left < 0 :
            self._is_outsid = 1
        if self.rect.height > HEIGHT or self.rect.height < 0:
            self._is_outsid = 1

        return self._is_outsid

    def is_inside(self, position):
        """
        :param position:
        :return:
        """
        return self.rect.collidepoint(position[0], position[1])

if __name__ == "__main__":
    g = Game()
    g.start()

