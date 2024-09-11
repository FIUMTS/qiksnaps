import os
import subprocess


class Digicam:
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(Digicam, cls).__new__(cls)
        return cls.__instance

    # Function to find where CameraControlCmd.exe is located starting at provided root
    def find_cam_ctrl_cmd(self, root_dir):
        target_file = "CameraControlCmd.exe"

        for root, dirs, files in os.walk(root_dir):
            try:
                if target_file in files:
                    return os.path.join(root, target_file)
            except PermissionError:
                continue

        return None

    # Runs CameraControlCmd.exe with the specified commands and saves picture to the specified directory
    def take_pic(self, cmd_path = None, pic_dir = None, filename = None):

        # if given cmd_path is not valid file, it runs find_cam_ctrl_cmd
        if cmd_path is None:
            cmd_path = self.find_cam_ctrl_cmd("C:\\")
            # if cmd_path doesn't exist, CameraControlCmd.exe doesn't exist on given dir
            if not cmd_path:
                raise FileNotFoundError("CameraControlCmd.exe not found")

        if not os.path.isfile(cmd_path):
            cmd_path = self.find_cam_ctrl_cmd("C:\\")
            # if cmd_path doesn't exist, CameraControlCmd.exe doesn't exist on given dir
            if not cmd_path:
                raise FileNotFoundError("CameraControlCmd.exe not found")

        # if given pic_dir doesn't exist it creates the dir
        if not os.path.isdir(pic_dir):
            print("Creating directory")
            os.mkdir(pic_dir)

        # ensure that file has valid extension from provided tuple
        valid_filetypes = (".jpg", ".png", ".gif", ".pdf", ".svg", "jpeg")
        if not filename.endswith(valid_filetypes):
            raise ValueError(f"Invalid file extension.")

        # Commands to take a photo using CameraControlCmd.exe
        commands = [
            cmd_path,
            "/filename",
            os.path.join(pic_dir, filename),
            "/capture",
        ]

        try:
            process = subprocess.Popen(
                commands, stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
            stdout, stderr = process.communicate()

            if process.returncode == 0:
                # prints CameraControlCmd output after taking picture
                print(stdout.decode())
            else:
                print(f"Error capturing photo: {stderr.decode()}")
        except Exception as e:
            print(f"An error occurred: {e}")
