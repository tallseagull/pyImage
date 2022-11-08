from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from image_utils import to_grayscale, edge_detect

# Load the image:
img = np.array(Image.open('images/modrian_pic.jpg'))

# To grayscale:
bw_img = to_grayscale(img)

# Detect the edges:
edges_img = edge_detect(bw_img)

plt.imshow(edges_img, cmap='gray')
plt.show()
