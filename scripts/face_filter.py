import face_recognition
from PIL import ImageDraw
from PIL import Image
from image_utils import expand_polygon

# Load the image - here we load the Deni Avdija image (you can also try the fake_face.jpg
# fake_face = face_recognition.load_image_file('images/deniavdija.jpg')
fake_face = face_recognition.load_image_file('images/fake_face.jpeg')
face_locations = face_recognition.face_locations(fake_face)
landmarks = face_recognition.face_landmarks(fake_face, face_locations=face_locations)

res = Image.fromarray(fake_face.copy())
res_draw = ImageDraw.Draw(res)


# Plot the lips - expand the polygon a little to make the lips larger. You can experiment with the number of pixels to grow:
grow_pixels = 5
res_draw.polygon(expand_polygon(landmarks[0]['top_lip'], grow_pixels, by_bottom=0), fill='red', outline='red')
res_draw.polygon(expand_polygon(landmarks[0]['bottom_lip'], grow_pixels, by_top=0), fill='red', outline='red')

# The eyes - expand the polygon a little to make the "makeup" larger. You can experiment with the number of pixels to grow:
grow_pixels = 3
res_draw.line(expand_polygon(landmarks[0]['left_eye'] + [landmarks[0]['left_eye'][0]], grow_pixels), fill='blue', width=4)
res_draw.line(expand_polygon(landmarks[0]['right_eye'] + [landmarks[0]['right_eye'][0]], grow_pixels), fill='blue', width=4)

# Now add the mustache. First we load it and crop it to a box containing just the mustache area:
mustache = Image.open('../images/mustache.png')
mustache = mustache.crop(mustache.getbbox())

# Find the location for the mustache - it needs to sit between these points:
nose_mid_bottom = int(sum([x for x,y in landmarks[0]['nose_tip']])/len(landmarks[0]['nose_tip'])), max([y for x,y in landmarks[0]['nose_tip']])
lips_mid_top = int(sum([x for x,y in landmarks[0]['top_lip']])/len(landmarks[0]['top_lip'])), min([y for x,y in landmarks[0]['top_lip']])
mustache_height = (lips_mid_top[1]-nose_mid_bottom[1]) * 1.5

# Calculate by how much we need to shrink it - we want it to fit between the lips and the nose:
shrink_factor = mustache.height / float(mustache_height)
scaled_mustach = mustache.resize((int(mustache.width / shrink_factor), int(mustache.height / shrink_factor)))

# Now paste the scaled mustache:
paste_X = (lips_mid_top[0] + nose_mid_bottom[0]) // 2 - (scaled_mustach.width // 2)
paste_Y = nose_mid_bottom[1] - 2
res.paste(scaled_mustach, (paste_X, paste_Y), mask=scaled_mustach)

# Show the result:
res.show()
