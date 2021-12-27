import math
import pygame
import random
import numpy as np
#import pathlib
######### yes, im really bad at english, so what? Just take it, please (;-;)
FPS = 60
if __name__ == '__main__':
    pygame.init()
    size = width, height = 1200, 800
    screen = pygame.display.set_mode(size)
    screen.fill((250, 250, 250))
    pygame.display.set_caption('Vsevolod Buzhinskiy :3')
    running = True
    value = 75
    list_of_possobility_to_go = np.array([[0 for _ in range(width//75)] for _ in range(height//75)])
    all_sprites = pygame.sprite.Group()
    towers_sprites = pygame.sprite.Group()
    enemies_sprites = pygame.sprite.Group()
    mouse_sprites = pygame.sprite.Group()
    polosa_sprites = pygame.sprite.Group()
    clock = pygame.time.Clock()


    def update_fps():
        font = pygame.font.SysFont("Arial", 18)
        fps = str(int(clock.get_fps()))
        fps_text = font.render(fps, 1, pygame.Color("coral"))
        return fps_text


    class Game:
        def __init__(self):
            self.screen_for_draw = pygame.Surface((width, height)).convert_alpha()    # idk how to name it, so let it go
            self.screen_for_draw.fill((0, 0, 0, 0))
            self.screen_for_upgr_built = pygame.Surface((width//3, height*2//3)).convert_alpha()  # idk how to name it either, so let it go, please, i wanna die
            self.screen_for_upgr_built.fill((0, 0, 0, 0))
            self.speed_up_button_rect = pygame.Rect(width*2//15, height//10*8, width//15, height//10)
            self.screen_for_many_feautures = pygame.Surface((width, height)).convert_alpha()
            self.screen_for_many_feautures.fill((0, 0, 0, 0))
            self.next_wave_button_rect = pygame.Rect(width // 30, height - height // 20 - height // 8, width // 12,
                                                     height // 8)
            #####   settings
            self.in_game_settings_open_button_rect = pygame.Rect(width // 60, height // 40, width // 12, height // 8)
            self.in_game_settings_screen = pygame.Surface((width, height)).convert_alpha()
            self.in_game_settings_screen.fill((0, 0, 0, 100))
            self.in_game_settings_close_button_rect = pygame.Rect(width * 2 // 3 - 80, height // 5 + 10,
                                                                  70, height // 10 - 10)
            self.in_game_settings_auto_next_wave_button_rect = pygame.Rect(width * 2 // 3 - 85, height // 10 * 3 + 45,
                                                                           width // 30, height // 20)  ### (width // 3 + 5, height // 10 * 3 + 10)
            self.auto_next_wave = False
            #####
            self.bool_to_go_to_next_wave = False
            self.map = Map()
            all_sprites.add(self.map)
            self.towers = []
            self.mouse = Mouse(self)
            self.clock = pygame.time.Clock()
            self.list_of_speeds = [0, 1, 2, 4]
            self.speed_of_game = 1
            self.time = 2
            self.wave = 1
            self.number_of_enemies = 10
            self.max_number_of_enemies = 10
            self.tot = 'Привет'
            self.enemies_list = []
            self.lifes = 10
            self.enemy_hp = 5
            self.coins = 200
            self.clicked_bui_upg_but = False
            print('ddddddddddddddddddd')
            self.font = pygame.font.Font(None, 40)
            self.font50 = pygame.font.Font(None, 50)
            self.build_upgr_timer = pygame.time.Clock()
            self.build_upgr_time = 0
            self.screen_focus = 'game'
            self.once_draw_some_things()
            self.draw_settings_in_game()

        def update(self):
            if self.screen_focus == 'game':
                self.update_waves()
            elif self.screen_focus == 'in-game settings':
                self.settings_in_game()

        def update_waves(self):
            self.time = self.time - self.clock.tick() / 1000 * self.speed_of_game
            if self.time <= 0:
                self.time = 0
            if len(self.enemies_list) == 0 and self.number_of_enemies == 0:
                self.bool_to_go_to_next_wave = False
                self.max_number_of_enemies += 1
                self.number_of_enemies = self.max_number_of_enemies
                self.wave += 1
                pygame.draw.rect(self.screen_for_many_feautures, (0, 0, 0, 0), ((220, 15), (80, 80)), 0)
                wave_text = self.font50.render(str(self.wave), True, (20, 20, 250))
                self.screen_for_many_feautures.blit(wave_text, (220, 15))
                if self.wave % 2 == 0:
                    self.enemy_hp += 1
                if not self.auto_next_wave:
                    rect = self.next_wave_button_rect
                    pos_for_triangle = (rect.left + 20, rect.top + 20), (rect.right - 20, rect.top + rect.width // 2), \
                                       (rect.left + 20, rect.bottom - 20)
                    pygame.draw.polygon(self.screen_for_many_feautures, (250, 250, 250), pos_for_triangle, 0)
            if self.time <= 0 and self.number_of_enemies != 0 and (self.bool_to_go_to_next_wave or self.auto_next_wave):
                if self.wave % 5 == 0 and self.number_of_enemies - 1 == 0:
                    enemy = Enemy('boss', 20, self.enemy_hp*5, self)
                elif self.wave % 3 == 0 and self.number_of_enemies <= self.max_number_of_enemies//5:
                    enemy = Enemy('hidden', 15, self.enemy_hp, self)
                elif self.number_of_enemies <= self.max_number_of_enemies//3:
                    enemy = Enemy('fast', 15, self.enemy_hp//2, self)
                else:
                    enemy = Enemy('common', 15, self.enemy_hp, self)
                self.time = 2
                self.number_of_enemies -= 1
                self.enemies_list.append(enemy)
            coins_text = self.font50.render(str(self.coins), True, (250, 250, 0))
            lifes_text = self.font50.render(str(self.lifes), True, (200, 0, 0))
            speed_text = pygame.font.Font(None, 50).render(f'X{str(self.speed_of_game)}', True, (200, 200, 200))
            screen.blit(lifes_text, (350, 10))
            screen.blit(coins_text, (500, 15))
            screen.blit(self.screen_for_many_feautures, (0, 0))
            screen.blit(speed_text, (width*2//15+width//30-20, height//10*8+height//20-15))     ### width*2//15, height//10*8, width//15, height//10

        def settings_in_game(self, name=None):
            screen.blit(self.in_game_settings_screen, (0, 0))
            _ = self.clock.tick()
            if name == 'auto next wave':
                rect = self.next_wave_button_rect
                pos_for_triangle = (rect.left + 20, rect.top + 20), (rect.right - 20, rect.top + rect.width // 2), \
                                   (rect.left + 20, rect.bottom - 20)
                pygame.draw.polygon(self.screen_for_many_feautures, (150, 150, 150), pos_for_triangle, 0)

        def draw_settings_in_game(self):
            #### just big rect. no, really it's quite big :0
            pos_of_big_rect = (width // 3, height // 5), (width // 3, height * 3 // 5)
            pygame.draw.rect(self.in_game_settings_screen, (40, 40, 40), pos_of_big_rect, 0)
            #### here is gonna be name of this thing('Setings')
            pos_of_name_rect = (width // 3 + 5, height // 5 + 5), (width // 3 - 10, height // 10)
            pygame.draw.rect(self.in_game_settings_screen, (60, 60, 60), pos_of_name_rect, 0)
            #### close button
            close_button = self.in_game_settings_close_button_rect
            pygame.draw.rect(self.in_game_settings_screen, (200, 0, 0), close_button, 0)
            pos = (close_button.left + 5, close_button.top + 5), (close_button.width - 10, close_button.height - 10)
            pygame.draw.rect(self.in_game_settings_screen, (250, 0, 0), pos, 0)
            #### place where all settings gonna be, also quit button :0
            pos_of_rect = (width // 3 + 5, height // 10 * 3 + 10), (width // 3 - 10, height // 2 - 15)
            pygame.draw.rect(self.in_game_settings_screen, (70, 70, 70), pos_of_rect, 0)
            #### 'auto next wave' button + text
            auto_next_wave_rect = self.in_game_settings_auto_next_wave_button_rect
            pygame.draw.rect(self.in_game_settings_screen, (50, 50, 50), auto_next_wave_rect, 0)

        def once_draw_some_things(self):
            wave_text = self.font50.render(str(self.wave), True, (20, 20, 250))
            ####  making coins
            screen_for_coin = pygame.Surface((50, 50)).convert_alpha()
            screen_for_coin.fill((0, 0, 0, 0))
            pos_for_coin = (20, 10), (40, 15), (45, 40), (20, 50), (5, 28)
            pygame.draw.polygon(screen_for_coin, (200, 200, 0), pos_for_coin, 0)
            pos_for_coin = (20, 15), (35, 20), (40, 38), (20, 45), (10, 28)
            pygame.draw.polygon(screen_for_coin, (200, 150, 0), pos_for_coin, 0)
            ####  making heart :)
            screen_for_heart = pygame.Surface((50, 50)).convert_alpha()
            screen_for_heart.fill((0, 0, 0, 0))
            pos_for_life = (25, 10), (35, 0), (45, 10), (40, 25), (25, 38), (10, 25), (5, 10), (15, 0)
            pygame.draw.polygon(screen_for_heart, (200, 0, 0), pos_for_life, 0)
            ####  making wave
            screen_for_wave = pygame.Surface((50, 50)).convert_alpha()
            screen_for_wave.fill((0, 0, 0, 0))
            pos_for_wave1 = (5, 10), (20, 5), (35, 10), (45, 5), (35, 20), (20, 15), (5, 20)
            pos_for_wave2 = (5, 30), (20, 25), (35, 30), (45, 25), (35, 40), (20, 35), (5, 40)
            pygame.draw.polygon(screen_for_wave, (20, 20, 250), pos_for_wave1, 0)
            pygame.draw.polygon(screen_for_wave, (20, 20, 220), pos_for_wave2, 0)
            #### making 'speed up' button
            pygame.draw.rect(self.screen_for_many_feautures, (100, 100, 100), self.speed_up_button_rect, 0)
            pos_of_circle = (width//6, height//20*17)   ### width*2//15, height//10*8, width//15, height//10
            pygame.draw.circle(self.screen_for_many_feautures, (40, 40, 40), pos_of_circle, 35)
            pygame.draw.circle(self.screen_for_many_feautures, (80, 80, 80), pos_of_circle, 30)
            #### making 'next wave' button
            rect = self.next_wave_button_rect
            pygame.draw.rect(self.screen_for_many_feautures, (40, 40, 40), rect, 0)
            pos_for_mini_rect = (rect.left + 5, rect.top + 5), (rect.width - 10, rect.height - 10)
            pygame.draw.rect(self.screen_for_many_feautures, (80, 80, 80), pos_for_mini_rect, 0)
            pos_for_triangle = (rect.left + 20, rect.top + 20), (rect.right - 20, rect.top + rect.width // 2), \
                               (rect.left + 20, rect.bottom - 20)
            pygame.draw.polygon(self.screen_for_many_feautures, (250, 250, 250), pos_for_triangle, 0)
            #### making 'open "in game" settings' button
            settings_rect = self.in_game_settings_open_button_rect
            s_r_w = settings_rect.width
            s_r_h = settings_rect.height
            s_r_t = settings_rect.top
            s_r_l = settings_rect.left
            pygame.draw.rect(self.screen_for_many_feautures, (60, 60, 60), settings_rect, 0)
            pos_of_rect1 = (s_r_l + 5, s_r_t + 5), (s_r_w - 10, s_r_h - 10)
            pos_of_rect2 = (s_r_l + s_r_w // 5, s_r_t + s_r_h * 2 // 10), (s_r_w // 5, s_r_h * 6 // 10)
            pos_of_rect3 = (s_r_l + s_r_w * 3 // 5, s_r_t + s_r_h * 2 // 10), (s_r_w // 5, s_r_h * 6 // 10)
            pygame.draw.rect(self.screen_for_many_feautures, (100, 100, 100), pos_of_rect1, 0)
            pygame.draw.rect(self.screen_for_many_feautures, (60, 60, 60), pos_of_rect2, 0)
            pygame.draw.rect(self.screen_for_many_feautures, (60, 60, 60), pos_of_rect3, 0)
            #### making 'to close-open build-upgrade tower' button
            pygame.draw.rect(self.screen_for_upgr_built, (80, 80, 80), ((0, 0), (width // 3, 80)), 0)
            pygame.draw.polygon(self.screen_for_upgr_built, (40, 40, 40),
                                ((width // 12, height // 50), (width // 6, 80 - height // 50),
                                 (width // 3 - width // 12, height // 50)), 0)
            #### blit everything
            self.screen_for_many_feautures.blit(screen_for_coin, (440, 0))
            self.screen_for_many_feautures.blit(screen_for_heart, (300, 10))
            self.screen_for_many_feautures.blit(screen_for_wave, (160, 10))
            self.screen_for_many_feautures.blit(wave_text, (220, 15))

        def built_upgrade_tower(self, screen_=None, j_b=False, bool=False, pos=None, bool_for_clicked_or_not=False):
            self.build_upgr_time = self.build_upgr_time - self.build_upgr_timer.tick()/1000
            bool_to_open_close = True
            if self.build_upgr_time <= 0:
                self.build_upgr_time = 0
            if self.mouse.last_pos != self.mouse.pos:
                bool_for_clicked_or_not = True
                self.clicked_bui_upg_but = False
                bool_to_open_close = False
                bool = True
            if bool:
                if width*7//10 <= self.mouse.click_pos[0] <= width*29//30 and \
                        height//2 < self.mouse.click_pos[1] <= height*11//18 and j_b:     #   upgrade and built  tower
                    if len([1 for tower_pos in Tower.towers_pos if tower_pos == self.mouse.pos]) == 0 and \
                            self.coins - 48 >= 0 and self.build_upgr_time == 0:
                        self.towers.append(Tower(self.mouse.pos[0], self.mouse.pos[1], self))
                        self.coins -= 48
                        self.mouse.screen_for_Game = self.screen_for_draw
                        bool_for_clicked_or_not = True
                        bool_to_open_close = False
                        self.build_upgr_time = 1
                        self.mouse.here_tower = True
                    elif len([1 for tower_pos in Tower.towers_pos if tower_pos == self.mouse.pos]) > 0:
                        tower = self.towers[Tower.towers_pos.index(self.mouse.pos)]
                        if self.coins - tower.upgrade_cost >= 0 and self.build_upgr_time == 0:
                            self.coins -= tower.upgrade_cost
                            if tower.level % 3 == 0:
                                tower.attack_speed *= 0.9
                            elif tower.level % 2 == 0:
                                tower.attack_radius = int(1.2 * tower.attack_radius)
                            else:
                                tower.attack_dmg += tower.beginning_attack_dmg
                            self.build_upgr_time = 1
                            tower.level += 1
                            tower.upgrade_cost = int(1.2 * tower.upgrade_cost)
                            bool_for_clicked_or_not = True
                            bool_to_open_close = False
                if bool_for_clicked_or_not:
                    if bool_to_open_close:
                        self.clicked_bui_upg_but = not self.clicked_bui_upg_but
                    if self.clicked_bui_upg_but:
                        self.screen_for_upgr_built.fill((40, 40, 40))
                        pos_of_button = (5, 80), (width//3-10, height*2//3-85)
                        pygame.draw.rect(self.screen_for_upgr_built, (130, 130, 130), pos_of_button, 0)
                        pos_of_button_to_bui_upg = (width//30, height//2), (width//15*4, height//9)
                        pygame.draw.rect(self.screen_for_upgr_built, (40, 40, 40), pos_of_button_to_bui_upg, 0)
                        pos_of_button_to_bui_upg = (width//30+5, height//2+5), (width//15*4-10, height//9-10)
                        pygame.draw.rect(self.screen_for_upgr_built, (80, 80, 80), pos_of_button_to_bui_upg, 0)
                        font40 = pygame.font.Font(None, 40)
                        if len([1 for tower in Tower.towers_pos if tower == self.mouse.pos]) == 0:
                            text_for_button = pygame.font.Font(None, 80).render('Build', True, (40, 40, 40))
                            upgrade_cost_text = font40.render(f'Build Cost: 48', True, (40, 40, 40))
                            rect5 = upgrade_cost_text.get_rect()
                            rect5.top, rect5.x = 370, width // 6 - rect5.width // 2
                            self.screen_for_upgr_built.blit(upgrade_cost_text, rect5)
                        else:
                            tower = self.towers[Tower.towers_pos.index(self.mouse.pos)]
                            text_for_button = pygame.font.Font(None, 80).render('Upgrade', True, (40, 40, 40))
                            level_text = pygame.font.Font(None, 50).render(f'Level: {tower.level}', True, (40, 40, 40))
                            speed_text = font40.render(f'Attack Speed: {tower.attack_speed}', True, (40, 40, 40))
                            radius_text = font40.render(f'Radius Attack: {tower.attack_radius}', True, (40, 40, 40))
                            attack_text = font40.render(f'Attack Damage: {tower.attack_dmg}', True, (40, 40, 40))
                            if tower.level % 3 == 0:
                                speed_text = font40.render(
                                    f'Attack Speed: {tower.attack_speed}(-{tower.attack_speed / 10})',
                                    True, (40, 40, 40))
                            elif tower.level % 2 == 0:
                                radius_text = font40.render(
                                    f'Radius Attack: {tower.attack_radius}(+{tower.attack_radius//5})', True,
                                    (40, 40, 40))
                            else:
                                attack_text = font40.render(
                                    f'Attack Damage: {tower.attack_dmg}(+{tower.beginning_attack_dmg})', True,
                                    (40, 40, 40))
                            upgrade_cost_text = font40.render(f'Upgrade Cost: {tower.upgrade_cost}', True, (40, 40, 40))
                            rect1 = level_text.get_rect()
                            rect1.top, rect1.x = 100, width // 6 - rect1.width // 2
                            self.screen_for_upgr_built.blit(level_text, rect1)
                            rect2 = radius_text.get_rect()
                            rect2.top, rect2.x = 160, width//6-rect2.width//2
                            self.screen_for_upgr_built.blit(radius_text, rect2)
                            rect3 = attack_text.get_rect()
                            rect3.top, rect3.x = 220, width // 6 - rect3.width // 2
                            self.screen_for_upgr_built.blit(attack_text, rect3)
                            rect4 = speed_text.get_rect()
                            rect4.top, rect4.x = 280, width // 6 - rect4.width // 2
                            self.screen_for_upgr_built.blit(speed_text, rect4)
                            rect5 = upgrade_cost_text.get_rect()
                            rect5.top, rect5.x = 370, width // 6 - rect5.width // 2
                            self.screen_for_upgr_built.blit(upgrade_cost_text, rect5)
                        rect = text_for_button.get_rect()
                        rect.top, rect.x = height//2 + height//18-rect.height//2, width//6-rect.width//2
                        self.screen_for_upgr_built.blit(text_for_button, rect)
                        posses = (width // 12, 80 - height // 50), (width // 6, height // 50), \
                                 (width // 3 - width // 12, 80 - height // 50)
                        print('MANY')
                    else:
                        self.screen_for_upgr_built.fill((0, 0, 0, 0))
                        posses = (width//12, height//50), (width//6, 80-height//50), (width//3-width//12, height//50)
                        print('NOt')
                    pygame.draw.rect(self.screen_for_upgr_built, (40, 40, 40), ((0, 0), (width // 3, 80)), 0)
                    pygame.draw.rect(self.screen_for_upgr_built, (70, 70, 70), ((5, 5), (width // 3-10, 70)), 0)
                    pygame.draw.polygon(self.screen_for_upgr_built, (40, 40, 40), posses, 0)
                #self.screen_for_upgr_built.blit(text_for_button, rect)
            if screen_ != None:
                if not self.mouse.here_tower:
                    pos_ = (self.mouse.pos[0]*value+5, self.mouse.pos[1]*value+5), (value-10, value-10)
                    pygame.draw.rect(screen_, (0, 200, 0, 250), pos_, 0)
                    screen.blit(screen_, (0, 0))
                    pygame.draw.rect(screen_, (0, 0, 0, 0), pos_, 0)
                else:
                    pos_ = self.mouse.pos[0]*value + value // 2, self.mouse.pos[1]*value + value // 2
                    radius = self.towers[Tower.towers_pos.index(self.mouse.pos)].attack_radius
                    pygame.draw.circle(screen_, (0, 0, 200, 50), pos_, radius)
                    screen.blit(screen_, (0, 0))
                    pygame.draw.rect(screen_, (0, 0, 0, 0), ((0, 0), (width, height)), 0)
            screen.blit(self.screen_for_upgr_built, (width*2//3, 0))


    class Map(pygame.sprite.Sprite, Game):
        def __init__(self):
            super().__init__()
            global list_of_possobility_to_go
            self.list_of_values_to_draw = [[0 for _ in range(width//value)] for _ in range(height//value)]
            self.image = pygame.Surface((value*len(self.list_of_values_to_draw[0]),
                                         value*len(self.list_of_values_to_draw)), pygame.SRCALPHA, 32)
            self.map = {1: [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 2, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 2, 1, 2, 2, 2, 1, 2, 0, 0, 0, 0, 0, 0],
                            [0, 0, 2, 2, 1, 2, 0, 2, 1, 2, 0, 0, 0, 2, 0, 0],
                            [0, 3, 1, 1, 1, 0, 0, 2, 1, 2, 2, 1, 1, 1, 4, 0],
                            [0, 0, 2, 2, 2, 0, 0, 0, 1, 0, 2, 1, 2, 2, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 2, 1, 2, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0]]}
            list_of_possobility_to_go = self.map[1]
            print(self.map[1])
            print(list_of_possobility_to_go)
            for y in range(len(list_of_possobility_to_go)):
                for x in range(len(list_of_possobility_to_go[y])):
                    if list_of_possobility_to_go[y][x] == 3:
                        self.portal_pos = x, y
                    pos_and_propotions = ((x * value, y * value), (value, value))
                    pos1 = ((x * value, y * value), (value, value))
                    if list_of_possobility_to_go[y][x] == 1:
                        if list_of_possobility_to_go[y + 1][x] not in [1, 3, 4]:
                            pos1 = pos1[0], (pos1[1][0], pos1[1][1] - 5)
                        if list_of_possobility_to_go[y - 1][x] not in [1, 3, 4]:
                            pos1 = (pos1[0][0], pos1[0][1] + 5), (pos1[1][0], pos1[1][1] - 5)
                        if list_of_possobility_to_go[y][x + 1] not in [1, 3, 4]:
                            pos1 = pos1[0], (pos1[1][0] - 5, pos1[1][1])
                        if list_of_possobility_to_go[y][x - 1] not in [1, 3, 4]:
                            pos1 = (pos1[0][0] + 5, pos1[0][1]), (pos1[1][0] - 5, pos1[1][1])
                        pygame.draw.rect(self.image, (40, 40, 40), pos_and_propotions, 0)
                        pygame.draw.rect(self.image, (60, 60, 60), pos1, 0)
                    if list_of_possobility_to_go[y][x] == 2:
                        pos_and_propotions = (x * value + 5, y * value + 5), (value - 10, value - 10)
                        pos_and_propotions1 = (x * value + 10, y * value + 10), (value - 20, value - 20)
                        pygame.draw.rect(self.image, (80, 80, 80), pos_and_propotions, 0)
                        pygame.draw.rect(self.image, (100, 100, 100), pos_and_propotions1, 0)
                    if list_of_possobility_to_go[y][x] == 3:
                        if list_of_possobility_to_go[y + 1][x] not in [1, 3, 4]:
                            pos1 = pos1[0], (pos1[1][0], pos1[1][1] - 5)
                        if list_of_possobility_to_go[y - 1][x] not in [1, 3, 4]:
                            pos1 = (pos1[0][0], pos1[0][1] + 5), (pos1[1][0], pos1[1][1] - 5)
                        if list_of_possobility_to_go[y][x + 1] not in [1, 3, 4]:
                            pos1 = pos1[0], (pos1[1][0] - 5, pos1[1][1])
                        if list_of_possobility_to_go[y][x - 1] not in [1, 3, 4]:
                            pos1 = (pos1[0][0] + 5, pos1[0][1]), (pos1[1][0] - 5, pos1[1][1])
                        pygame.draw.rect(self.image, (40, 40, 40), pos_and_propotions, 0)
                        pygame.draw.rect(self.image, (60, 60, 60), pos1, 0)
                        pos_and_propotions_of_portal = (x * value + value // 2, y * value + value // 2)
                        pygame.draw.circle(self.image, (102, 0, 255), pos_and_propotions_of_portal, 30)
                        pygame.draw.circle(self.image, (128, 0, 255), pos_and_propotions_of_portal, 25)
                        pygame.draw.circle(self.image, (139, 0, 255), pos_and_propotions_of_portal, 20)
                        pygame.draw.circle(self.image, (138, 43, 226), pos_and_propotions_of_portal, 15)
                        pygame.draw.circle(self.image, (148, 0, 211), pos_and_propotions_of_portal, 10)
                        pygame.draw.circle(self.image, (153, 50, 204), pos_and_propotions_of_portal, 5)
                    if list_of_possobility_to_go[y][x] == 4:
                        if list_of_possobility_to_go[y + 1][x] not in [1, 3, 4]:
                            pos1 = pos1[0], (pos1[1][0], pos1[1][1] - 5)
                        if list_of_possobility_to_go[y - 1][x] not in [1, 3, 4]:
                            pos1 = (pos1[0][0], pos1[0][1] + 5), (pos1[1][0], pos1[1][1] - 5)
                        if list_of_possobility_to_go[y][x + 1] not in [1, 3, 4]:
                            pos1 = pos1[0], (pos1[1][0] - 5, pos1[1][1])
                        if list_of_possobility_to_go[y][x - 1] not in [1, 3, 4]:
                            pos1 = (pos1[0][0] + 5, pos1[0][1]), (pos1[1][0] - 5, pos1[1][1])
                        pygame.draw.rect(self.image, (40, 40, 40), pos_and_propotions, 0)
                        pygame.draw.rect(self.image, (60, 60, 60), pos1, 0)
                        pos_and_propotions_of_base = ((x * value+10, y * value+10), (value-20, value-20))
                        pygame.draw.rect(self.image, (41, 41, 255), pos_and_propotions_of_base, 0)
                        pos_of_circle = (x * value + value // 2, y * value + value // 2)
                        pygame.draw.circle(self.image, (21, 21, 205), pos_of_circle, 20)
                        pygame.draw.circle(self.image, (21, 21, 150), pos_of_circle, 10)
            self.rect = pygame.Rect(0, 0, value*len(self.list_of_values_to_draw[0]),
                                    value*len(self.list_of_values_to_draw))
            print(self.list_of_values_to_draw)
            print('Усё')


    class Enemy(pygame.sprite.Sprite):
        def __init__(self, type, radius, hp, parent):
            super().__init__(all_sprites)
            self.parent = parent
            self.radius = radius
            self.rand_value = random.randint(-value//5, value//5)
            x = self.parent.map.portal_pos[0]*value + value//2
            y = self.parent.map.portal_pos[1]*value + value//2 - self.rand_value - self.radius
            self.hp = hp
            self.max_hp = hp
            self.image = pygame.Surface((2*radius, 2*radius), pygame.SRCALPHA, 32)
            self.vx = 1
            self.v = 1
            self.vy = 0
            self.type = type
            if type == 'common':
                pygame.draw.circle(self.image, (50, 50, 255), (radius, radius), radius)
                pygame.draw.circle(self.image, (50, 50, 205), (radius, radius), radius-5)
                pygame.draw.circle(self.image, (50, 50, 155), (radius, radius), radius-10)
                self.earn_coins = 2
            elif type == 'boss':
                pygame.draw.rect(self.image, (200, 10, 10), ((0, 0), (radius*2, radius*2)), 0)
                pygame.draw.rect(self.image, (150, 10, 10), ((5, 5), (radius * 2 - 10, radius * 2 - 10)), 0)
                self.earn_coins = 20
            elif type == 'fast':
                pygame.draw.polygon(self.image, (200, 200, 10), ((0, 0), (radius * 2, 0), (radius, radius * 3 // 2)), 0)
                pygame.draw.polygon(self.image, (150, 150, 10),
                                    ((5, 2), (radius * 2-5, 2), (radius, radius * 3 // 2-5)), 0)
                self.earn_coins = 4
                self.v = 2
            elif type == 'hidden':
                pygame.draw.circle(self.image, (50, 50, 255, 100), (radius, radius), radius)
                pygame.draw.circle(self.image, (50, 50, 205, 100), (radius, radius), radius-5)
                pygame.draw.circle(self.image, (50, 50, 155, 100), (radius, radius), radius-10)
                self.earn_coins = 6
            self.rect = pygame.Rect(x, y, 2*radius, 2*radius)
            self.direction_of_movement = 'right'
            self.mask = pygame.mask.from_surface(self.image)
            enemies_sprites.add(self)
            self.hp_bar = HPBar(self.rect.left, self.rect.top, self)

        def damaged(self, tower):
            if tower.time <= 0:
                tower.time = 0
                self.hp -= tower.attack_dmg
                tower.time = tower.attack_speed
            if self.hp <= 0:     # if died
                del self.parent.enemies_list[self.parent.enemies_list.index(self)]
                all_sprites.remove(self, self.hp_bar)
                polosa_sprites.remove(self.hp_bar)
                enemies_sprites.remove(self)
                self.parent.coins += self.earn_coins

        def update(self):
            if self.type == 'hidden':
                if pygame.sprite.collide_rect(self, self.parent.mouse):
                    all_sprites.add(self.hp_bar)
                else:
                    all_sprites.remove(self.hp_bar)
                    self.hp_bar.update()
            else:
                if pygame.sprite.collide_mask(self, self.parent.mouse):
                    all_sprites.add(self.hp_bar)
                else:
                    all_sprites.remove(self.hp_bar)
                    self.hp_bar.update()
            if list_of_possobility_to_go[int(self.rect.top)//75][int(self.rect.left+value//2) // 75] == 4:
                self.direction_of_movement = None
            r_t = self.rect.top
            rad = self.radius
            r_l = self.rect.left
            r_v = self.rand_value
            v = self.parent.speed_of_game
            if self.direction_of_movement == 'right':   # movement
                if list_of_possobility_to_go[int(r_t+rad)//75][int(r_l+rad+value/2-r_v+v)//75] == 1 or \
                        list_of_possobility_to_go[int(r_t+rad)//75][int(r_l+rad+value/2-r_v+v)//75] == 4:
                    self.vx, self.vy = v * self.v, 0
                elif list_of_possobility_to_go[int(r_t+rad-value/2+r_v-v)//75][int(r_l)//75] == 1:
                    self.direction_of_movement = 'up'
                elif list_of_possobility_to_go[int(r_t+rad+value/2+r_v+v)//75][int(r_l)//75] == 1:
                    self.direction_of_movement = 'down'
            elif self.direction_of_movement == 'up':
                if list_of_possobility_to_go[int(r_t+rad-value/2+r_v-v)//75][int(r_l)//75] == 1:
                    self.vx, self.vy = 0, -v * self.v
                elif list_of_possobility_to_go[int(r_t+rad)//75][int(r_l+rad+value/2-r_v+v)//75] == 1:
                    self.direction_of_movement = 'right'
            elif self.direction_of_movement == 'down':
                if list_of_possobility_to_go[int(r_t+rad+value/2+r_v+v)//75][int(r_l)//75] == 1:
                    self.vx, self.vy = 0, v * self.v
                elif list_of_possobility_to_go[int(r_t+rad)//75][int(r_l+rad+value/2-r_v+v)//75] == 1:
                    self.direction_of_movement = 'right'
            else:
                self.parent.lifes -= 1
                del self.parent.enemies_list[self.parent.enemies_list.index(self)]
                all_sprites.remove(self, self.hp_bar)
                polosa_sprites.remove(self.hp_bar)
                enemies_sprites.remove(self)
            self.rect = self.rect.move(self.vx, self.vy)


    class Tower(pygame.sprite.Sprite):
        towers_pos = []

        def __init__(self, x, y, parent):
            super().__init__()
            self.x, self.y = x, y
            self.image = pygame.Surface((value, value), pygame.SRCALPHA, 32)
            pygame.draw.rect(self.image, (20, 200, 200), ((10, 10), (value - 20, value - 20)), 0)
            self.rect = pygame.Rect(x*value, y*value, value, value)
            self.mask = pygame.mask.from_surface(self.image)
            towers_sprites.add(self)
            all_sprites.add(self)
            self.attack_radius = 100
            self.upgrade_cost = 40
            self.beginning_attack_dmg = 1
            self.attack_dmg = self.beginning_attack_dmg
            self.center = self.rect.center
            print(self.center)
            self.clock = pygame.time.Clock()
            self.attack_speed = 1
            self.level = 1
            self.time = self.attack_speed
            self.parent = parent
            #pygame.draw.circle(self.parent.screen_for_draw, (0, 0, 200, 50), self.center, self.attack_radius)
            Tower.towers_pos.append((self.x, self.y))

        def update(self):
            self.time = self.time - self.clock.tick() / 1000 * self.parent.speed_of_game
            if self.time <= 0:
                self.time = 0
            try:
                for enemy in self.parent.enemies_list:
                    valrt = math.sqrt((enemy.rect.center[0]+enemy.radius-self.center[0])**2 +
                                      (enemy.rect.center[1]-enemy.radius-self.center[1])**2)
                    valrb = math.sqrt((enemy.rect.center[0] + enemy.radius - self.center[0]) ** 2 +
                                      (enemy.rect.center[1] + enemy.radius - self.center[1]) ** 2)
                    vallb = math.sqrt((enemy.rect.center[0] - enemy.radius - self.center[0]) ** 2 +
                                      (enemy.rect.center[1] + enemy.radius - self.center[1]) ** 2)
                    vallt = math.sqrt((enemy.rect.center[0] - enemy.radius - self.center[0]) ** 2 +
                                      (enemy.rect.center[1] - enemy.radius - self.center[1]) ** 2)
                    if valrt < self.attack_radius or valrb < self.attack_radius or vallb < self.attack_radius or \
                            vallt < self.attack_radius:
                        if not (enemy.type == 'hidden' and self.level < 3):
                            enemy.damaged(self)
                            break
            except:
                pass


    class HPBar(pygame.sprite.Sprite):
        def __init__(self, x, y, enemy_parent):
            super().__init__()
            self.enemy_parent = enemy_parent
            self.image = pygame.Surface((self.enemy_parent.radius*2, 10), pygame.SRCALPHA, 32)
            self.image.fill(pygame.Color('black'))
            pygame.draw.rect(self.image, pygame.Color('green'), ((2, 2), (self.enemy_parent.radius*2-4, 6)), 0)
            self.rect = pygame.Rect(x, y-20, self.enemy_parent.radius*2, 10)
            polosa_sprites.add(self)

        def update(self):
            if self.enemy_parent.hp > 0:
                self.image.fill(pygame.Color('black'))
                w = int(round(self.enemy_parent.hp/self.enemy_parent.max_hp, 2) * (self.enemy_parent.radius * 2 - 4))
                h = 6
                pygame.draw.rect(self.image, pygame.Color('green'), ((2, 2), (w, h)), 0)
                self.rect = self.rect.move(self.enemy_parent.vx, self.enemy_parent.vy)
            else:
                all_sprites.remove(self)


    class Mouse(pygame.sprite.Sprite):
        def __init__(self, parent):
            super().__init__()
            pygame.mouse.set_visible(False)
            self.parent = parent
            self.image = pygame.Surface((10, 10), pygame.SRCALPHA, 32)
            pygame.draw.circle(self.image, (50, 250, 0), (5, 5), 5)
            self.rect = pygame.Rect(0, 0, 10, 10)
            self.mask = pygame.mask.from_surface(self.image)
            #all_sprites.add(self)
            mouse_sprites.add(self)
            self.clicked_bool = False
            #self.clicked_bool_for_built_or_upg = (False, False)
            # self.screen_for_detected_tower = pygame.Surface((width, height)).convert_alpha()
            # self.screen_for_detected_tower.fill((0, 0, 0, 0))
            self.pos = None
            self.screen_for_Game = pygame.Surface((width, height), pygame.SRCALPHA, 32)
            self.screen_for_Game.fill((0, 0, 0, 0))
            self.last_pos = None
            self.here_tower = False
            self.not_none_field = False

        def update(self, *args):
            if args and args[0].type == pygame.MOUSEMOTION:
                self.rect.topleft = event.pos[0] - 5, event.pos[1] - 5

        def clicked(self, pos=(0, 0), click=False):
            if click:
                self.click_pos = pos[0], pos[1]
                self.clicked_bool = True
            if self.parent.screen_focus == 'game':
                if len(list_of_possobility_to_go) * value > self.click_pos[1]:
                    if width * 2 // 3 <= self.click_pos[0] <= width and self.click_pos[1] <= 80 and self.not_none_field:
                        self.parent.built_upgrade_tower(self.screen_for_Game, False, True, self.pos, click)
                    elif self.parent.clicked_bui_upg_but and width * 2 // 3 <= self.click_pos[0] <= width and \
                            height * 2 // 3 >= self.click_pos[1] > 80 and self.not_none_field:
                        self.parent.built_upgrade_tower(self.screen_for_Game, True, click)
                    elif self.clicked_bool and (
                    self.click_pos[0] // value, self.click_pos[1] // value) in Tower.towers_pos:
                        self.last_pos = self.pos
                        self.pos = self.click_pos[0] // value, self.click_pos[1] // value
                        self.parent.built_upgrade_tower(self.screen_for_Game)
                        self.here_tower = True
                        self.not_none_field = True
                        # self.clicked_bool_for_built_or_upg = (True, False)
                    elif self.clicked_bool and \
                            list_of_possobility_to_go[self.click_pos[1] // value][self.click_pos[0] // value] == 2:
                        self.last_pos = self.pos
                        self.pos = self.click_pos[0] // value, self.click_pos[1] // value
                        self.here_tower = False
                        self.parent.built_upgrade_tower(self.screen_for_Game)
                        self.not_none_field = True
                        # self.clicked_bool_for_built_or_upg = (False, True)
                    else:
                        self.not_none_field = False
                if self.rect.colliderect(self.parent.speed_up_button_rect) and click:
                    parent = self.parent
                    if parent.list_of_speeds.index(parent.speed_of_game) + 1 >= len(parent.list_of_speeds):
                        parent.speed_of_game = parent.list_of_speeds[0]
                    else:
                        parent.speed_of_game = parent.list_of_speeds[
                            parent.list_of_speeds.index(parent.speed_of_game) + 1]
                    print(parent.speed_of_game)
                if self.rect.colliderect(self.parent.next_wave_button_rect) and click and \
                        not self.parent.bool_to_go_to_next_wave:
                    self.parent.bool_to_go_to_next_wave = True
                    rect = self.parent.next_wave_button_rect
                    pos_for_triangle = (rect.left + 20, rect.top + 20), (rect.right - 20, rect.top + rect.width // 2), \
                                       (rect.left + 20, rect.bottom - 20)
                    pygame.draw.polygon(self.parent.screen_for_many_feautures, (150, 150, 150), pos_for_triangle, 0)
                if self.rect.colliderect(self.parent.in_game_settings_open_button_rect) and click:
                    self.parent.speed_of_game = 0
                    self.parent.screen_focus = 'in-game settings'
            if self.parent.screen_focus == 'in-game settings':
                if self.rect.colliderect(self.parent.in_game_settings_close_button_rect) and click:
                    self.parent.speed_of_game = 1
                    self.parent.screen_focus = 'game'
                if self.rect.colliderect(self.parent.in_game_settings_auto_next_wave_button_rect) and click:
                    self.parent.auto_next_wave = not self.parent.auto_next_wave
                    self.parent.bool_to_go_to_next_wave = True
                    self.parent.settings_in_game('auto next wave')


    game = Game()
    for item in list_of_possobility_to_go:
        print(item)
    while running:
        screen.fill((10, 10, 10))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEMOTION:
                mouse_sprites.update(event)
            if event.type == pygame.MOUSEBUTTONUP:
                game.mouse.clicked(event.pos, True)
        all_sprites.draw(screen)
        all_sprites.update()
        screen.blit(update_fps(), (10, 0))
        game.update()
        if game.mouse.clicked_bool:
            game.mouse.clicked()
        mouse_sprites.draw(screen)
        mouse_sprites.update()
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()