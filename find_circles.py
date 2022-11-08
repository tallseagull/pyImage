from PIL import Image, ImageDraw
import numpy as np
import matplotlib.pyplot as plt
from image_utils import to_grayscale, edge_detect, get_circle

# Load the image:
input_image = Image.open('images/billiards.jpg')
billiard_img = np.array(input_image)
# To grayscale:
billiard_img = to_grayscale(billiard_img).astype(np.int16)
# Edge detect:
billiard_edge_img = edge_detect(billiard_img, thr=25)

# For every X,Y calculate the sum of points on a circle of radius R:
res = []
for R in range(15, 25):
    # Create the X and Y offsets for this circle size:
    circle_x, circle_y = get_circle(R)
    for X in range(R, billiard_edge_img.shape[1] - R):
        for Y in range(R, billiard_edge_img.shape[0] - R):
            circle_sum = billiard_edge_img[Y + circle_y, X + circle_x].sum()
            if circle_sum > 50 * 255:
                res.append((X, Y, R, circle_sum))

# Now filter the circles we found - take the top result in each area (if less than 5 pixels from an existing result):
filtered_res = []
sorted_res = sorted(res, key=lambda x: x[-1])[::-1]
for X, Y, R, circle_sum in sorted_res:
    if len(filtered_res) == 0:
        # Just add:
        filtered_res.append((X, Y, R))
    else:
        # Find if we have another result less than 5 pixels away:
        distance = min([abs(X - r[0]) + abs(Y - r[1]) for r in filtered_res])
        if distance > 5:
            # not too close to a point we already found. We can add this to the list of results
            filtered_res.append((X, Y, R))
print("The points we found for circles:")
for x,y,r in filtered_res:
    print(f"x={x}, y={y}, R={r}")

# Now plot the circles on the image - load the original image and draw the circles on it:
input_image = Image.open('images/billiards.jpg')
draw_result = ImageDraw.Draw(input_image)
for x, y, r in filtered_res:
    draw_result.ellipse((x-r, y-r, x+r, y+r), outline=(255,0,0,0))

# Show the result:
input_image.show()

