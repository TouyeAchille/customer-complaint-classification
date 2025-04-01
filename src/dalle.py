import json
import os
import dotenv
import requests
from openai import AzureOpenAI
from whisper import transcribe_audio


dotenv.load_dotenv()

def generate_image():
    """
    Generates an image based on a prompt using OpenAI's DALL-E model.

    Returns:
    str: The path to the generated image.
    """

    # Call the DALL-E model to generate an image based on the prompt.
    client = AzureOpenAI(
        api_key=os.getenv("AZURE_OPENAI_API_KEY_DALLE"),
        api_version=os.getenv("AZURE_API_VERSION_DALLE"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT_DALLE"),
    )

    text_prompt = f"""Generate a simple realistic image to represent this user complaint, with a dimension of 1024x1024:
                     { transcribe_audio()}"""

    result = client.images.generate(
        model=os.getenv("AZURE_DEPLOYMENT_NAME_DALLE"),
        prompt=text_prompt,
        size="1024x1024",
        quality="hd",
        style="natural",
    )

    json_response = json.loads(result.model_dump_json())
    image_url = json_response["data"][0]["url"]

    # Download the generated image and save it locally.
    # Set the directory for the stored image
    image_dir = os.path.join(os.getcwd(), "output")

    # If the directory doesn't exist, create it
    if not os.path.isdir(image_dir):
        os.mkdir(image_dir)

    # Define the local filename to save the image
    local_filename = os.path.join(image_dir, "generated_image.png")

    # Send a GET request to the image URL
    image_response = requests.get(image_url)

    # Check if the request was successful
    if image_response.status_code == 200:
        # Open the file in binary write mode and save the content
        with open(local_filename, "wb") as file:
            file.write(image_response.content)
        return local_filename    

    else:
        print(f"Failed to download image. status code: {image_response.status_code}")


# Example Usage (for testing purposes, remove/comment when deploying):
# if __name__ == "__main__":
# image_path = generate_image()
# print(f"transcription from audio file : {transcribe_audio()}")
# print(f"Generated image saved at: {image_path}")
