
import sys
import pygame
from pygame.locals import QUIT

class View:
    def __init__(self):
        pygame.init()
        window = pygame.display.set_mode((800, 600))
        pygame.display.set_caption('ACO Simulator')
        window.fill((255, 255, 255))

        # 宣告 font 文字物件
        head_font = pygame.font.SysFont(None, 60)
        # 渲染方法會回傳 surface 物件
        text_surface = head_font.render('Hello World!', True, (0, 0, 0))
        # blit 用來把其他元素渲染到另外一個 surface 上，這邊是 window 視窗
        window.blit(text_surface, (10, 10))

        # 更新畫面，等所有操作完成後一次更新（若沒更新，則元素不會出現）
        pygame.display.update()
