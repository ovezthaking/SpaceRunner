import pygame
import sys
from settings import *
from button import Button
import time
from random import choice, randint


pygame.init()

SCREEN = pygame.display.set_mode((480, 800))
pygame.display.set_caption("Menu")

BG = pygame.image.load('./SpaceRunner/graphics/environment/background.png')

def get_font(size):  
    return pygame.font.Font('./SpaceRunner/graphics/font/BD_Cartoon_Shout.ttf', size)

jumpvol = 0.5
vol = 0.3
ship =pygame.image.load (f'./SpaceRunner/graphics/ship/smil0.png').convert_alpha()



with open('./SpaceRunner/txt/cruiser.txt', 'r+') as cruiserfile:
    unlockedscruiser = int(cruiserfile.read())
if unlockedscruiser == 1:
    scruiserPrice = ""
else:
    scruiserPrice = "200"


with open('./SpaceRunner/txt/jstarship.txt', 'r+') as jedifile:
    unlockedjediship = int(jedifile.read())
if unlockedjediship == 1:
    jedishipPrice = ""
else:
    jedishipPrice = "1000"


with open('./SpaceRunner/txt/destroyer.txt', 'r+') as sdesfile:
    unlockedsdes = int(sdesfile.read())
if unlockedsdes == 1:
    sdesPrice = ""
else:
    sdesPrice = "1000"



with open('./SpaceRunner/txt/xwing.txt', 'r+') as xwingfile:
    unlockedxwing = int(xwingfile.read())
if unlockedxwing == 1:
    xwingPrice = ""
else:
    xwingPrice = "500"


with open('./SpaceRunner/txt/ywing.txt', 'r+') as ywingfile:
    unlockedywing = int(ywingfile.read())
if unlockedywing == 1:
    ywingPrice = ""
else:
    ywingPrice = "500"

def play():
 while True:
    class Game:
        def __init__(self):
            
            
            
            pygame.init()
            
            self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
            pygame.display.set_caption('Space Runner')
            self.clock = pygame.time.Clock()
            self.active = True

            
            self.all_sprites = pygame.sprite.Group()
            self.collision_sprites = pygame.sprite.Group()

           
            bg_height = pygame.image.load('./SpaceRunner/graphics/environment/background.png').get_height()
            self.scale_factor = WINDOW_HEIGHT / bg_height

             
            BG(self.all_sprites, self.scale_factor)
            Ground([self.all_sprites, self.collision_sprites], self.scale_factor)
            self.ship = Ship(self.all_sprites, self.scale_factor / 1.7)

           
            
            self.obstacle_timer = pygame.USEREVENT + 1
            pygame.time.set_timer(self.obstacle_timer, 1400)

            
            self.font = pygame.font.Font('./SpaceRunner/graphics/font/BD_Cartoon_Shout.ttf',30)
            self.score = 0
            self.start_offset = 0

            
            self.menu_surf = pygame.image.load('./SpaceRunner/graphics/ui/menu.png').convert_alpha()
            self.menu_rect = self.menu_surf.get_rect(center = (WINDOW_WIDTH / 2,WINDOW_HEIGHT / 2))

             
            
            self.music = pygame.mixer.Sound("./SpaceRunner/sounds/music.mp3")
            self.music.play(loops = -1)
            volume = self.music 
            
            volume.set_volume(vol)
            
        def collisions(self):
            if pygame.sprite.spritecollide(self.ship,self.collision_sprites,False,pygame.sprite.collide_mask)\
            or self.ship.rect.top <= 0:
                for sprite in self.collision_sprites.sprites():
                    if sprite.sprite_type == 'obstacle':
                        sprite.kill()
                self.active = False
                self.ship.kill()
                

        def display_score(self):
            if self.active:
                
                self.score = (pygame.time.get_ticks() - self.start_offset) // 1000

                

                y = WINDOW_HEIGHT / 10
            else:
                y = WINDOW_HEIGHT / 2 + (self.menu_rect.height / 1.5)

                
                with open('./SpaceRunner/txt/score.txt', 'w') as scorefile:

                    scorefile.write(str(self.score))

            score_surf = self.font.render(str(self.score),True,'white')
            score_rect = score_surf.get_rect(midtop = (WINDOW_WIDTH / 2,y))
            self.display_surface.blit(score_surf,score_rect)
            

        def run(self):
            self.start_offset = pygame.time.get_ticks()
            last_time = time.time()
            while True:
                
                
                dt = time.time() - last_time
                last_time = time.time()

                
                for event in pygame.event.get():
                    if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        with open('./SpaceRunner/txt/score.txt', 'w') as scorefile:

                            scorefile.write(str(self.score))

                        with open('./SpaceRunner/txt/score.txt', 'r+') as scorefile:
                            scorepart = int(scorefile.read())
                        with open('./SpaceRunner/txt/totalscore.txt', 'r+') as totalscorefileread:
                                            
                            totalscore = int(totalscorefileread.read())
                                        
                        with open('./SpaceRunner/txt/totalscore.txt', 'w') as totalscorefile:

                            totalscorefile.write(str(totalscore + scorepart))  
                        self.music.stop()
                        main_menu()
                        
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE or event.type == pygame.MOUSEBUTTONDOWN:
                            if self.active:
                                self.ship.jump()
                                
                            else:
                                self.ship = Ship(self.all_sprites, self.scale_factor / 1.7)
                                self.active = True
                                self.start_offset = pygame.time.get_ticks()
                                
                                with open('./SpaceRunner/txt/score.txt', 'r+') as scorefile:
                                    scorepart = int(scorefile.read())
                                with open('./SpaceRunner/txt/totalscore.txt', 'r+') as totalscorefileread:
                                                    
                                    totalscore = int(totalscorefileread.read())
                                                
                                with open('./SpaceRunner/txt/totalscore.txt', 'w') as totalscorefile:

                                    totalscorefile.write(str(totalscore + scorepart))
                                    

                    if event.type == self.obstacle_timer and self.active:
                        Obstacle([self.all_sprites,self.collision_sprites],self.scale_factor * 1.1)
                
                
                
                self.display_surface.fill('black')
                self.all_sprites.update(dt)
                self.all_sprites.draw(self.display_surface)
                self.display_score()

                if self.active: 
                    self.collisions()
                    
                else:
                    self.display_surface.blit(self.menu_surf,self.menu_rect)


                pygame.display.update()
                # self.clock.tick(FRAMERATE)
    class BG(pygame.sprite.Sprite):
        def __init__(self,groups,scale_factor):
            super().__init__(groups)
            bg_image = pygame.image.load('./SpaceRunner/graphics/environment/background.png').convert()

            full_height = bg_image.get_height() * scale_factor
            full_width = bg_image.get_width() * scale_factor
            full_sized_image = pygame.transform.scale(bg_image,(full_width,full_height))
            
            self.image = pygame.Surface((full_width * 2,full_height))
            self.image.blit(full_sized_image,(0,0))
            self.image.blit(full_sized_image,(full_width,0))

            self.rect = self.image.get_rect(topleft = (0,0))
            self.pos = pygame.math.Vector2(self.rect.topleft)

        def update(self,dt):
            self.pos.x -= 300 * dt
            if self.rect.centerx <= 0:
                self.pos.x = 0
            self.rect.x = round(self.pos.x)

    class Ground(pygame.sprite.Sprite):
        def __init__(self,groups,scale_factor):
            super().__init__(groups)
            self.sprite_type = 'ground'
            
            
            ground_surf = pygame.image.load('./SpaceRunner/graphics/environment/ground.png').convert_alpha()
            self.image = pygame.transform.scale(ground_surf,pygame.math.Vector2(ground_surf.get_size()) * scale_factor)
            
            
            self.rect = self.image.get_rect(bottomleft = (0,WINDOW_HEIGHT))
            self.pos = pygame.math.Vector2(self.rect.topleft)

            
            self.mask = pygame.mask.from_surface(self.image)

        def update(self,dt):
            self.pos.x -= 360 * dt
            if self.rect.centerx <= 0:
                self.pos.x = 0

            self.rect.x = round(self.pos.x)

    class Ship(pygame.sprite.Sprite):
        def __init__(self,groups,scale_factor):
            super().__init__(groups)

            
            self.import_frames(scale_factor)
            self.frame_index = 0
            self.image = self.frames[self.frame_index]

            
            self.rect = self.image.get_rect(midleft = (WINDOW_WIDTH / 20,WINDOW_HEIGHT / 2))
            self.pos = pygame.math.Vector2(self.rect.topleft)

            
            self.gravity = 600
            self.direction = 0

            
            self.mask = pygame.mask.from_surface(self.image)

            
            self.jump_sound = pygame.mixer.Sound('./SpaceRunner/sounds/jump.wav')
            self.jump_sound.set_volume(jumpvol)

        def import_frames(self,scale_factor):
            self.frames = []
            
            global ship
            surf = ship
            scaled_surface = pygame.transform.scale(surf,pygame.math.Vector2(surf.get_size())* scale_factor)
            self.frames.append(scaled_surface)
            return surf, ship
            

        def apply_gravity(self,dt):
            self.direction += self.gravity * dt
            self.pos.y += self.direction * dt
            self.rect.y = round(self.pos.y)

        def jump(self):
            self.jump_sound.play()
            self.direction = -400

        def animate(self,dt):
            self.frame_index += 10 * dt
            if self.frame_index >= len(self.frames):
                self.frame_index = 0
            self.image = self.frames[int(self.frame_index)]

        def rotate(self):
            rotated_ship = pygame.transform.rotozoom(self.image,-self.direction * 0.06,1)
            self.image = rotated_ship
            self.mask = pygame.mask.from_surface(self.image)

        def update(self,dt):
            self.apply_gravity(dt)
            self.animate(dt)
            self.rotate()

    class Obstacle(pygame.sprite.Sprite):
        def __init__(self,groups,scale_factor):
            super().__init__(groups)
            self.sprite_type = 'obstacle'

            orientation = choice(('up','down'))
            surf = pygame.image.load(f'./SpaceRunner/graphics/obstacles/{choice((1,2))}.png').convert_alpha()
            self.image = pygame.transform.scale(surf,pygame.math.Vector2(surf.get_size()) * scale_factor)
            
            x = WINDOW_WIDTH + randint(40,100)

            if orientation == 'up':
                y = WINDOW_HEIGHT + randint(10,50)
                self.rect = self.image.get_rect(midbottom = (x,y))
            else:
                y = randint(-50,-10)
                self.image = pygame.transform.flip(self.image,False,True)
                self.rect = self.image.get_rect(midtop = (x,y))

            self.pos = pygame.math.Vector2(self.rect.topleft)

            
            self.mask = pygame.mask.from_surface(self.image)

        def update(self,dt):
            self.pos.x -= 400 * dt
            self.rect.x = round(self.pos.x)
            if self.rect.right <= -100:
                self.kill()

    if __name__ == '__main__':
        game = Game()
        game.run()
    
def options():
    while True:
        
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("Black")

        OPTIONS_TEXT = get_font(45).render("Options", True, "White")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(240, 50))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_BACK = Button(image=None, pos=(240, 700), 
                            text_input="BACK", font=get_font(75), base_color="White", hovering_color="Green")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)
        global vol

        MUSIC_TEXT = get_font(30).render("Music Volume", True, "White")
        MUSIC_RECT = MUSIC_TEXT.get_rect(center=(240, 150))
        SCREEN.blit(MUSIC_TEXT, MUSIC_RECT)
        MUSICVOL_TEXT = get_font(30).render(str(vol), True, "White")
        MUSICVOL_RECT = MUSICVOL_TEXT.get_rect(center=(240, 200))
        SCREEN.blit(MUSICVOL_TEXT, MUSICVOL_RECT)

        VOLMIN = Button(image=pygame.image.load("./SpaceRunner/graphics/ui/minus.png"), pos=(90, 200), 
                            text_input="", font=get_font(20), base_color="White", hovering_color="Green")

        VOLMIN.changeColor(OPTIONS_MOUSE_POS)
        VOLMIN.update(SCREEN)

        VOLPLUS = Button(image=pygame.image.load("./SpaceRunner/graphics/ui/plus.png"), pos=(400, 200), 
                            text_input="", font=get_font(20), base_color="White", hovering_color="Green")

        VOLPLUS.changeColor(OPTIONS_MOUSE_POS)
        VOLPLUS.update(SCREEN)

        global jumpvol

        SFX_TEXT = get_font(30).render("SFX Volume", True, "White")
        SFX_RECT = SFX_TEXT.get_rect(center=(240, 300))
        SCREEN.blit(SFX_TEXT, SFX_RECT)

        SFXVOL_TEXT = get_font(30).render(str(jumpvol), True, "White")
        SFXVOL_RECT = SFXVOL_TEXT.get_rect(center=(240, 350))
        SCREEN.blit(SFXVOL_TEXT, SFXVOL_RECT)

        SFXMIN = Button(image=pygame.image.load("./SpaceRunner/graphics/ui/minus.png"), pos=(90, 350), 
                            text_input="", font=get_font(20), base_color="White", hovering_color="Green")

        SFXMIN.changeColor(OPTIONS_MOUSE_POS)
        SFXMIN.update(SCREEN)

        SFXPLUS = Button(image=pygame.image.load("./SpaceRunner/graphics/ui/plus.png"), pos=(400, 350), 
                            text_input="", font=get_font(20), base_color="White", hovering_color="Green")

        SFXPLUS.changeColor(OPTIONS_MOUSE_POS)
        SFXPLUS.update(SCREEN)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if VOLMIN.checkForInput(OPTIONS_MOUSE_POS):
                    if vol >= 0.10:
                        vol -= 0.10
                        vol = round(vol, 1)
                    if vol < 0.1:
                        vol = 0.00
                        
                if VOLPLUS.checkForInput(OPTIONS_MOUSE_POS):
                    if vol <= 0.9:
                        vol += 0.10
                        vol = round(vol, 1)
                    if vol > 0.9:
                        vol = 1.00
                if SFXMIN.checkForInput(OPTIONS_MOUSE_POS):
                    if jumpvol >= 0.10:
                        jumpvol -= 0.10
                        jumpvol = round(jumpvol, 1)
                    if jumpvol < 0.1:
                        jumpvol = 0.00
                if SFXPLUS.checkForInput(OPTIONS_MOUSE_POS):
                    if jumpvol <= 0.9:
                        jumpvol += 0.10
                        jumpvol = round(jumpvol, 1)
                    if jumpvol > 0.9:
                        jumpvol = 1.00
                        jumpvol = round(jumpvol, 1)
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    main_menu()

        pygame.display.update()


def select():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("white")

        SELECT_TEXT = get_font(45).render("Select a Ship", True, "Black")
        SELECT_RECT = SELECT_TEXT.get_rect(center=(240, 100))
        SCREEN.blit(SELECT_TEXT, SELECT_RECT)

        with open('./SpaceRunner/txt/totalscore.txt', 'r') as tscorefile:
            totalscore = int(tscorefile.read())
        gold = pygame.Color(146,106,11)
        SCORE2_TEXT = get_font(20).render("Total Score: " + str(totalscore) , True, gold)
        SCORE2_RECT = SCORE2_TEXT.get_rect(center=(240, 170))
        SCREEN.blit(SCORE2_TEXT, SCORE2_RECT)


        SMIL_TEXT = get_font(10).render("Millennium Falcon", True, "Black")
        SMIL_RECT = SMIL_TEXT.get_rect(center=(90, 220))
        SCREEN.blit(SMIL_TEXT, SMIL_RECT)

        SMIL = Button(image=pygame.image.load("./SpaceRunner/graphics/ship/smil0.png"), pos=(90, 250),
                            text_input="", font=get_font(20), base_color="Black", hovering_color="Blue")
        SMIL.update(SCREEN)


        SCR_TEXT = get_font(10).render("Skywalker Cruiser", True, "Black")
        SCR_RECT = SCR_TEXT.get_rect(center=(250, 220))
        SCREEN.blit(SCR_TEXT, SCR_RECT)

        global scruiserPrice
        SCRUISER = Button(image=pygame.image.load("./SpaceRunner/graphics/ship/scruiser.png"), pos=(250, 250),
                            text_input=scruiserPrice, font=get_font(20), base_color="Red", hovering_color="Red")
        SCRUISER.update(SCREEN)

        JSH_TEXT = get_font(10).render("Jedi Space Ship", True, "Black")
        JSH_RECT = JSH_TEXT.get_rect(center=(400, 220))
        SCREEN.blit(JSH_TEXT, JSH_RECT)

        
        global jedishipPrice
        JEDISHIP = Button(image=pygame.image.load("./SpaceRunner/graphics/ship/jedispaceship.png"), pos=(400, 250),
                            text_input=jedishipPrice, font=get_font(20), base_color="Red", hovering_color="Red")
        
        JEDISHIP.changeColor(OPTIONS_MOUSE_POS)
        JEDISHIP.update(SCREEN)

        global sdesPrice
        SDES = Button(image=pygame.image.load("./SpaceRunner/graphics/ship/stardestroyer.png"), pos=(90, 350),
                            text_input=sdesPrice, font=get_font(20), base_color="Red", hovering_color="Red")
        SDES.update(SCREEN)


        SDES_TEXT = get_font(10).render("Star Destroyer", True, "Black")
        SDES_RECT = SDES_TEXT.get_rect(center=(90, 320))
        SCREEN.blit(SDES_TEXT, SDES_RECT)

        global xwingPrice
        XWING = Button(image=pygame.image.load("./SpaceRunner/graphics/ship/xwing.png"), pos=(250, 350),
                            text_input=xwingPrice, font=get_font(20), base_color="Red", hovering_color="Red")
        XWING.update(SCREEN)

        XW_TEXT = get_font(10).render("X-Wing", True, "Black")
        XW_RECT = XW_TEXT.get_rect(center=(240, 320))
        SCREEN.blit(XW_TEXT, XW_RECT)


        YW_TEXT = get_font(10).render("Y-Wing", True, "Black")
        YW_RECT = YW_TEXT.get_rect(center=(390, 320))
        SCREEN.blit(YW_TEXT, YW_RECT)

        
        global ywingPrice
        YWING = Button(image=pygame.image.load("./SpaceRunner/graphics/ship/ywing.png"), pos=(400, 350),
                            text_input=ywingPrice, font=get_font(20), base_color="Red", hovering_color="Red")
        
        YWING.changeColor(OPTIONS_MOUSE_POS)
        YWING.update(SCREEN)

        OPTIONS_BACK = Button(image=None, pos=(240, 700), 
                            text_input="BACK", font=get_font(75), base_color="Black", hovering_color="Blue")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)




        for event in pygame.event.get():
            global unlockedscruiser
            global unlockedjediship
            global unlockedsdes
            global unlockedxwing
            global unlockedywing
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                smil = pygame.image.load("./SpaceRunner/graphics/ship/smil0.png")
                scruiser = pygame.image.load("./SpaceRunner/graphics/ship/scruiser.png")
                jediship = pygame.image.load("./SpaceRunner/graphics/ship/jedispaceship.png")
                sdes = pygame.image.load("./SpaceRunner/graphics/ship/stardestroyer.png")
                xw = pygame.image.load("./SpaceRunner/graphics/ship/xwing.png")
                yw = pygame.image.load("./SpaceRunner/graphics/ship/ywing.png")

                global ship

                with open('./SpaceRunner/txt/totalscore.txt', 'r') as tscorefile:
                    totalscore = int(tscorefile.read())

                if SMIL.checkForInput(OPTIONS_MOUSE_POS):
                    ship = smil
                if SCRUISER.checkForInput(OPTIONS_MOUSE_POS):
                    if unlockedscruiser == 1:
                        ship = scruiser
                    if unlockedscruiser == 0:
                        if totalscore >= 200:
                            scruiserPrice = ""
                            unlockedscruiser = 1;
                            totalscore -= 200
                            with open('./SpaceRunner/txt/totalscore.txt', 'w') as tscorefile:
                                tscorefile.write(str(totalscore))
                            with open('./SpaceRunner/txt/scruiser.txt', 'w') as scruiserfile:
                                scruiserfile.write(str(unlockedscruiser))
                if JEDISHIP.checkForInput(OPTIONS_MOUSE_POS):
                    if unlockedjediship == 1:
                        ship = jediship
                    if unlockedjediship == 0:
                        if totalscore >= 500:
                            jedishipPrice = ""
                            unlockedjediship = 1;
                            totalscore -= 500
                            with open('./SpaceRunner/txt/totalscore.txt', 'w') as tscorefile:
                                tscorefile.write(str(totalscore))
                            with open('./SpaceRunner/txt/jediship.txt', 'w') as jedifile:
                                jedifile.write(str(unlockedjediship))
                if SDES.checkForInput(OPTIONS_MOUSE_POS):
                    if unlockedsdes == 1:
                        ship = sdes
                    if unlockedsdes == 0:
                        if totalscore >= 1000:
                            sdesPrice = ""
                            unlockedsdes = 1;
                            totalscore -= 1000
                            with open('./SpaceRunner/txt/totalscore.txt', 'w') as tscorefile:
                                tscorefile.write(str(totalscore))
                            with open('./SpaceRunner/txt/sdes.txt', 'w') as sdesfile:
                                sdesfile.write(str(unlockedsdes))
                if XWING.checkForInput(OPTIONS_MOUSE_POS):
                    if unlockedxwing == 1:
                        ship = xw
                    if unlockedxwing == 0:
                        if totalscore >= 500:
                            xwingPrice = ""
                            unlockedxwing = 1;
                            totalscore -= 500
                            with open('./SpaceRunner/txt/totalscore.txt', 'w') as tscorefile:
                                tscorefile.write(str(totalscore))
                            with open('./SpaceRunner/txt/xwing.txt', 'w') as xwingfile:
                                xwingfile.write(str(unlockedxwing))
                if YWING.checkForInput(OPTIONS_MOUSE_POS):
                    if unlockedywing == 1:
                        ship = yw
                    if unlockedywing == 0:
                        if totalscore >= 500:
                            ywingPrice = ""
                            unlockedywing = 1;
                            totalscore -= 500
                            with open('./SpaceRunner/txt/totalscore.txt', 'w') as tscorefile:
                                tscorefile.write(str(totalscore))
                            with open('./SpaceRunner/txt/ywing.txt', 'w') as ywingfile:
                                ywingfile.write(str(unlockedywing))
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    main_menu()

        pygame.display.update()

def score():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("white")
        with open('./SpaceRunner/txt/score.txt', 'r') as scorefile:
            score = int(scorefile.read())
        
        with open('./SpaceRunner/txt/totalscore.txt', 'r') as tscorefile:
            totalscore = int(tscorefile.read())
        
        with open('./SpaceRunner/txt/highscore.txt', 'r') as hscorefile:
            highscore = int(hscorefile.read())
            if score > highscore:
                with open('./SpaceRunner/txt/highscore.txt', 'w') as hscorefile:
                    hscorefile.write(str(score))
            else:
                with open('./SpaceRunner/txt/highscore.txt', 'w') as hscorefile:
                    hscorefile.write(str(highscore))
        with open('./SpaceRunner/txt/highscore.txt', 'r') as hscorefile:
            highscore = int(hscorefile.read())

        SCORE_TEXT = get_font(45).render("Your Score: " + str(score) , True, "Black")
        SCORE_RECT = SCORE_TEXT.get_rect(center=(240, 100))
        SCREEN.blit(SCORE_TEXT, SCORE_RECT)
        

        SCORE2_TEXT = get_font(25).render("Total Score: " + str(totalscore) , True, "Black")
        SCORE2_RECT = SCORE_TEXT.get_rect(center=(240, 170))
        SCREEN.blit(SCORE2_TEXT, SCORE2_RECT)

        CREDIT_TEXT = get_font(10).render("The total score is the currency you can buy items with "  , True, "Black")
        CREDIT_RECT = SCORE_TEXT.get_rect(center=(240, 200))
        SCREEN.blit(CREDIT_TEXT, CREDIT_RECT)

        SCORE3_TEXT = get_font(25).render("Highscore: " + str(highscore) , True, "Black")
        SCORE3_RECT = SCORE3_TEXT.get_rect(center=(160, 250))
        SCREEN.blit(SCORE3_TEXT, SCORE3_RECT)


        OPTIONS_BACK = Button(image=None, pos=(240, 700), 
                            text_input="BACK", font=get_font(75), base_color="Black", hovering_color="Blue")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)

        RESET_SCORE = Button(image=None, pos=(150, 400), 
                            text_input="Reset Score", font=get_font(30), base_color="Black", hovering_color="Red")

        RESET_SCORE.changeColor(OPTIONS_MOUSE_POS)
        RESET_SCORE.update(SCREEN)

        RESET_TEXT = get_font(10).render("That resets Your Score and Total Score (Game Value)!!! "  , True, "Black")
        RESET_RECT = SCORE_TEXT.get_rect(center=(240, 450))
        SCREEN.blit(RESET_TEXT, RESET_RECT)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if RESET_SCORE.checkForInput(OPTIONS_MOUSE_POS):
                    with open('./SpaceRunner/txt/score.txt', 'w') as scorefile:
                        scorefile.write('0')
                    with open('./SpaceRunner/txt/totalscore.txt', 'w') as tscorefile:
                        tscorefile.write('0')
                        LUL_TEXT = get_font(30).render("POW!"  , True, "Purple")
                        LUL_RECT = LUL_TEXT.get_rect(center=(240, 350))
                        SCREEN.blit(LUL_TEXT, LUL_RECT)
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    main_menu()

        pygame.display.update()

def main_menu():
    while True:
        MENU_MOUSE_POS = pygame.mouse.get_pos()

        
        SCREEN.fill((0, 0, 0))

        
        background = pygame.transform.scale(BG, (480, 800))  
        SCREEN.blit(background, (0, 0))

        MENU_TEXT = get_font(50).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(240, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("./SpaceRunner/assets/Play_Rect.png"), pos=(240, 250), 
                            text_input="PLAY", font=get_font(40), base_color="#d7fcd4", hovering_color="White")
        SELECT_BUTTON = Button(image=pygame.image.load("./SpaceRunner/assets/Ch_Rect.png"), pos=(240, 400), 
                            text_input="SHIPS", font=get_font(40), base_color="#d7fcd4", hovering_color="White")
        SCORE_BUTTON = Button(image=pygame.image.load("./SpaceRunner/assets/Ch_Rect.png"), pos=(240, 550), 
                            text_input="SCORE", font=get_font(40), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("./SpaceRunner/assets/Quit_Rect.png"), pos=(240, 700), 
                            text_input="QUIT", font=get_font(40), base_color="#d7fcd4", hovering_color="White")
        OPTIONS_BUTTON = Button(image=pygame.image.load("./SpaceRunner/assets/Options_Rect.png"), pos=(40, 770), 
                            text_input="OPTIONS", font=get_font(10), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON ,SELECT_BUTTON, SCORE_BUTTON, QUIT_BUTTON, OPTIONS_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if SCORE_BUTTON.checkForInput(MENU_MOUSE_POS):
                    score()
                if SELECT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    select()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


main_menu()
