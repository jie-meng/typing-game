import pygame
from pygame import Surface

class StartScene:
    def __init__(self, screen: Surface, clock):
        self.screen: Surface = screen
        self.clock = clock

        self.start_button_rect = pygame.Rect(self.screen.get_width() // 2 - 100, 200, 200, 50)
        self.highscore_button_rect = pygame.Rect(self.screen.get_width() // 2 - 100, 300, 200, 50)
        
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN: 
                    return 'game'
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    pos = pygame.mouse.get_pos()
                    if self.start_button_rect.collidepoint(pos):
                        return 'game'
                    elif self.highscore_button_rect.collidepoint(pos):
                        return 'highscore'

            self.screen.fill((255, 255, 255))

            font = pygame.font.Font(None, 36)
            start_button_text = font.render("Start Game", True, (0, 0, 0))
            highscore_button_text = font.render("Highscore", True, (0, 0, 0))

            pygame.draw.rect(self.screen, (0, 255, 0), self.start_button_rect)
            self.screen.blit(start_button_text, (self.screen.get_width() // 2 - start_button_text.get_width() // 2,
                                                 self.start_button_rect.centery - start_button_text.get_height() // 2))

            pygame.draw.rect(self.screen, (0, 255, 0), self.highscore_button_rect)
            self.screen.blit(highscore_button_text, (self.screen.get_width() // 2 - highscore_button_text.get_width() // 2,
                                                     self.highscore_button_rect.centery - highscore_button_text.get_height() // 2))

            pygame.display.update()
            self.clock.tick(30)
