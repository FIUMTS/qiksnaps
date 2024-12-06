from .photoExceptions import NextClassException, PreviousClassException
from .step import step
import pygame
import sys
from photoplugins.cleanup import cleanup


class Welcome(step):

    def __init__(self):
        self.count = 0

    def run(self, display=None, events=None, session=None):

        if display is None:
            print("No pygame in step 2")
            cleanup()
            pygame.quit()

        img = pygame.image.load("images/idle.png").convert()
        display.blit(img, (0, 0))
        pygame.display.flip()

        for event in events:
            if event.type == pygame.QUIT:
                cleanup()
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    cleanup()
                    pygame.quit()
                    sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                print("Next!")
                pygame.event.clear()
                pygame.display.flip()
                raise NextClassException("Moving on from Step 1.")

    def __str__(self):
        return "Step 1"
