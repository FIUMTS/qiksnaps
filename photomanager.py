import pygame
from photoplugins.photoExceptions import NextClassException


class PhotoManager:
    _instance = None

    def __new__(self):
        if self._instance is None:
            self._instance = super(PhotoManager, self).__new__(self)
            self._instance.classes = []
            pygame.init()
            self._instance.display = pygame.display.set_mode((1080, 1920), pygame.FULLSCREEN)

        return self._instance

    def run(self):
        a_class = self.classes[0]
        #print("Running %s" % (a_class))

        try:
            a_class.run(self.display, pygame.event.get())
        #make an expection class just for this
        except NextClassException:
            a_class = self.classes.pop(0)
            self.classes.append(a_class)

    def register(self, a_class):
        #print(aClass)
        self.classes.append(a_class)
