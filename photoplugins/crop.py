import mediapipe as mp
import os
import cv2
from PIL import Image


class Crop:
    """
    A class for automatically detecting and cropping faces in images.
    Uses MediaPipe's face detection to identify face locations and
    creates cropped versions that properly frame the detected faces.
    """

    def __init__(self):
        """
        Initializes the HeadshotCrop class and sets up MediaPipe face detection.
        """
        self.mp_face_detection = mp.solutions.face_detection

    def crop_image(self, img, x1, y1, x2, y2, width, height):
        """
        Crop an image based on face bounding box coordinates with additional padding.
        The additional padding is the size of the bounding box.

        Args:
            img: The input image array
            x1, y1: Top-left coordinates of the face bounding box
            x2, y2: Bottom-right coordinates of the face bounding box
            width, height: Additional padding to add around the detected face

        Returns:
            Cropped image array with the face properly framed
        """
        h, w = img.shape[:2]

        x1 = max(0, x1 - width)
        y1 = max(0, y1 - height)
        x2 = min(w, x2 + width)
        y2 = min(h, y2 + height)

        return img[y1:y2, x1:x2]

    def validate_image(self, image_path):
        """
        Validate that the provided file path points to a valid image.
        First verifying if it can open the image with OpenCV, then validates that the file
        is an image using Pillow's image verification module.

        Args:
            image_path: The file path of the image

        Returns:
            OpenCV image if valid

        Raises:
            ValueError: If the file is not a valid image
        """
        image_path = os.path.abspath(image_path)
        # Check if provided file is an image
        try:
            img = cv2.imread(image_path)
            if img is None:
                raise ValueError("FAILED TO LOAD IMAGE")

            with Image.open(image_path) as pil_img:
                pil_img.verify()
            print("VALID IMAGE")
            return img
        except (IOError, SyntaxError) as e:
            raise ValueError("INVALID IMAGE: File is not a valid image") from e

    def create_dir(self, save_image_dir):
        """
        Create a directory to save the cropped images if it doesn't exist.

        Args:
            save_image_dir: The directory path to save the cropped images

        Returns:
            The directory path to save the cropped images

        Raises:
            ValueError: If the directory cannot be created
        """
        # Create directory if not exist else save in current directory
        if save_image_dir is not None:
            try:
                os.makedirs(save_image_dir, exist_ok=True)
                print(f"CREATED DIRECTORY: {save_image_dir}")
            except OSError as e:
                raise ValueError(f"FAILED TO CREATE DIRECTORY: {e}")
        else:
            save_image_dir = os.getcwd()
        return save_image_dir

    def detect(self, image_path, save_image_dir=None):
        """
        Main Method to detect faces and crop the image accordingly.

        This method handles the complete process:
        1. Validates the input image
        2. Creates output directory if needed
        3. Detects faces in the image using MediaPipe face detection
        4. Crops the image based on detection results:
            - For a single face: crops around that face
            - For multiple faces: crops to include all faces
        5. Saves the cropped image to the specified directory

        Args:
            image_path: The file path of the image
            save_image_dir: The directory path to save the cropped images (optional)

        Returns:
            True if faces are detected and cropped, False otherwise
        """
        img = self.validate_image(image_path)
        save_image_dir = self.create_dir(save_image_dir)

        # Convert the image from BGR to RGB
        # as OpenCV uses BGR format while MediaPipe uses RGB
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        with self.mp_face_detection.FaceDetection(
            model_selection=1, min_detection_confidence=0.5
        ) as face_detection:
            results = face_detection.process(img_rgb)

        is_cropped = False
        faces = []

        if results.detections:
            for detection in results.detections:
                bbox = detection.location_data.relative_bounding_box
                h, w = img.shape[:2]

                # Converts from normal coordinates/values to pixel coordinates/values
                x1, y1 = int(bbox.xmin * w), int(bbox.ymin * h)
                width, height = int(bbox.width * w), int(bbox.height * h)
                x2, y2 = x1 + width, y1 + height
                faces.append((x1, y1, x2, y2, width, height))

        try:
            if len(faces) == 1:
                x1, y1, x2, y2, width, height = faces[0]
                img = self.crop_image(img, x1, y1, x2, y2, width, height)
                is_cropped = True
            elif len(faces) > 1:
                x_min = min([p[0] for p in faces])
                y_min = min([p[1] for p in faces])
                x_max = max([p[2] for p in faces])
                y_max = max([p[3] for p in faces])
                width_max = max([p[4] for p in faces])
                height_max = max([p[5] for p in faces])

                img = self.crop_image(
                    img, x_min, y_min, x_max, y_max, width_max, height_max
                )
                is_cropped = True
            else:
                print("NO FACES DETECTED")

            filename = os.path.basename(image_path)
            full_path = os.path.join(save_image_dir, filename)
            cv2.imwrite(full_path, img)

            print(f"SUCCESS: IMAGE CROPPED: {full_path}")

            return is_cropped
        except Exception as e:
            print(f"ERROR OCCURRED: {e}")
            return False
