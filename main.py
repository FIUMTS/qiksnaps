import sys
from photomanager import PhotoManager
from photoplugins.step1 import Step1
from photoplugins.flash import Flash
from photoplugins.end import LastStep
from photoplugins.preview import previewCamera
from photoplugins.email import EmailPicture
from photoplugins.cleanup import cleanup
if __name__ == "__main__":
    cleanup()
    print("Starting FIU photobooth")
    p = PhotoManager()
    s1 = Step1()
    s2 = previewCamera()
    s3 = Flash()
    s4 = LastStep()
    email = EmailPicture()
    p.register(s1)
    p.register(s2)
    p.register(s3)
    p.register(email)
    p.register(s4)

    while True:
        try:
            p.run()
        except:
            cleanup()
            print("Cleaning up")
            sys.exit()
