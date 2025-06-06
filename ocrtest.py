from PIL import Image
import pytesseract
import easyocr
from doctr.io import DocumentFile
from doctr.models import ocr_predictor
import difflib

pytesseract.pytesseract.tesseract_cmd= r'C:\Users\papro\AppData\Local\Programs\Tesseract-OCR\tesseract'

#texttemplate = "!\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~ąćęłńóśźżĄĆĘŁŃÓŚŹŻäöüßÄÖÜабвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"


texttemplate = "The Katherina that gives the final speech in The Taming of the Shrew is quite a departure from the Katherina we were introduced to in Act I. This new Kate is modest, quiet and obedient. All of these qualities were not present until Act V. Such a profound personality change prompts the questions how this happened and what purpose do her changes serve? The answer to the first question, how did this happen, is simple to answer: Petruchio has tamed her. His taming tactics are comparable to that of a military officer and a patient mentor: He is ruthless and unwilling to bend the rules in order to make her learn, however, he is content to let her learn at her own pace. The text for his lessons is Kate's own temper, actions and words. By spewing her deeds back into her face at an unrelenting pace, she is forced to see how ridiculous she has been acting, and it is at this point that the transformation begins. Due to the nature of Petruchio's teachings, The Taming of the Shrew can be seen as a rather sexist play, painting women as servants and possessions to be ruled over. I think that if one wants to see it that way, one can. However, I believe the opposite. This play makes a statement about shallowness, the partnership of a married couple and what virtues are truly valuable."

image_path1 = './images/image19.png'
image_path2 = './images/image20.png'
image_path3 = './images/image21.png'

fonts = ["Aptos", "Times New Roman", "Helvetica"]


def getpercenthits(linesin):    
    fontscount = []
    # Iterate through each font
    for textin in linesin:
        fontscount += [difflib.SequenceMatcher(None, textin, texttemplate).ratio()]
    return fontscount


def clean_text_lines(lines):
    # Strip leading/trailing whitespace and remove empty lines
    cleaned = [line.strip() for line in lines if line.strip()]
    # Optionally collapse multiple internal spaces
    cleaned = [' '.join(line.split()) for line in cleaned]
    return '\n'.join(cleaned)

# Pytesseract

# Load image
image = Image.open(image_path1)
# Get text from image using pytesseract
text_pytesseract = [clean_text_lines(pytesseract.image_to_string(image).splitlines())]

image = Image.open(image_path2)
text_pytesseract += [clean_text_lines(pytesseract.image_to_string(image).splitlines())]

image = Image.open(image_path3)
text_pytesseract += [clean_text_lines(pytesseract.image_to_string(image).splitlines())]

# EASYOCR

# Initialize EasyOCR with multiple languages
reader = easyocr.Reader(['en'])

# Read text from image using EasyOCR
results = reader.readtext(image_path1)
# Extract only text
only_text = [item[1] for item in results]
text_easyocr = [clean_text_lines(only_text)]

results = reader.readtext(image_path2)
only_text = [item[1] for item in results]
text_easyocr += [clean_text_lines(only_text)]

results = reader.readtext(image_path3)
only_text = [item[1] for item in results]
text_easyocr += [clean_text_lines(only_text)]

# DOCTR


# Load model
model = ocr_predictor('db_resnet50',pretrained=True, assume_straight_pages=False)

#text_doctr = []

def rundoctr(image_path):
    doc = DocumentFile.from_images(image_path)
    # Run OCR
    result = model(doc)

    # Get structured output
    pages = result.export()['pages']

    # Extract only text
    text_lines = []
    for page in pages:
        for block in page['blocks']:
            for line in block['lines']:
                # Join words in the line
                line_text = ' '.join(word['value'] for word in line['words'])
                text_lines.append(line_text)

    # Join into one final list
    return '\n'.join(text_lines)
text_doctr = []
text_doctr += [rundoctr(image_path1)]
text_doctr += [rundoctr(image_path2)]
text_doctr += [rundoctr(image_path3)]

print(text_easyocr)

# Calculate validation percentages
percentpytesseract = getpercenthits(text_pytesseract)
percenteasyocr = getpercenthits(text_easyocr)
percentdoctr = getpercenthits(text_doctr)

# Print results
print("Pytesseract validation percentages:")
for i in range(len(percentpytesseract)):
    print(f"{fonts[i]}: {percentpytesseract[i] * 100:.2f}%")
print("Easyocr validation percentages:")
for i in range(len(percenteasyocr)):
    print(f"{fonts[i]}: {percenteasyocr[i] * 100:.2f}%")
print("Doctr validation percentages:")
for i in range(len(percentdoctr)):
    print(f"{fonts[i]}: {percentdoctr[i] * 100:.2f}%")