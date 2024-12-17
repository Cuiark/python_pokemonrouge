import pygame
from pygame.locals import *

# 初始化 Pygame
pygame.init()

# 设置窗口大小
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("宝可梦游戏")

# 定义颜色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

# 定义字体
font = pygame.font.Font("ariblk.ttf")

# 按钮类
class Button:
    def __init__(self, x, y, w, h, text, action=None):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = BLUE
        self.text = text
        self.action = action

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        text_surf = font.render(self.text, True, WHITE)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def is_clicked(self, event):
        if event.type == MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                if self.action:
                    self.action()

# 示例按钮的动作
def start_game():
    print("游戏开始！")

# 创建按钮
start_button = Button(300, 200, 200, 50, "Start Game", start_game)

# 游戏主循环
running = True
while running:
    screen.fill(WHITE)
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == MOUSEBUTTONDOWN:
            if start_button.is_clicked(event):
                pass
    # 绘制按钮
    start_button.draw(screen)

    pygame.display.flip()

pygame.quit()
