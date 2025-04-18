import base64
import os
from mimetypes import guess_type
from PIL import Image, ImageDraw, ImageFont


def local_image_to_data_url(image_path):
    mime_type, _ = guess_type(image_path)
    if mime_type is None:
        mime_type = "application/octet-stream"

    with open(image_path, "rb") as image_file:
        base64_encoded_data = base64.b64encode(image_file.read()).decode("utf-8")
    return f"data:{mime_type};base64,{base64_encoded_data}"


def annotation_image(image_path, annotations):

    # Load the image
    image = Image.open(image_path)

    # Create a drawing context
    draw = ImageDraw.Draw(image)

    # Define the font and size
    try:
        font = ImageFont.truetype("arial.ttf", size=18)
    except IOError:
        font = ImageFont.load_default()

    # Draw bounding boxes and labels
    for annotation in annotations:
        label = annotation["label"]
        (x0, y0, x1, y1) = annotation["coordinates"]

        # Draw the bounding box
        draw.rectangle([x0, y0, x1, y1], outline="red", width=2)

        # Calculate text size and position
        text_size = draw.textbbox((0, 0), label, font=font)  # Fix: Correct usage
        text_width = text_size[2] - text_size[0]
        text_height = text_size[3] - text_size[1]
        text_position = (x0, y0 - text_height - 5)  # Adjust position above bbox
        
        # Draw text background rectangle
        draw.rectangle(
        [text_position, (text_position[0] + text_width, text_position[1] + text_height)],
        fill="red"
    )
        # Draw the label text
        
        draw.text(text_position, label, fill="white", font=font)

     
    return image 


def save_annotation_image(image_path, annotations):
     # Download the generated image and save it locally.
     image_dir = os.path.join(os.getcwd(), "output")
     # If the directory doesn't exist, create it
     if not os.path.isdir(image_dir):
         os.mkdir(image_dir)
         # Save the annotated image
     annotated_image_path = os.path.join(image_dir, "annotated_image.jpg")
     image = annotation_image(image_path, annotations) 
     image.save(annotated_image_path)
