from .photoExceptions import NextClassException
import pygame
import pygame.camera
import sys
from photoplugins.cleanup import cleanup
from datetime import datetime, timedelta
from .step import step


class PreviewCamera(step):

    def __init__(self):
        self.count = 0
        pygame.camera.init()
        print(pygame.camera.list_cameras())
        self.cam = pygame.camera.Camera(pygame.camera.list_cameras()[0], (1280, 720))
        self.cam.start()

    def run(self, display=None, events=None, session=None):

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
                print(event.pos)
                if 403 <= event.pos[0] <= 672 and 1749 <= event.pos[1] <= 1875:
                    print("Photo taken, Next!")
                    self.runCountDown(display)
                    print("getting image")
                    # No clue why, but we need to call get_image 3 times
                    # to get the current, image (;﹏;)
                    myimg = self.cam.get_image()
                    myimg = self.cam.get_image()
                    myimg = self.cam.get_image()

                    pygame.image.save(myimg, "snap/me.png")
                    raise NextClassException("Moving on from preview.")

    def runCountDown(self, display):
        count = 3
        fontobj = pygame.font.Font('fonts/segoe-ui.ttf', 1000)
        display.fill((255, 255, 255))
        starttime = datetime.now()
        while count > 0:

            font_surface = fontobj.render(str(count), False, (0,0,0))
            display.blit(font_surface, (300, 100))
            pygame.display.flip()

            currenttime = datetime.now()
            diff = currenttime - starttime

            if diff.total_seconds() > 1:
                print("%s!" % count)
                count = count - 1
                starttime = datetime.now()
                display.fill((255, 255, 255))


    def __str__(self):
        return "Camera preview step"
