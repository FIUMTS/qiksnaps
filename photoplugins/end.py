from .photoExceptions import NextClassException
import pygame
from datetime import datetime
import sys
from photoplugins.cleanup import cleanup
from .step import step


class LastStep(step):

    def __init__(self):
        self.count = 0
        self.time = None
        self.fontObj = pygame.font.Font('fonts/segoe-ui.ttf', 16)

    def run(self, display=None, events=None, session=None):

        #Set the time on the first run
        if self.time is None:
            self.time = datetime.now()

        if display is None:
            print("No pygame in laststep")
            cleanup()
            pygame.quit()

        img = pygame.image.load("images/end.png").convert()
        display.blit(img, (0, 0))
        pygame.display.flip()

        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                cleanup()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    cleanup()
                    sys.exit()

        timetest = datetime.now() - self.time

        #if 9 or more seconds pass, clear the screen and go to the next step
        if timetest.total_seconds() > 9:
            display.fill((0, 0, 0))
            pygame.display.flip()
            pygame.event.clear()
            self.time = None
            raise NextClassException("Moving on from the end.")

    def __str__(self):
        return "Last Step launch time:%s current time: %s" % (self.time, datetime.now())
