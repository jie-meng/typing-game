import sys
import pygame
import random
from pygame import Surface

class GameScene:
    def __init__(self, screen: Surface, clock):
        self.screen: Surface = screen
        self.clock = clock
        self.font = pygame.font.Font(None, 30)
        self.player_name = ''
        self.score = 0

        self.lives = 3
        self.alphabet_list = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890')
        self.alphabet_speed = 1
        self.alphabet_size = 36
        self.drop_rate = 1000  # in milliseconds
        self.next_drop_time = pygame.time.get_ticks() + self.drop_rate
        self.alphabets = []
        self.min_speed = 30
        self.max_speed = 60

        # self.explosion_img = pygame.image.load('res/images/explosion.png')
        self.beat_sound = pygame.mixer.Sound('res/sounds/explosion.wav')
        self.hurt_sound = pygame.mixer.Sound('res/sounds/ugh.wav')

        self.setup()

    def setup(self):
        # initialize game variables and objects
        # 设置背景颜色
        self.screen.fill((255, 255, 255))

        # 设置字体
        self.font = pygame.font.Font(None, 36)

        # 初始化变量
        self.score = 0
        self.lives = 3
        self.alphabets = []
        self.game_over = False
    
    def play_effect_beat(self, alphabet):
        self.beat_sound.play()
    
    def play_effect_hurt(self, alphabet):
        self.hurt_sound.play()

    def handle_events(self, events):
        # handle events such as key presses
        for event in events:
            if event.type == pygame.KEYDOWN:
                key = event.unicode.lower()  # get lowercase character from event
                for alphabet in self.alphabets:
                    if alphabet['char'].lower() == key:
                        alphabet['remove'] = True
                        self.score += 1 
                        self.play_effect_beat(alphabet)

    def update(self, dt):
        # 在合适的位置展示待下落的字符
        self.screen.fill((255, 255, 255))

        # 在左上角显示生命值
        lives_text = self.font.render(f'Lives: {self.lives}', True, (255, 0, 0))
        self.screen.blit(lives_text, (10, 10))

        # 在右上角显示得分
        score_text = self.font.render(f'Score: {self.score}', True, (0, 255, 0))
        score_rect = score_text.get_rect()
        score_rect.topright = (self.screen.get_width() - 10, 10)
        self.screen.blit(score_text, score_rect)

        if len(self.alphabets) == 0:
            return

        for alphabet in self.alphabets:
            # x, y, char, speed = alphabet
            text = self.font.render(alphabet['char'], True, (0, 0, 255))
            text_rect = text.get_rect()
            text_rect.center = (alphabet['x'], alphabet['y'])
            self.screen.blit(text, text_rect)

        # 更新待下落字符的位置
        for i in range(len(self.alphabets)):
            y = self.alphabets[i]['y']
            y += self.alphabets[i]['speed'] * dt
            self.alphabets[i]['y'] = y

            # 如果字母超出屏幕底部，就将其移除
            if y >= self.screen.get_height():
                self.remove_alphabet(self.alphabets[i])
        
        # remove all alphabets that have been marked as to be removed
        self.alphabets = [a for a in self.alphabets if not a.get('remove')]

    def run(self):
        while self.lives > 0:
            # delay to control frame rate
            dt = self.clock.tick(60) / 1000

            # handle events
            events = pygame.event.get()
            self.handle_events(events)

            # update game state
            now = pygame.time.get_ticks()
            if now >= self.next_drop_time:
                self.drop_alphabet()
                self.next_drop_time = now + self.drop_rate

            self.update(dt)

            # update screen
            pygame.display.flip()

        # game over, show input box for player name
        return self.show_input_box()

    def drop_alphabet(self):
        # 随机选择一个字母或数字
        character = random.choice(self.alphabet_list)

        # 随机选择一个起始位置
        x = random.randint(self.alphabet_size, self.screen.get_width() - self.alphabet_size)
        y = -self.alphabet_size

        # 随机选择一个速度
        speed = random.randint(self.min_speed, self.max_speed)

        # 添加字母或数字到列表
        self.alphabets.append({'char': character, 'x': x, 'y': y, 'speed': speed, 'remove': False})

    def remove_alphabet(self, alphabet):
        alphabet['remove'] = True
        self.lives -= 1
        self.play_effect_hurt(alphabet)

    def show_input_box(self):
        # 清空键盘输入
        pygame.key.set_repeat()
        self.input_box_text = "" 

        # 展示游戏结束界面
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        # 返回到游戏主菜单
                        return 'start_game'

            # 展示游戏结束界面
            self.screen.fill((255, 255, 255))

            # 游戏结束界面的字体和颜色设置
            font = pygame.font.Font(None, 100)
            text_surface = font.render("GAME OVER", True, (0, 0, 0))
            text_rect = text_surface.get_rect()
            text_rect.center = (self.screen.get_width() // 2, self.screen.get_height() // 3)
            self.screen.blit(text_surface, text_rect)

            # 展示玩家得分
            font = pygame.font.Font(None, 50)
            text_surface = font.render("SCORE: " + str(self.score), True, (0, 0, 0))
            text_rect = text_surface.get_rect()
            text_rect.center = (self.screen.get_width() // 2, self.screen.get_height() // 2)
            self.screen.blit(text_surface, text_rect)

            pygame.display.flip()
            self.clock.tick(60)
    
    