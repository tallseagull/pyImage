from PIL import Image, ImageDraw, ImageFont
import face_recognition

# The file we want to work on:
# file_to_id = 'images/beatles/BeatlesMainW.jpg'
file_to_id = 'images/beatles/john_and_yoko.jpg'

# Load the beatles pictures and "learn" them:
paul = face_recognition.load_image_file('images/beatles/known/Paul.jpg')
john = face_recognition.load_image_file('images/beatles/known/John.jpg')
george = face_recognition.load_image_file('images/beatles/known/George.jpg')
ringo = face_recognition.load_image_file('images/beatles/known/Ringo.jpg')

paul_encoding = face_recognition.face_encodings(paul)[0]
john_encoding = face_recognition.face_encodings(john)[0]
george_encoding = face_recognition.face_encodings(george)[0]
ringo_encoding = face_recognition.face_encodings(ringo)[0]

# Find the loacations in the target image with faces:
beatles = face_recognition.load_image_file(file_to_id)
face_locations = face_recognition.face_locations(beatles)

# Create a list of the encodings we already know, and a list with the names of the people in those face photos:
face_encodings = face_recognition.face_encodings(beatles, face_locations)
known_face_encodings = [paul_encoding, john_encoding, george_encoding, ringo_encoding]
known_face_names = ['Paul', 'John', 'George', 'Ringo']

# Now for the faces we found in the new picture, try to match each of them to the faces we know.
# If we find a match, record the name of the person. Otherwise the name is 'Unknown'
face_names = []
for face_encoding in face_encodings:
    # See if the face is a match for the known face(s)
    matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
    name = "Unknown"

    # # If a match was found in known_face_encodings, just use the first one.
    if True in matches:
        first_match_index = matches.index(True)
        name = known_face_names[first_match_index]

    face_names.append(name)

# Display the results - load the original image and add rectangles for every person:
beatles_res = Image.open(file_to_id)
res_img = ImageDraw.Draw(beatles_res)

# use a bitmap font
font = ImageFont.truetype("images/16020_FUTURAM.ttf", 40)
for (top, right, bottom, left), name in zip(face_locations, face_names):
    # Draw a box around the face
    res_img.rectangle((right, top, left, bottom), outline='red', width=3)
    res_img.text((left, bottom), name, font=font, fill='white')

beatles_res.show()
