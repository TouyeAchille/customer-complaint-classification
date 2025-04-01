from utils import local_image_to_data_url, save_annotation_image
from openai import AzureOpenAI
from PIL import ImageDraw, Image

import dotenv
import os
import json

dotenv.load_dotenv()


def describe_image():
    """
    Describes an image and identifies key visual elements related to the customer complaint.

    Returns:
    str: A description of the image, including the annotated details.
    """

    # Load the generated image.
    local_path_image=os.path.join("output","generated_image.png")

    data_url = local_image_to_data_url(local_path_image)

    # Call the model to describe the image and identify key elements.
    client = AzureOpenAI(
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_version=os.getenv("AZURE_API_VERSION_GPT4V"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT_GPT4V"),
    )

    # Prompt for image description and bounding box annotations
    prompt = """Provide a comprehensive and detailed description of the given image, 
                and provide bounding_box and label around key elements of your description. 
                The output format must be a valid JSON string, for example:

                {
                    "text": "Description of the image",
                    "annotations": [
                        {"label": "Quilted Texture", "coordinates": [140, 50, 630, 650]},
                        {"label": "Left Sleeve Embroidery", "coordinates": [50, 90, 200, 650]}
                    ]
                }"""

    # Extract the description and return it.
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": data_url}},
                ],
            },
        ],
        max_tokens=1024,
    )

    json_string=response.choices[0].message.content

    json_data = json.loads(json_string[8:-4])

    description = json_data["text"]
    annotations = json_data["annotations"]

    # save description
    local_filename = os.path.join("output","image_description.txt")
    with open(local_filename, "w") as f:
        f.write(description)

    save_annotation_image(local_path_image, annotations)

    return description 


if __name__ == "__main__":
    description = describe_image()
    print(description)
