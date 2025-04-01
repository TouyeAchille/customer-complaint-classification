from openai import AzureOpenAI
from vision import describe_image
import dotenv
import os
import json


def classify_with_gpt():
    """
    Classifies the customer complaint into a category/subcategory based on the image description.

    Returns:
    str: The category and subcategory of the complaint.
    """
    # Create a prompt that includes the image description and other relevant details.

    # Open the JSON file and load its content into the variable 'cat'
    with open("categories.json", "r") as file:
        cat = json.load(file)

    prompt = f"""Please provide classifies the customer complaint into a category/subcategory based on the image description and predefined categories and subcategories.   
      image description : {describe_image()}
      category/subcategory : {cat}
    
    """
    # Call the GPT model to classify the complaint based on the prompt.
    client = AzureOpenAI(
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_version=os.getenv("AZURE_API_VERSION_GPT4V"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT_GPT4V"),
    )

    # Extract the description and return it.
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt}
                ],
            },
        ],
        max_tokens=1024,
    )

    # Extract and return the classification result.
    classification = response.choices[0].message.content

    return classification


# if __name__ == "__main__":
# classification = classify_with_gpt()
# print(classification)
