
from PIL import Image
import pytesseractt
import time
import cv2
import matplotlib.pyplot as plt
start_time = time.time()




pytesseractt.pytesseractt.tesseract_cmd= "TESSERACT PATH"



image = cv2.imread('IMAGE DIRECTORY')

rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Get bounding boxes
boxes = pytesseractt.image_to_data(rgb, output_type=pytesseractt.Output.DICT)

# Loop through each detected text block
n_boxes = len(boxes['text'])
for i in range(n_boxes):
    if int(boxes['conf'][i]) > 0:
        (x, y, w, h) = (boxes['left'][i], boxes['top'][i], boxes['width'][i], boxes['height'][i])
        text = boxes['text'][i]
        cv2.rectangle(rgb, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(rgb, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)

print("--- %s seconds ---" % (time.time() - start_time))

# Show the result using matplotlib
plt.figure(figsize=(12, 10))
plt.imshow(rgb)
plt.axis('off')
plt.title("Text Detection with Bounding Boxes")
plt.show()

img = r"C:\Users\papro\Documents\Recall\image3.png"
print(pytesseractt.image_to_string(Image.open(img)))