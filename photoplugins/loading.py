from .photoExceptions import NextClassException, PreviousClassException
import pygame
import sys
from photoplugins.cleanup import cleanup
from .digicam import Digicam
from .step import step


class loadingStep(step):

    def __init__(self):
        self.count = 0
        self.dslr = Digicam()

    def run(self, display=None, events=None, session=None):

        if display is None:
            print("No pygame in loading page")
            cleanup()
            pygame.quit()

        img = pygame.image.load("images/loading.jpg").convert()
        display.blit(img, (0, 0))
        pygame.display.flip()
        self.dslr.take_pic(cmd_path="C:\\Program Files (x86)\\digiCamControl\\CameraControlCmd.exe" \
                           , pic_dir="snap/", filename="me.jpeg")
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

        raise NextClassException("Moving from loading screen")

    def __str__(self):
        return "Step 1"
