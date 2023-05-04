import pygame
import sys
from src.scenes.start_scene import StartScene
from src.scenes.game_scene import GameScene

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


if __name__ == "__main__":
    # 启动 pygame
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    # 调用开始场景
    next_scene = "start_game"
    while next_scene:
        if next_scene == 'start_game':
            next_scene = StartScene(screen, clock).run()
        elif next_scene == "game":
            next_scene = GameScene(screen, clock).run()
        elif next_scene == "high_score":
            # 进入最高分场景
            pass
        elif next_scene == "game_over":
            # 进入游戏结束场景
            pass
        else:
            pygame.quit()
            sys.exit()

    # 退出游戏
    pygame.quit()
    sys.exit()
