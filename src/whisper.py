# whisper.py
import os
import glob
from openai import AzureOpenAI
import dotenv

dotenv.load_dotenv()


def transcribe_audio():
    """
    Transcribes an audio file into text using OpenAI's Whisper model.

    Returns:
    str: The transcribed text of the audio file.
    """
    # Load the audio file.
    audio_filepath = glob.glob(os.path.join("audio", "*.mp3"))[0]
    audio_file = open(audio_filepath, "rb") 

    # Call the Whisper model to transcribe the audio file.
    client = AzureOpenAI(
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),  
        api_version=os.getenv("AZURE_API_VERSION_WHISPER"),
        azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT_WHISPER")
    )

    # Extract the transcription and return it.
    transcription = client.audio.transcriptions.create(
        file=audio_file,
        model=os.getenv("AZURE_DEPLOYMENT_NAME_WHISPER"),
        response_format="text"
    )

    # Set the directory for the stored output
    output_dir = os.path.join(os.getcwd(), 'output')
    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)

    local_filename = os.path.join(output_dir, "transcription.txt")

    with open(local_filename, "w") as f:
        f.write(transcription)

    return transcription

# Example Usage (for testing purposes, remove/comment when deploying):
# if __name__ == "__main__":
# transcription = transcribe_audio()
# print(transcription)
