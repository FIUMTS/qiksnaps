from .photoExceptions import NextClassException
import pygame
import pygame.camera
import sys
from pygame_vkeyboard import *
from photoplugins.cleanup import cleanup
from .step import step
import re
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication



def consumer(text):
    print('%s' % text)


class EmailPicture(step):

    def __init__(self):
        self.layout = VKeyboardLayout(VKeyboardLayout.AZERTY)
        self.keyboard = None
        self.font = pygame.font.SysFont('../fonts/segoe-ui.ttf', 55)

    def run(self, display=None, events=None, session=None):

        color = pygame.Color(8, 30, 63)
        btn_color = pygame.Color(12, 18, 26)
        input_rect = pygame.Rect(80, 1100, 900, 80)
        btn_rect = pygame.Rect(420, 1200, 190, 80)
        top = pygame.image.load("images/top.png").convert()
        user = pygame.transform.scale(pygame.image.load("snap/me.png").convert(), (640, 480))
        email_text = "Enter an email address below"

        if self.keyboard is None:
            self.layout = VKeyboardLayout(VKeyboardLayout.AZERTY)
            self.keyboard = VKeyboard(display, consumer, self.layout)

        self.keyboard.update(events)

        pygame.draw.rect(display, color, input_rect, border_radius=60)
        pygame.draw.rect(display, btn_color, btn_rect, border_radius=60)
        display.blit(self.font.render("Send", True, (255, 255, 255)), (465, 1220))
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
                if 420 <= event.pos[0] <= 610 and 1200 <= event.pos[1] <= 1280:
                    print("checking email")
                    # Need to check if valid email address
                    # Need to send the email
                    email = self.keyboard.get_text()
                    if is_valid(email):
                        print("Sending email")
                        #send email
                        msg = make_email(email)
                        send_email(msg, email)
                        self.keyboard = None
                        display.fill((255, 255, 255))
                        raise NextClassException()
                    else:
                        display.blit(self.font.render("Enter a valid email address", True, (255, 0, 0)), (260, 1010))

        self.keyboard.draw(display)
        display.blit(top, (0, 0))
        display.blit(user, (240, 250))
        pygame.display.update()

    def __str__(self):
        return "Email step"


def make_email(email):
    message = MIMEMultipart()
    message['Subject'] = "Your image from the FIU photobooth"
    message['From'] = "no-reply@fiu.edu"
    message['To'] = email
    body_part = MIMEText("See attached for your photo.")
    message.attach(body_part)

    with open("snap/me.png", 'rb') as file:
        # Attach the file with filename to the email
        message.attach(MIMEApplication(file.read(), Name="me.png"))

    return message


def send_email(message, to):
    with smtplib.SMTP("smtpout.fiu.edu", 25) as server:
        server.sendmail("no-reply@fiu.edu", to, message.as_string())


def is_valid(email):
    """Check if the given email address is valid."""
    regex = re.compile(
        r"(?i)"  # Case-insensitive matching
        r"(?:[A-Z0-9!#$%&'*+/=?^_`{|}~-]+"  # Unquoted local part
        r"(?:\.[A-Z0-9!#$%&'*+/=?^_`{|}~-]+)*"  # Dot-separated atoms in local part
        r"|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]"  # Quoted strings
        r"|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")"  # Escaped characters in local part
        r"@"  # Separator
        r"[A-Z0-9](?:[A-Z0-9-]*[A-Z0-9])?"  # Domain name
        r"\.(?:[A-Z0-9](?:[A-Z0-9-]*[A-Z0-9])?)+"  # Top-level domain and subdomains
    )

    return True if re.fullmatch(regex, email) else False
