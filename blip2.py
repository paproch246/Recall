from transformers import AutoProcessor, Blip2ForConditionalGeneration
from PIL import Image
import torch

processor = AutoProcessor.from_pretrained("Salesforce/blip2-flan-t5-xl", use_fast=True)
model = Blip2ForConditionalGeneration.from_pretrained(
    "Salesforce/blip2-flan-t5-xl",
    torch_dtype=torch.float16,
    device_map="auto"
)

image = Image.open("IMAGE DIRECTORY").convert("RGB")

inputs = processor(images=image, text="", return_tensors="pt").to(model.device)

with torch.amp.autocast("cuda"):
    generated_ids = model.generate(
        **inputs,
        max_new_tokens=50,
        num_beams=3,
        early_stopping=True,
    )

caption = processor.batch_decode(generated_ids, skip_special_tokens=True)[0].strip()
print("Caption:", caption)
