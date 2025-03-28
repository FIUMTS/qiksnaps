import cv2
import os
from PIL import Image
from ultralytics import YOLO

class yolo_detect:
    def __init__(self):
        self.model = YOLO("yolov8n.pt")

    def crop_image(
        self, img, x1, y1, x2, y2, btm_pad_percent, top_pad_percent, side_pad
    ):
        h, w = img.shape[:2]

        box_width = x2 - x1
        box_height = y2 - y1
        box_aspect_ratio = box_width / box_height

        padding_bottom = int((btm_pad_percent / 100) * box_height)
        padding_top = int((top_pad_percent / 100) * box_height)

        print("box aspect ration", box_aspect_ratio)

        if 0.9 <= box_aspect_ratio <= 1.2:
            x1 = max(0, x1 + side_pad)
            y1 = max(0, y1 - padding_top)
            x2 = min(w, x2 - side_pad)
            y2 = min(h, y2)
        elif box_aspect_ratio < 0.5:
            padding_bottom = int((50 / 100) * box_height)
            padding_top = 0

            x1 = max(0, x1 + side_pad)
            y1 = max(0, y1 - padding_top)
            x2 = min(w, x2 - side_pad)
            y2 = min(h, y2 - padding_bottom)
        else:
            x1 = max(0, x1 + side_pad)
            y1 = max(0, y1 - padding_top)
            x2 = min(w, x2 - side_pad)
            y2 = min(h, y2 - padding_bottom)

        return img[y1:y2, x1:x2]

    def draw_rect(self, img, x1, y1, x2, y2):
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
        return img

    def detect(self, image_path, save_image_dir=None):

        image_path = os.path.abspath(image_path)

        # Check if provided file is an image
        try:
            with Image.open(image_path) as img:
                img.verify()
            print("VALID IMAGE")
        except (IOError, SyntaxError) as e:
            raise ValueError("INVALID IMAGE: File is not a valid image") from e

        # Create directory if not exist else save in current directory
        if save_image_dir is not None:
            if not os.path.exists(save_image_dir):
                try:
                    os.makedirs(save_image_dir, exist_ok=True)
                    print(f"CREATED DIRECTORY: {save_image_dir}")
                except OSError as e:
                    raise ValueError(f"FAILED TO CREATE DIRECTORY: {e}")
        else:
            save_image_dir = os.getcwd()

        img = cv2.imread(image_path)
        if img is None:
            raise ValueError("FAILED TO LOAD IMAGE")

        results = self.model(img)

        is_cropped = False

        persons = []
        for box in results[0].boxes:
            if box.cls[0] == 0:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                persons.append((x1, y1, x2, y2))

        try:
            if len(persons) == 1:
                x1, y1, x2, y2 = persons[0]
                img = self.crop_image(img, x1, y1, x2, y2, 30, 10, 0)
                # img = self.draw_rect(img, x1, y1, x2, y2)
                is_cropped = True
            elif len(persons) > 1:
                x_min = min([p[0] for p in persons])
                y_min = min([p[1] for p in persons])
                x_max = max([p[2] for p in persons])
                y_max = max([p[3] for p in persons])

                img = self.crop_image(img, x_min, y_min, x_max, y_max)
                is_cropped = True
            else:
                print("NO PERSONS DETECTED")

            filename = os.path.basename(image_path)
            full_path = os.path.join(save_image_dir, filename)

            cv2.imwrite(full_path, img)

            return is_cropped
        except Exception as e:
            print(f"ERROR OCCURRED: {e}")
            return False
