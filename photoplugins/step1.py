from .photoExceptions import NextClassException
import pygame
import sys


class Step1:

    def __init__(self):
        self.count = 0

    def run(self, display=None, events=None):

        if display is None:
            print("No pygame in step 2")
            pygame.quit()

        img = pygame.image.load("images/idle.png").convert()
        display.blit(img, (0, 0))
        pygame.display.flip()

        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                print("Next!")
                pygame.event.clear()
                display.fill((255, 255, 255))
                pygame.display.flip()
                raise NextClassException("Moving on from Step 1.")

    def __str__(self):
        return "Step 1"
