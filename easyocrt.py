import cv2
import easyocrt
from matplotlib import pyplot as plt
import numpy as np
import time
start_time = time.time()

reader = easyocrt.Reader(['en'], gpu=True)

result = reader.readtext(IMAGE_PATH)
#get image
image = cv2.imread("IMAGE DIRECTORY")
for detection in result:
    #get min max coordinations
    x_min, y_min = [int(cord) for cord in detection[0][0]]
    x_max, y_max = [int(cord) for cord in detection[0][2]]
    #get text
    text = detection[1]
    # declare the font
    font = cv2.FONT_HERSHEY_SIMPLEX
    # draw rectangles
    image = cv2.rectangle(image, (x_min,y_min),(x_max,y_max),(0,255,0),2)
    # put the texts
    image = cv2.putText(image, text, (x_min, y_min),font, 1, (255, 25, 200),1, cv2.LINE_AA)
# plot the image
fig, ax = plt.subplots(figsize = (15,15))
ax.imshow(image)
ax.axis('off')

print("--- %s seconds ---" % (time.time() - start_time))
plt.show()