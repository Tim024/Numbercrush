class View:
    def init(self):
        raise NotImplementedError
    def display(self,thingsToDisplay):
        raise NotImplementedError


import pygame
class basicView(View):
    def init(self):
        self.w = 400
        self.h = 300
        self.screen = pygame.display.set_mode((self.w,self.h))
        self.fps = 20
        self.clock = pygame.time.Clock()
        self.bg_color = (240,255,245)
        self.bgim = pygame.image.load('assets/bg.png').convert_alpha()

    def display(self,a):
        #self.screen.fill(self.bg_color)
        self.screen.blit(self.bgim,(0,0))
        for i in a:
            self.screen.blit(i[0],i[1])
        pygame.display.update()
        self.clock.tick(self.fps)