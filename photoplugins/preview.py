from .photoExceptions import NextClassException
import pygame
import pygame.camera
import sys
from photoplugins.cleanup import cleanup


class previewCamera:

    def __init__(self):
        self.count = 0
        pygame.camera.init()
        print(pygame.camera.list_cameras())
        self.cam = pygame.camera.Camera(pygame.camera.list_cameras()[0], (1280, 720))
        self.cam.start()

    def run(self, display=None, events=None):

        if display is None:
            print("No pygame in step 2")
            pygame.quit()
        display.fill((255, 255, 255))
        top = pygame.image.load("images/top.png").convert()
        bottom = pygame.image.load("images/bottom.png").convert()
        takephoto = pygame.image.load("images/takephoto.png").convert_alpha()
        camimg = self.cam.get_image()

        display.blit(top, (0, 0))
        display.blit(bottom, (0, 1704))
        display.blit(takephoto, (403, 1749))
        display.blit(camimg, (0, 600))
        pygame.display.flip()

        for event in events:
            if event.type == pygame.QUIT:
                self.cam.stop()
                pygame.quit()
                cleanup()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.cam.stop()
                    cleanup()
                    pygame.quit()
                    sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                print("Next!")
                pygame.image.save(camimg, "snap/me.png")
                display.fill((0, 0, 0))
                pygame.display.flip()
                pygame.event.clear()

                raise NextClassException("Moving on from preview.")

    def __str__(self):
        return "Camera preview step"
