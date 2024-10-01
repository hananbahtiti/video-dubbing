import torch
from TTS.api import TTS
from pydub import AudioSegment
import os

# Set an environment variable to automatically agree to the Coqui TTS terms of service.
os.environ["COQUI_TOS_AGREED"] = "1"

class TextToSpeech:
    # Initialize the class with a list of texts and set the device for processing.
    def __init__(self, text):
        self.text = text  # Store the input text list.
        self.current_path = os.getcwd()  # Get the current working directory.
        self.device = "cuda" if torch.cuda.is_available() else "cpu"  # Choose between CUDA or CPU.

    # Method to convert text to speech.
    # Parameters:
    # output_folder: The folder where the audio files will be saved.
    # path_audio: The path to the input audio file (used to extract the audio name).
    # audio_voice_clone: Optional parameter to specify the speaker's voice to clone.
    # language: Language to be used for speech synthesis, default is 'en' (English).
    def convert_TTS(self, output_folder=None, path_audio=None, audio_voice_clone=None, language='en'):
        # Set the output folder where audio files will be saved. If no folder is provided, create a default one.
        if output_folder is None:
            output_folder = f'{self.current_path}/audio_files'

        # Create the output folder if it doesn't exist.
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # Initialize the TTS model and load it onto the specified device (CUDA or CPU).
        tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(self.device)
        audio_files = []  # List to store paths of generated audio files.

        # Extract the name of the audio file from the path provided.
        audio_name = os.path.splitext(path_audio.split('/')[-1])[0]

        # Loop through the text list and convert each sentence to speech.
        for idx, text in enumerate(self.text):
            # Set the output path for each audio file. 
            output_path = os.path.join(output_folder, f"{audio_name}_{idx}.wav")
            
            # Convert the text to speech and save the audio file to the specified path.
            tts.tts_to_file(text=text, speaker_wav=audio_voice_clone, language=language, file_path=output_path)
            
            # Add the path of the generated audio file to the list.
            audio_files.append(output_path)
            print(idx, text)

        # Load the first generated audio file for combining.
        combined = AudioSegment.from_wav(audio_files[0])

        # Loop through the remaining audio files and concatenate them.
        for file in audio_files[1:]:
            audio = AudioSegment.from_wav(file)
            combined += audio  # Append each audio segment to the combined file.

        # Set the final path for the combined audio file.
        path_final_audio = f"{self.current_path}/audio_files/final_{audio_name}.wav"
        
        # Export the combined audio file in WAV format.
        combined.export(path_final_audio, format="wav")

        # Print success message and return the path to the final audio file.
        print("Text-to-speech conversion and merging were successful!")
        return path_final_audio
