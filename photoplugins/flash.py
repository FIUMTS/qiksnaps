from .photoExceptions import NextClassException
import pygame
import time
import sys
from datetime import datetime, timedelta
from photoplugins.cleanup import cleanup

class Flash:

    def __init__(self):
        self.time = None

    def run(self, display=None, events=None):

        if self.time is None:
            self.time = datetime.now()

        if display is None:
            print("No pygame in step 2")
            cleanup()
            pygame.quit()

        display.fill((255, 255, 255))
        print("Step 2")
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

        pygame.display.update()
        timetest = (datetime.now() - self.time) / timedelta(microseconds=1)

        if timetest > 800000:
            pygame.event.clear()
            raise NextClassException("Moving on from Step 2.")

    def __str__(self):
        return "Flash, smile!"
