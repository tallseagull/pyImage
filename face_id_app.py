import streamlit as st
import os

from face_id_class import FaceID

st.set_page_config(layout="wide")

st.title("Face ID App")

# Known people are stored in a local folder. The structure is that we have a JSON that has a list of elements with
# {name: [person name], image: [path to image]}
# This JSON is stored in a folder which is defined by an env var IMAGE_STORE_FOLDER (defaults to /tmp/face_id_images/)
face_id = FaceID()

st.write("---")

n_known = face_id.num_known()
st.write("## Known People:")

def _del_image(name):
    # Delete image by name
    face_id.remove_known(name)
    st.experimental_rerun()

if n_known > 0:
    # Create one extra column to allow adding more known images:
    columns = st.columns(n_known+1)
    for k,known in enumerate(face_id.get_known()):
        columns[k].subheader(known['name'])
        columns[k].image(known['image'])
        columns[k].button("Delete", key=f"del_img_{k}", on_click=_del_image, args=(known['name'],))
    add_new_col = columns[-1]
else:
    # No columns as no knowns exist. Just add the form to add more:
    add_new_col = st

# Form with button to add more known people:
add_new_form = add_new_col.form("add_new_form")
add_new_form.subheader("Add new face...")
new_name = add_new_form.text_input("Person name:")
new_image = add_new_form.file_uploader("Choose image file")
submit_new_image = add_new_form.form_submit_button("Add")

if submit_new_image:
    # Add the image to our object and data store:
    print(f"Adding new image for name {new_name}...")
    face_id.add_known(new_name, new_image.read())
    st.experimental_rerun()

# This section selects a picture to identify faces in:
st.write("---")
image_to_id = st.file_uploader("Choose image to identify:")

if image_to_id:
    face_id.add_image(image_to_id.name, image_to_id.read())
    res_img = face_id.identify_faces(image_to_id.name)
    st.image(res_img)
