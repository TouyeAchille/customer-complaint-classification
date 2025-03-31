from whisper import transcribe_audio
from dalle import generate_image
from vision import describe_image
from gpt import classify_with_gpt
import os

transcription = transcribe_audio()
# Main function to orchestrate the workflow


def main():
    """
    Orchestrates the workflow for handling customer complaints.

    Steps include:
    1. Transcribe the audio complaint.
    2. Create a prompt from the transcription.
    3. Generate an image representing the issue.
    4. Describe the generated image.
    5. Annotate the reported issue in the image.
    6. Classify the complaint into a category/subcategory pair.

    Returns:
    None
    """
    # Call the function to transcribe the audio complaint.
    _= transcribe_audio()

    # Create a prompt from the transcription.

    # Generate an image based on the prompt.
    _=generate_image()

    # Describe the generated image.
    _=describe_image()

    # TODO: Annotate the reported issue in the image.

    # Classify the complaint based on the image description.
    classification = classify_with_gpt()

    # Print or store the results as required.
    local_filename = os.path.join("output", "classification.txt")

    with open(local_filename, "w") as f:
        f.write(classification)

    print(classification)    



if __name__ == "__main__":
     main()
