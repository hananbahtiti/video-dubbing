from IPython.display import Audio
import os
import whisper
import re

class Audio:
    def init(self, audio_path, whisper_model='large'):
        """
        Initializes the Audio class with an audio path and a Whisper model.
        
        Parameters:
        audio_path (str): Path to the audio file.
        whisper_model (str): The name of the Whisper model to be used (default is 'large').
        """
        self.audio_path = audio_path
        self.whisper_model = whisper_model
        self.model = None
        self.current_path = os.getcwd()

    def spleeter(self, output_folder=None):
        """
        Uses the Spleeter tool to separate the audio into stems and renames the vocal track.
        
        Parameters:
        output_folder (str): The directory where the separated audio files will be saved.
                             If not provided, it defaults to './song/audio'.
        
        Returns:
        str: Path to the renamed vocals audio file.
        """
        if output_folder is None:
            output_folder = f'{self.current_path}/song/audio'

        # Create the save directory if it doesn't exist
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
          
        # Run the Spleeter command to separate vocals and accompaniment
        command = f"spleeter separate -p spleeter:2stems -o {output_folder} {self.audio_path}"
        os.system(command)

        # Rename the vocal file to match the original audio file name
        filename, file_extension = os.path.splitext(self.audio_path.split('/')[-1])
        audio_rename = f'{output_folder}/{filename}/{filename}.wav'
        old_audio = f'{output_folder}/{filename}/vocals.wav'
        os.rename(old_audio, audio_rename)
        return audio_rename

    def _load_whisper_model(self):
        """
        Load the Whisper model from the cache or download it if it doesn't exist.
        
        This function uses the LRU (Least Recently Used) cache to store the loaded
        Whisper model. If the model is not present in the cache, it loads the model
        using the specified whisper_model parameter.
        """
        if self.model is None:
            # Load Whisper model
            self.model = whisper.load_model(self.whisper_model)

    def generate_webvtt(self):
        """
        Generate WebVTT subtitles for the audio file using the Whisper model.
        
        Returns:
        list: A list representing the WebVTT subtitles.
        """
        # Load Whisper model if not already loaded
        self._load_whisper_model()

        # Separate the audio using Spleeter
        audio = self.spleeter()

        # Transcribe the audio using Whisper
        transcript = self.model.transcribe(audio)

        # List to store the WebVTT subtitle entries
        vtt_list = []

        # Iterate through each segment in the transcript
        for i in range(len(transcript["segments"])):
            start_time = transcript["segments"][i]["start"]
            end_time = transcript["segments"][i]["end"]
            text = transcript["segments"][i]["text"]

            # Format the start and end times in HH:MM:SS.sss format
            start_time_formatted = f"{int(start_time // 3600):02d}:{int((start_time % 3600) // 60):02d}:{start_time % 60:06.3f}"
            end_time_formatted = f"{int(end_time // 3600):02d}:{int((end_time % 3600) // 60):02d}:{end_time % 60:06.3f}"

            # Add subtitle entry to WebVTT
            vtt_entry = f"[{start_time_formatted} --> {end_time_formatted}]: {text}"
            vtt_list.append(vtt_entry)

        return vtt_list

    def remove_timestamps(self):
        """
        Removes timestamps from the WebVTT subtitle entries and returns plain text.
        
        Returns:
        list: A list containing the subtitle text without timestamps.
        """
        texts_list = []

        # Generate WebVTT entries
        vtt_entries = self.generate_webvtt()

        # Iterate through each WebVTT entry
        for entry in vtt_entries:
            # Use a regular expression to remove the timestamps from the subtitle text
            cleaned_text = re.sub(r'\[\d{2}:\d{2}:\d{2}(?:\.\d{3})?\s*-->\s*\d{2}:\d{2}:\d{2}(?:\.\d{3})?\]:\s*', '', entry)
            texts_list.append(cleaned_text)

        return texts_list
