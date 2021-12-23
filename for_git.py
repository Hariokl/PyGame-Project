import pygame
if __name__ == '__main__':
    pygame.init()
    width, height = 1200, 800
    screen = pygame.display.set_mode((width, height))
    mouse_sprite = pygame.sprite.Group()
    clock = pygame.time.Clock()


    class Game:
        def __init__(self):
            self.page = 'menu'
            self.mouse = Mouse(self)
            self.play_button_rect = pygame.Rect(width//2-200, height//2, 400, 120)
            self.settings_button_rect = pygame.Rect(width-150, height-150, 100, 100)
            self.settings_screen = pygame.Surface((width, height)).convert_alpha()
            self.settings_screen.fill((0, 0, 0, 100))
            self.settings_exit_button_rect = pygame.Rect(width//3*2-30, height//8, 80, 80)

        def update(self):
            if self.page == 'menu':
                self.menu()
            if self.page == 'gameplay':
                self.gameplay()
            if self.page == 'settings':
                self.settings()

        def menu(self):
            screen.fill((20, 20, 20))
            #   play button
            pygame.draw.rect(screen, (0, 200, 0), self.play_button_rect)
            play_button_text = pygame.font.Font(None, 100).render('Play', True, (0, 100, 0))
            play_button_text_rect = play_button_text.get_rect()
            play_button_text_rect.x = width//2-play_button_text_rect.width//2
            play_button_text_rect.top = height//2+play_button_text_rect.height//2
            screen.blit(play_button_text, play_button_text_rect)
            #   settings button
            pygame.draw.rect(screen, (100, 100, 100), self.settings_button_rect)


        def gameplay(self):
            screen.fill((20, 20, 20))

        def settings(self):
            self.menu()
            pygame.draw.rect(self.settings_screen, (80, 80, 80),
                             ((width//3-50, height//8), (width//3+100, height//8*6)), 0)
            pygame.draw.rect(self.settings_screen, (150, 0, 0), self.settings_exit_button_rect)
            screen.blit(self.settings_screen, (0, 0))



    class Mouse(pygame.sprite.Sprite):
        def __init__(self, parent):
            super().__init__()
            pygame.mouse.set_visible(False)
            self.parent = parent
            self.image = pygame.Surface((10, 10), pygame.SRCALPHA, 32)
            pygame.draw.circle(self.image, (50, 250, 0), (5, 5), 5)
            self.rect = pygame.Rect(0, 0, 10, 10)
            self.mask = pygame.mask.from_surface(self.image)
            mouse_sprite.add(self)

        def update(self, *args):
            if args and args[0].type == pygame.MOUSEMOTION:
                self.rect.topleft = event.pos[0] - 5, event.pos[1] - 5

        def clicked(self, pos):
            if self.parent.page == 'menu':
                if self.rect.colliderect(self.parent.play_button_rect):
                    self.parent.page = 'gameplay'
                if self.rect.colliderect(self.parent.settings_button_rect):
                    self.parent.page = 'settings'
            if self.parent.page == 'settings':
                if self.rect.colliderect(self.parent.settings_exit_button_rect):
                    self.parent.page = 'menu'


    game = Game()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEMOTION:
                mouse_sprite.update(event)
            if event.type == pygame.MOUSEBUTTONUP:
                game.mouse.clicked(event.pos)
        game.update()
        mouse_sprite.draw(screen)
        mouse_sprite.update()
        pygame.display.set_caption(str(int(clock.get_fps())))
        pygame.display.update()
        clock.tick(60)
    pygame.quit()