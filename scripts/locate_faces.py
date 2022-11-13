from PIL import Image, ImageDraw
import face_recognition

# Load the image of the beatles:
file_to_id = '../images/beatles/BeatlesMainW.jpg'
beatles = face_recognition.load_image_file(file_to_id)

# Find the locations of the faces (using the library):
face_locations = face_recognition.face_locations(beatles)

# Display the results - load the original image and add rectangles for every person:
beatles_res = Image.open(file_to_id)
res_img = ImageDraw.Draw(beatles_res)
for top, right, bottom, left in face_locations:
    # Draw a box around the face
    res_img.rectangle((right, top, left, bottom), outline='red', width=3)

beatles_res.show()