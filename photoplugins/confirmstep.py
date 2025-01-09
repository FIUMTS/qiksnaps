from .photoExceptions import NextClassException, PreviousClassException
import pygame
import sys
from photoplugins.cleanup import cleanup


class confirmstep:

    def __init__(self):
        self.count = 0

    def run(self, display=None, events=None, loopid=-1):

        if display is None:
            print("No pygame in confirm step")
            cleanup()
            pygame.quit()

        img = pygame.image.load("images/confirm.png").convert()
        nextBtn = pygame.image.load("images/next.png").convert()
        autocropBtn = pygame.image.load("images/autoCrop.png").convert()
        backBtn = pygame.image.load("images/back.png").convert()
        user = pygame.transform.scale(pygame.image.load("snap/me.jpeg").convert(), (640, 480))

        display.blit(img, (0, 0))
        display.blit(nextBtn, (568,1310))
        display.blit(autocropBtn, (304,1127))
        display.blit(backBtn, (131,1310))
        display.blit(user, (106, 566))
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
                if 568 <= event.pos[0] <= 919 and 1310 <= event.pos[1] <= 1422:
                    print("Next!")
                    pygame.event.clear()
                    display.fill((255,255,255))
                    pygame.display.flip()
                    raise NextClassException("Moving on from confirm/preview step.")
                if 131 <= event.pos[0] <= 699 and 1310 <= event.pos[1] <= 1422:
                    print("back")
                    pygame.event.clear()
                    pygame.display.flip()
                    raise PreviousClassException("-2")


    def __str__(self):
        return "Confirm or edit"
