from .photoExceptions import nextClassException
import pygame
from datetime import datetime
import sys

class laststep:

    def __init__(self):
        self.count = 0
        self.time = None
        self.fontObj = pygame.font.Font('fonts/segoe-ui.ttf', 16)

    def run(self, display = None, events = None):
        #set the time on the first run
        if self.time == None:
            self.time = datetime.now()

        if display == None:
            print("No pygame in laststep")
            pygame.quit()

        img = pygame.image.load("images/end.png").convert()
        display.blit(img, (0,0))
        pygame.display.flip()

        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        timetest = datetime.now() - self.time

        #if 9 or more seconds pass, clear the screen and go to the next step
        if timetest.total_seconds() > 9:
            display.fill((0,0,0))
            pygame.display.flip()
            pygame.event.clear()
            self.time = None
            raise nextClassException("Moving on from the end.")

    def __str__(self):
        return "Last Step launch time:%s current time: %s"%(self.time, datetime.now())
