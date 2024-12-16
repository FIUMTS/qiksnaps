import sys
from photomanager import PhotoManager
from photoplugins.welcome import Welcome
from photoplugins.flash import Flash
from photoplugins.end import LastStep
from photoplugins.preview import PreviewCamera
from photoplugins.email import EmailPicture
from photoplugins.loading import loadingStep
from photoplugins.cleanup import cleanup


if __name__ == "__main__":
    cleanup()
    print("Starting Quiksnaps photobooth")
    p = PhotoManager()
    s1 = Welcome()
    holding = loadingStep()
    s2 = PreviewCamera()
    s3 = Flash()
    s4 = LastStep()
    email = EmailPicture()
    p.register(s1)
    p.register(holding)
    p.register(s2)
    p.register(s3)
    p.register(email)
    p.register(s4)
    session = {}

    while True:
        try:
            p.run(session)
        except Exception as e:
            print(e)
            cleanup()
            print("Cleaning up")
            sys.exit()


