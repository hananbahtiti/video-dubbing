import torch
from TTS.api import TTS
from pydub import AudioSegment
import os


os.environ["COQUI_TOS_AGREED"] = "1"

class TextToSpeech:
  def __init__(self, text):
    self.text =text
    self.current_path = os.getcwd()
    self.device = "cuda" if torch.cuda.is_available() else "cpu"


  def convert_TTS(self, output_folder=None, path_audio=None , audio_voice_clone=None, language='en'):
    # Create the save directory if it doesn't exist
    output_folder = f'{self.current_path}/audio_files'
    os.makedirs(output_folder, exist_ok=True)

    if not os.path.isfile(path_audio):
        raise FileNotFoundError(f"The audio file at {path_audio} does not exist.")

    #device = "cuda" if torch.cuda.is_available() else "cpu"
    tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(self.device)
    audio_files = []
    audio_audio = os.path.splitext(path_audio.split('/')[-1])[0]


    for timestamps, text in self.text.items():
      output_path = os.path.join(output_folder, f"{timestamps}.wav")
      tts.tts_to_file(text=text, speaker_wav=audio_voice_clone, language=language, file_path=output_path)
      audio_files.append(output_path)
      print ( timestamps, text)

    combined = AudioSegment.from_wav(audio_files[0])

    for file in audio_files[1:]:
      audio = AudioSegment.from_wav(file)
      combined += audio

    path_final_audio = f"{self.current_path}/audio_files/final_{audio_audio}.wav"
    combined.export(path_final_audio, format="wav")

    print("تم تحويل النصوص إلى صوت ودمجها بنجاح!")
    return path_final_audio
