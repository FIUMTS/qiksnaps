from .photoExceptions import NextClassException
import pygame
import pygame.camera
import sys
from pygame_vkeyboard import *
from photoplugins.cleanup import cleanup
from .step import step


def consumer(text):
    print('%s' % text)


class EmailPicture(step):

    def __init__(self):
        self.layout = VKeyboardLayout(VKeyboardLayout.AZERTY)
        self.keyboard = None
        self.font = pygame.font.SysFont('../fonts/segoe-ui.ttf', 55)

    def run(self, display=None, events=None, session=None):

        color = pygame.Color(8, 30, 63)
        input_rect = pygame.Rect(80, 1100, 900, 80)
        top = pygame.image.load("images/top.png").convert()
        user = pygame.image.load("snap/me.png").convert()
        email_text = "Enter an email address below"

        if self.keyboard is None:
            self.keyboard = VKeyboard(display, consumer, self.layout)

        self.keyboard.update(events)

        pygame.draw.rect(display, color, input_rect, border_radius=60)
        display.blit(self.font.render(self.keyboard.get_text(), True, (255, 255, 255)), (120, 1120))
        display.blit(self.font.render(email_text, False, (0, 0, 0)), (260, 1050))
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

            if event.type == pygame.MOUSEBUTTONUP or event.type == pygame.FINGERUP:
                print("YES %s" % self.keyboard.get_text())
                print(event.pos)

        self.keyboard.draw(display)
        display.blit(top, (0, 0))
        display.blit(user, (0, 250))
        pygame.display.update()

    def __str__(self):
        return "Email step"
