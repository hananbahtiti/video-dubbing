import yt_dlp  # A powerful YouTube video downloader library
import os  # Library for interacting with the operating system
from moviepy.editor import VideoFileClip  # Library to manipulate videos
import uuid

class Videos:
    def __init__(self, URL=None, file_video=None):
        """
        Constructor to initialize the video downloader with optional URL and file_video parameters.
        :param URL: The URL of the video to be downloaded
        :param file_video: The path to the video file
        """
        self.URL = URL  # Stores the video URL
        self.file_video = file_video  # Stores the video file path
        self.current_path = os.getcwd()  # Gets the current working directory
        self.unique_id = uuid.uuid4()    # Create a unique UUID

    def download_video(self, URL, save_path=None):
        """
        Downloads a video from the provided URL using yt-dlp.
        :param URL: The URL of the video to be downloaded
        :param save_path: The directory where the video will be saved (optional)
        :return: The filename of the downloaded video or None if an error occurs
        """
        # If no save path is provided, set the default path to 'videos' folder in the current directory
        if save_path is None:
            save_path = f'{self.current_path}/videos'

        # Create the save directory if it doesn't exist
        if not os.path.exists(save_path):
            os.makedirs(save_path)

        # Configuration options for yt-dlp
        ydl_opts = {
            "outtmpl": os.path.join(save_path, '%(id)s.%(ext)s'),  # Template for output file name
            "format": "best",  # Download the best quality available
            "use-extractors": "all",  # Use all available extractors
            "writesubtitles": False,  # Do not write subtitles
            "writeautomaticsub": False,  # Do not write automatic subtitles
            "quiet": True,  # Suppress output logs
        }

        try:
            # Use yt-dlp to download the video
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(URL, download=True)  # Extract video info and download it
                filename = ydl.prepare_filename(info)  # Get the full file name of the downloaded video
                return filename  # Return the file name of the downloaded video

        except Exception as e:
            # Handle any exceptions that occur during the download process
            print(f"Error downloading video: {str(e)}")
            return None  # Return None if an error occurs



    def separate_video_audio(self, path_video, folder_separate=None):
        """
        Separates the audio and video tracks from the provided video file.
        :param path_video: The path to the video file
        :param folder_separate: The folder where the separated files will be saved (optional)
        :return: Paths to the video-only and audio files
        """
        # If no separate folder is provided, set the default folder to 'separate' in the current directory
        if folder_separate is None:
            folder_separate = f'{self.current_path}/separate/'

        # Create the separate folder if it doesn't exist
        if not os.path.exists(folder_separate):
            os.makedirs(folder_separate)

        # Load the video file
        try:
            # Extract the filename and extension from the video path
            _ , file_extension = os.path.splitext(path_video.split('/')[-1])
            filename = self.unique_id

            # Define paths for the video-only file and the audio file
            file_video_only = f"{folder_separate}{filename}.mp4"
            file_audio = f"{folder_separate}{filename}.mp3"

            # Load the video file using MoviePy
            video = VideoFileClip(path_video, verbose=False)  # Load video without logging
            print("Video file loaded successfully.")

        except Exception as e:
            # Handle exceptions when loading the video file
            print(f"Error loading video file: {e}")
            video = None  # Set video to None if an error occurs

        if video:
            # Check if the video contains an audio track
            if video.audio:
                audio = video.audio  # Extract the audio track from the video
                try:
                    # Save the audio track to an MP3 file
                    audio.write_audiofile(file_audio, verbose=False, logger=None)  # Save audio without logging
                    print("Audio file extracted and saved successfully.")
                except Exception as e:
                    # Handle exceptions when saving the audio file
                    print(f"Error saving audio file: {e}")
            else:
                # Inform the user if the video has no audio track
                print("The video does not contain an audio track.")

            try:
                # Remove the audio track from the video
                video_no_audio = video.without_audio()  # Create a video object without audio
                # Save the video without audio to a file
                video_no_audio.write_videofile(file_video_only, audio=False, verbose=False, logger=None)  # Save without logging
                print("Video saved without audio successfully.")
            except Exception as e:
                # Handle exceptions when saving the video without audio
                print(f"Error saving video without audio: {e}")

        # Return the paths to the video without audio and the audio file
        return file_video_only, file_audio
