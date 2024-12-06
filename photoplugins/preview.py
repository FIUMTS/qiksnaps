from .photoExceptions import NextClassException, PreviousClassException
import pygame
import pygame.camera
import sys
from photoplugins.cleanup import cleanup
from datetime import datetime, timedelta
from .step import step
from .digicam import Digicam

class PreviewCamera(step):

    def __init__(self):
        self.count = 0
        pygame.camera.init()
        print(pygame.camera.list_cameras())
        self.cam = pygame.camera.Camera(pygame.camera.list_cameras()[0], (640, 480))
        self.cam.start()
        self.dslr = Digicam()


    def run(self, display=None, events=None, session=None):

        if display is None:
            print("No pygame in step 2")
            pygame.quit()

        display.fill((255, 255, 255))
        top = pygame.image.load("images/top.png").convert()
        bottom = pygame.image.load("images/bottom.png").convert()
        takephoto = pygame.image.load("images/takephoto.png").convert_alpha()
        camimg = self.cam.get_image()
        #scaled_camimg = pygame.transform.scale(camimg, (640, 480))
        display.blit(top, (0, 0))
        display.blit(bottom, (0, 1704))
        display.blit(takephoto, (403, 1749))
        display.blit(camimg, (240, 600))
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

                if event.key == pygame.K_b:
                    raise PreviousClassException("Moving back from preview")

            if event.type == pygame.MOUSEBUTTONDOWN:
                print(event.pos)
                if 403 <= event.pos[0] <= 672 and 1749 <= event.pos[1] <= 1875:
                    print("Photo taken, Next!")
                    self.runCountDown(display)
                    print("getting image")
                    self.dslr.take_pic(cmd_path="C:\\Program Files (x86)\\digiCamControl\\CameraControlCmd.exe" \
                                       , pic_dir="snap/", filename="me.jpeg")

                    #pygame.image.save(myimg, "snap/me.png")
                    raise NextClassException("Moving on from preview.")

    def runCountDown(self, display):
        count = 3
        fontobj = pygame.font.Font('fonts/segoe-ui.ttf', 1000)
        fontobj2 = pygame.font.Font('fonts/segoe-ui.ttf', 75)
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
        font_surface = fontobj2.render("Hold that pose, saving the image", False, (0, 0, 0))
        display.blit(font_surface, (50, 800))
        pygame.display.flip()
    def __str__(self):
        return "Camera preview step"
