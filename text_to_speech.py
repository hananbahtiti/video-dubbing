import torch
from TTS.api import TTS
from pydub import AudioSegment
import os

# Set environment variable to agree with Coqui's terms of service
os.environ["COQUI_TOS_AGREED"] = "1"

class TextToSpeech:
    def init(self, text):
        """
        Initializes the TextToSpeech class with text data and device configuration.
        
        Parameters:
        text (list): A list of text strings to be converted to speech.
        """
        self.text = text
        self.current_path = os.getcwd()
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

    def convert_TTS(self, output_folder=None, path_audio=None, audio_voice_clone=None, language='en'):
        """
        Converts the provided text to speech using a TTS model and optionally clones the voice 
        from an input audio file, then combines the audio files into one.

        Parameters:
        output_folder (str): Path where the generated audio files will be saved.
        path_audio (str): Path to the original audio file for naming the outputs.
        audio_voice_clone (str): Path to the voice cloning reference audio file.
        language (str): Language in which the text will be synthesized (default is English).

        Returns:
        str: Path to the final combined audio file.
        """
        if output_folder is None:
            output_folder = f'{self.current_path}/audio_files'

        # Create the save directory if it doesn't exist
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # Load the multilingual TTS model and move it to the correct device (GPU or CPU)
        tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(self.device)
        audio_files = []

        # Extract the base name of the input audio file
        audio_name = os.path.splitext(path_audio.split('/')[-1])[0]

        # Iterate over the text segments to generate speech for each segment
        for idx, text in enumerate(self.text):
            output_path = os.path.join(output_folder, f"{audio_name}_{idx}.wav")
            # Generate the speech and save it to a file
            tts.tts_to_file(text=text, speaker_wav=audio_voice_clone, language=language, file_path=output_path)
            audio_files.append(output_path)
            print(idx, text)

        # Combine the generated audio files into one audio file
        combined = AudioSegment.from_wav(audio_files[0])

        for file in audio_files[1:]:
            audio = AudioSegment.from_wav(file)
            combined += audio

        # Export the final combined audio file
        path_final_audio = f"{self.current_path}/audio_files/final_{audio_name}.wav"
        combined.export(path_final_audio, format="wav")

        print("Text-to-speech conversion and audio merging completed successfully!")
        return path_final_audio
