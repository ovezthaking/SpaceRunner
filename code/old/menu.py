import pygame, sys
from settings import *
from sprites import BG, Ground, Ship, Obstacle
from main import Game

class Menu:
    def __init__(self):
        # setup
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
        pygame.display.set_caption('Space Runner')
        self.clock = pygame.time.Clock()

        # sprite groups
        self.all_sprites = pygame.sprite.Group()

        # scale factor
        bg_height = pygame.image.load('./SpaceRunner/graphics/environment/background.png').get_height()
        self.scale_factor = WINDOW_HEIGHT / bg_height

        # sprite setup 
        BG(self.all_sprites,self.scale_factor)
        Ground([self.all_sprites],self.scale_factor)

        # text
        self.font = pygame.font.Font('./SpaceRunner/graphics/font/BD_Cartoon_Shout.ttf',20)
        self.title = self.font.render('Space Runner',True,'white')
        self.title_rect = self.title.get_rect(center = (WINDOW_WIDTH / 2,WINDOW_HEIGHT / 4))

        self.subtitle = self.font.render('Press SPACE or click to start',True,'white')
        self.subtitle_rect = self.subtitle.get_rect(center = (WINDOW_WIDTH / 2,WINDOW_HEIGHT / 1.5))

        self.instructions = self.font.render('How to play: Jump over obstacles using SPACE or click',True,'white')
        self.instructions_rect = self.instructions.get_rect(center = (WINDOW_WIDTH / 2,WINDOW_HEIGHT / 1.2))

        # music 
        self.music = pygame.mixer.Sound('./SpaceRunner/sounds/music.mp3')
        self.music.play(loops = -1)
        self.music.set_volume(0.3)

    def run(self):
        while True:
            # event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE or event.type == pygame.MOUSEBUTTONDOWN:
                    game = Game()
                    game.run()
                    pygame.quit()
                    sys.exit()

            # game logic
            self.display_surface.fill('black')
            self.all_sprites.update(0)
            self.all_sprites.draw(self.display_surface)
            self.display_surface.blit(self.title,self.title_rect)
            self.display_surface.blit(self.subtitle,self.subtitle_rect)
            self.display_surface.blit(self.instructions,self.instructions_rect)

            pygame.display.update()
            # self.clock.tick(FRAMERATE)

if __name__ == '__main__':
    menu = Menu()
    menu.run()
   
