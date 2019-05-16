# 导入pygame库，这一步能让你使用库里提供的功能
import pygame
from pygame.locals import *
import math   # 因为需要计算旋转的角度
import random # 因为需要用到随机的功能

# 初始化pygame，设置展示窗口
pygame.init()
width, height = 640, 480
screen = pygame.display.set_mode((width, height))

# 不停地循环执行接下来的部分
# running变量会跟踪游戏是否结束，
# exitcode变量会跟踪玩家是否胜利。
running = True
while running:
	# 在给屏幕画任何东西之前用黑色进行填充
	screen.fill(0)
	screen.blit("hello world", (0, 30))

	screen.blit(health_img, (health1+8, 8))
	# 更新屏幕
	pygame.display.flip()

	# pygame.quit()
	# exit()


