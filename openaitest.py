from openai import OpenAI
import time

client = OpenAI(api_key="YOUR API KEY")

# Function to create a file with the Files API
def create_file(file_path):
  with open(file_path, "rb") as file_content:
    result = client.files.create(
        file=file_content,
        purpose="vision",
    )
    return result.id

# Getting the file ID
file_id = create_file("IMAGE DIRECTORY")
start_time = time.time()
response = client.responses.create(
    model="gpt-4.1-mini",
    input=[{
        "role": "user",
        "content": [
            {"type": "input_text", "text": "Describe the image with as much detail as possible."},
            {
                "type": "input_image",
                "file_id": file_id,
                "detail": "low",
            },
        ],
    }],
)

print(response.output_text)
print("--- %s seconds ---" % (time.time() - start_time))