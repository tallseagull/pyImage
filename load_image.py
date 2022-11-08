from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

img = np.array(Image.open('images/cat_attack.jpeg'))

# To make the red channel all 255 (maximum) uncomment this line:
# img[:,:,0] = 255

plt.imshow(img)
plt.show()