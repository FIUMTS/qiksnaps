import os


def cleanup():
    filelist = os.listdir("snap/")

    for f in filelist:
        try:
            os.remove("snap/" + f)
            print("Removing " + f)
        except Exception as e:
            print(e)
            continue
