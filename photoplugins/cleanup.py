import os


def cleanup():
    try:
        filelist = os.listdir("snap/")
    except:
        os.mkdir("snap")
        return

    # Clean up files, don't want old user photos
    # on the hard drive
    for f in filelist:
        try:
            os.remove("snap/" + f)
            print("Removing " + f)
        except Exception as e:
            print(e)
            continue
