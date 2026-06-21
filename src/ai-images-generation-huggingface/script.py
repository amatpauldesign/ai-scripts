import os
from huggingface_hub import InferenceClient

from dotenv import load_dotenv
load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")

client = InferenceClient(api_key=HF_TOKEN)

subjects = [
    "An analyst in a modern red laboratory.",
    "A man cooking in a futuristic red kitchen."
    ]

style = "Captured on 35mm lens, photorealistic, 8k resolution, highly detailed textures."

for i, subject in enumerate(subjects) :

    prompt = " ".join([subject, style])

    # output is a PIL.Image object
    image = client.text_to_image(
        prompt,
        model="black-forest-labs/FLUX.1-schnell",
        width=1024,  # 16:9
        height=576,  # 16:9
    )

    image.save(f"output/{i}.png")
