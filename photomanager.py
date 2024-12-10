import pygame
from photoplugins.photoExceptions import NextClassException, PreviousClassException


class PhotoManager:
    _instance = None

    def __new__(self):
        if self._instance is None:
            self._instance = super(PhotoManager, self).__new__(self)
            self._instance.classes = []
            pygame.init()
            # Stop double text on touch screens
            pygame.event.set_blocked([pygame.FINGERUP, pygame.FINGERDOWN])
            self._instance.display = pygame.display.set_mode((1080, 1920), pygame.FULLSCREEN)

        return self._instance

    def run(self, session):
        a_class = self.classes[0]
        #print("Running %s" % (a_class))

        try:
            a_class.run(self.display, pygame.event.get(), session)
        except NextClassException:
            a_class = self.classes.pop(0)
            self.classes.append(a_class)
        except PreviousClassException as e:
            try:
                i =  int(e.__str__())
            except ValueError:
                i = -1

            if i >= 0:
                i = -1
            #order [class we want to jump back to, the class that raised the exception, all the classes before the class we jump to]
            self.classes = self.classes[i:] + [a_class] + self.classes[:i]


    def register(self, a_class):
        #print(aClass)
        self.classes.append(a_class)
