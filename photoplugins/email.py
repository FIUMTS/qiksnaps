from .photoExceptions import NextClassException
import pygame
import pygame.camera
import sys
import keyboardlayout as kl
import keyboardlayout.pygame as klp
from pygame_vkeyboard import *


def consumer(text):
    print('%s' % text)


class EmailPicture:

    def __init__(self):
        self.layout = VKeyboardLayout(VKeyboardLayout.AZERTY)

        self.keyboard = None
        '''
        key_size = 60
        grey = pygame.Color('grey')
        dark_grey = ~pygame.Color('grey')
        key_info = kl.KeyInfo(
            margin=10,
            color=grey,
            txt_color=dark_grey,
            txt_font=pygame.font.Font('fonts/segoe-ui.ttf', 12),
            txt_padding=(key_size // 6, key_size // 10)
        )
        keyboard_info = kl.KeyboardInfo(
            position=(0, 1404),
            padding=2,
            color=~grey
        )

        letter_key_size = (key_size, key_size)  # width, height
        keyboard_layout = klp.KeyboardLayout(
            kl.LayoutName.QWERTY,
            keyboard_info,
            letter_key_size,
            key_info
        )

        self.key_up = key_info
        self.key_pressed = kl.KeyInfo(
            margin=10,
            color=dark_grey,
            txt_color=grey,
            txt_font=pygame.font.Font('fonts/segoe-ui.ttf', 12),
            txt_padding=(key_size // 6, key_size // 10)
        )
        self.keyboard_layout = keyboard_layout
        '''

    def run(self, display=None, events=None):

        top = pygame.image.load("images/top.png").convert()
#        bottom = pygame.image.load("images/bottom.png").convert()
#        display.fill((255, 255, 255))

        if self.keyboard is None:
            self.keyboard = VKeyboard(display, consumer, self.layout)
        self.keyboard.update(events)
        for event in events:

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

            if event.type == pygame.MOUSEBUTTONUP or event.type == pygame.FINGERUP:
                print("YES %s" % self.keyboard.get_text())
        self.keyboard.draw(display)
        display.blit(top, (0, 0))
#        display.blit(bottom, (0, 1704))
        pygame.display.update()

        '''
        top = pygame.image.load("images/top.png").convert()
        bottom = pygame.image.load("images/bottom.png").convert()
        display.fill((255, 255, 255))

        display.blit(top, (0, 0))
        display.blit(bottom, (0, 1704))

        for event in events:
            key = self.keyboard_layout.get_key(event)
            print(key)

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

                if key:
                    self.keyboard_layout.update_key(key, self.key_pressed)

            if event.type == pygame.KEYUP and key:
                self.keyboard_layout.update_key(key, self.key_up)

        self.keyboard_layout.draw(display)
        pygame.display.update()
        '''

    def __str__(self):
        return "Email step"
