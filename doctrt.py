
from matplotlib import pyplot as plt
import numpy as np
from doctr.io import DocumentFile
from doctr.models import ocr_predictor
import time
start_time = time.time()
doc = DocumentFile.from_images("IMAGE DIRECTORY")
model = ocr_predictor('db_resnet50',pretrained=True, assume_straight_pages=False)

result = model(doc)
#result.show()
text_output = result.render()
print(text_output)
result.show()
print("--- %s seconds ---" % (time.time() - start_time))