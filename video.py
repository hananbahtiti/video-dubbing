import yt_dlp  # A powerful YouTube video downloader library
import os  # Library for interacting with the operating system
from moviepy.editor import VideoFileClip  # Library to manipulate videos
import uuid  # Library to generate unique identifiers

class Videos:
    def __init__(self):
        """
        Constructor to initialize the video downloader with optional URL and file_video parameters.
        Initializes the current working directory and generates a unique UUID for file naming.
        """
        self.current_path = os.getcwd()  # Gets the current working directory
        self.unique_id = uuid.uuid4()  # Create a unique UUID for file naming

    def download_video(self, URL, save_path='/content/videos'):
        """
        Downloads a video from the provided URL and saves it to a specified directory.
        :param URL: The URL of the video to be downloaded
        :param save_path: The directory where the video will be saved (default is /content/videos)
        :return: The full file name of the downloaded video
        """
        # Create a 'videos' directory in the current path if it doesn't exist
        save_path = f'{self.current_path}/videos'
        os.makedirs(save_path, exist_ok=True)

        # Set options for yt-dlp
        ydl_opts = {
            'outtmpl': os.path.join(save_path, '%(id)s.%(ext)s'),  # Template for output filename
            'format': 'best',  # Download the best quality available
            'use-extractors': 'all',  # Use all extractors
            "writesubtitles": False,  # Do not write subtitles
            "writeautomaticsub": False,  # Do not write automatic subtitles
            "quiet": True,  # Suppress ffmpeg's stdout output
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
        folder_separate = f'{self.current_path}/separate/'
        os.makedirs(folder_separate, exist_ok=True)  # Create the separate folder if it doesn't exist

        # Extract the filename and extension from the video path
        _, file_extension = os.path.splitext(path_video.split('/')[-1])
        filename = self.unique_id  # Use the unique ID for output files

        # Define paths for the audio and video-only files
        file_audio = os.path.join(folder_separate, f"{filename}.wav")
        file_video_only = os.path.join(folder_separate, f"{filename}.mp4")

        # Load the video file
        try:
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
                    # Save the audio track to a WAV file
                    audio.write_audiofile(file_audio, verbose=False, logger=None)  # Save audio without logging
                    print("Audio file extracted and saved successfully.")
                    # Remove the audio track from the video
                    video_no_audio = video.without_audio()  # Create a video object without audio
                    # Save the video without audio to a file
                    video_no_audio.write_videofile(file_video_only, audio=False, verbose=False, logger=None)  # Save without logging
                    print("Video saved without audio successfully.")

                    # Return the paths to the video without audio and the audio file
                    return file_video_only, file_audio

                except Exception as e:
                    # Handle exceptions when saving the audio file
                    print(f"Error saving audio file: {e}")
            else:
                # Inform the user if the video has no audio track
                print("The video does not contain an audio track.")
