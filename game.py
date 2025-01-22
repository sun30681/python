#!/usr/bin/python
# -*- coding: UTF-8 -*-

import pygame
import sys

# 初始化 Pygame
pygame.init()

# 设置屏幕大小
screen = pygame.display.set_mode((800, 600))

# 加载图像
ball = pygame.image.load('ball.png')

# 调整图像大小
ball = pygame.transform.scale(ball, (50, 50))  # 将图像缩小到 50x50 像素
ballrect = ball.get_rect()

# 定义速度
speed = [2, 2]

# 主循环
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    # 移动小球
    ballrect = ballrect.move(speed)
    if ballrect.left < 0 or ballrect.right > screen.get_width():
        speed[0] = -speed[0]
    if ballrect.top < 0 or ballrect.bottom > screen.get_height():
        speed[1] = -speed[1]

    # 填充背景颜色
    screen.fill((0, 0, 0))

    # 在屏幕上绘制小球
    screen.blit(ball, ballrect)

    # 更新显示
    pygame.display.flip()
