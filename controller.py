import pygame


class Controller:
    def __init__(self,model,view):
        self.m = model
        self.v = view
        pygame.init()
        view.init()

    def run(self):
        continu = True
        while continu:
            #try:
            continu = self.processEvents()
            self.v.display(self.m.toDisplay())
            #except Exception as e:
            #    print("Error",str(e))
            #    continu = False
        pygame.quit()

    def processEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_ESCAPE]: return False
                return self.m.processKeys(keys)
        return self.m.process()