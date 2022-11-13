import json
import os
from PIL import Image, ImageDraw, ImageFont
import face_recognition
from slugify import slugify

IMAGE_DATA_JSON = "known_images.json"

class FaceID:
    def __init__(self):
        """
        Init class
        """
        # Load the JSON with the images we already know, then load those images and parse them:
        self.known_encodings = []
        self.known_names = []

        self.folder = os.environ.get("IMAGE_STORE_FOLDER", "/tmp/face_id_images/")
        os.makedirs(os.path.join(self.folder, "images"), exist_ok=True)

        self.known_json = os.path.join(self.folder, IMAGE_DATA_JSON)
        if os.path.exists(self.known_json):
            self.known_images = json.load(open(self.known_json, "r"))

            for image_data in self.known_images:
                # Each image data is a dict with keys: 'name', 'file':
                self._add_known_image(image_data['file'], image_data['name'])
        else:
            self.known_images = []

    def add_image(self, filename, image_data):
        """
        Add an image to our images folder
        :param filename: The name of the image file
        :param image_data: The binary image data
        :return:
        """
        with open(os.path.join(self.folder, "images", filename), 'wb') as fp:
            fp.write(image_data)

    def list_images(self):
        """
        List the files in the images folder
        :return: A list of files
        """
        return os.listdir(os.path.join(self.folder, "images"))

    def remove_image(self, filename):
        """
        Removes an image from the directory
        :param filename: The name of the file to remove
        :return:
        """
        os.remove(os.path.join(self.folder, "images", filename))

    def add_known(self, name, image_data):
        """
        Adds a name to our known DB - add it to the JSON, save it in a file in our directory
        :param name: The person name
        :param image_data: The image binary data
        :return:
        """
        filename = f"{slugify(name)}.jpg"
        self.add_image(filename, image_data)
        self.known_images.append({'name': name,
                                  'file': filename})
        self._add_known_image(filename, name)
        self._write_json()

    def _write_json(self):
        """
        Write the JSON to the file self.known_json
        :return:
        """
        with open(self.known_json, 'w') as fp:
            json.dump(self.known_images, fp)

    def remove_known(self, name):
        """
        Remove a known image by the name of the person. Remove the first found known that matches the name.
        Also removes the file from the folder
        :param name: Name of person to remove
        :return: True if removed. False if not
        """
        for k,image in enumerate(self.known_images):
            if image['name'] == name:
                # Remove this one!
                self.remove_image(image['file'])
                del self.known_images[k]
                del self.known_encodings[k]
                del self.known_names[k]
                self._write_json()
                return True
        return False

    def get_known(self):
        """
        A generator yielding the know images one by one. Each known returned is a dict with values {'name', 'image_file', 'image'}
        The name is a string, the image_file is a file location as a string, and image is an image from the PIL library
        :return:
        """
        for image in self.known_images:
            filename = os.path.join(self.folder, "images", image['file'])
            yield {"name": image['name'],
                   "image_file": filename,
                   "image": Image.open(filename)}

    def num_known(self):
        """
        Return the number of known images
        :return: The number of knowns
        """
        return len(self.known_images)

    def _add_known_image(self, filename, name):
        """
        Add a known face to the object
        :param filename: name of file to load. File is expected to be in our folder (self.folder) under 'images'
        :param name: The name of the person
        :return: None
        """
        image = face_recognition.load_image_file(os.path.join(self.folder, 'images', filename))
        encoding = face_recognition.face_encodings(image)[0]
        self.known_encodings.append(encoding)
        self.known_names.append(name)

    def identify_faces(self, filename):
        """
        Find faces in a file
        :param filename: name of file to load. File is expected to be in our folder (self.folder) under 'images'
        :return: Image with names and bounding boxes added to it
        """
        file_to_id = os.path.join(self.folder, 'images', filename)

        # Find the loacations in the target image with faces:
        img = face_recognition.load_image_file(file_to_id)
        face_locations = face_recognition.face_locations(img)

        # Create a list of the encodings we already know, and a list with the names of the people in those face photos:
        face_encodings = face_recognition.face_encodings(img, face_locations)

        # Now for the faces we found in the new picture, try to match each of them to the faces we know.
        # If we find a match, record the name of the person. Otherwise the name is 'Unknown'
        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(self.known_encodings, face_encoding)
            name = "Unknown"

            # # If a match was found in known_face_encodings, just use the first one.
            if True in matches:
                first_match_index = matches.index(True)
                name = self.known_names[first_match_index]

            face_names.append(name)

        # Display the results - load the original image and add rectangles for every person:
        image = Image.open(file_to_id)
        res_img = ImageDraw.Draw(image)

        # use a bitmap font
        font = ImageFont.truetype("images/16020_FUTURAM.ttf", 40)
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Draw a box around the face
            res_img.rectangle((right, top, left, bottom), outline='red', width=3)
            res_img.text((left, bottom), name, font=font, fill='white')

        return image


