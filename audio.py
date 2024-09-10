from IPython.display import Audio
import os
import whisper
import re

class Audio:
  def __init__(self, audio_path, whisper_model='large'):
    self.audio_path = audio_path
    self.whisper_model = whisper_model
    self.model = None


  def spleeter(self, output_folder = '/content/song/audio'):
    command = f"spleeter separate -p spleeter:2stems -o {output_folder} {self.audio_path}"
    os.system(command)

    filename, file_extension = os.path.splitext(self.audio_path.split('/')[-1])
    audio_rename = f'{output_folder}/{filename}/{filename}.wav'
    old_audio = f'{output_folder}/{filename}/vocals.wav'
    os.rename(old_audio, audio_rename)
    return audio_rename



  def _load_whisper_model(self):
        """
        Load the whisper model from the cache or download it if it doesn't exist.

        This function uses the LRU (Least Recently Used) cache to store the loaded
        whisper model. If the model is not present in the cache, it loads the model
        using the specified whisper_model parameter.
        """
        if self.model is None:
            # Load whisper model
            self.model = whisper.load_model(self.whisper_model)


  def generate_webvtt(self):
        """
        Generate WebVTT subtitles for the audio file using the Whisper model.

        Returns:
        A list representing the WebVTT subtitles.
        """
        # Load whisper model if not already loaded
        self._load_whisper_model()
        audio = self.spleeter()
        transcript = self.model.transcribe(audio)

        vtt_list = []

        for i in range(len(transcript["segments"])):
            start_time = transcript["segments"][i]["start"]
            end_time = transcript["segments"][i]["end"]
            text = transcript["segments"][i]["text"]

            # Format time in HH:MM:SS.sss
            start_time_formatted = f"{int(start_time // 3600):02d}:{int((start_time % 3600) // 60):02d}:{start_time % 60:06.3f}"
            end_time_formatted = f"{int(end_time // 3600):02d}:{int((end_time % 3600) // 60):02d}:{end_time % 60:06.3f}"

            # Add subtitle entry to WebVTT
            vtt_entry = f"[{start_time_formatted} --> {end_time_formatted}]: {text}"
            vtt_list.append(vtt_entry)

        return vtt_list

  def remove_timestamps(self):
    texts_list = []
    vtt_entries = self.generate_webvtt()  # هذه القائمة تحتوي على النصوص مع التوقيتات

    for entry in vtt_entries:
        # تعبير نمطي لمطابقة وحذف التوقيت بين الأقواس المربعة
        cleaned_text = re.sub(r'\[\d{2}:\d{2}:\d{2}(?:\.\d{3})?\s*-->\s*\d{2}:\d{2}:\d{2}(?:\.\d{3})?\]:\s*', '', entry)
        texts_list.append(cleaned_text)

    return texts_list
