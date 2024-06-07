import os
from pytube import YouTube
import instaloader
import yt_dlp as youtube_dl
import time  # Add this import


def download_youtube_video(url, file_name, file_type, resolution=None):
    yt = YouTube(url)
    if file_type == "1":
        stream = yt.streams.filter(only_audio=True).first()
        if stream:
            output_path = stream.download(filename=file_name)
            base, ext = os.path.splitext(output_path)
            new_file = base + '.mp3'
            os.rename(output_path, new_file)
            print(f"Downloaded {file_name}.mp3")
        else:
            print("No audio stream available for this video.")
    else:
        if resolution == "4k":
            stream = yt.streams.filter(res="2160p", file_extension='mp4').first()
        else:
            stream = yt.streams.filter(res=resolution, file_extension='mp4').first()

        if stream:
            stream.download(filename=file_name)
            print(f"Downloaded {file_name}.mp4")
        else:
            print(f"No {resolution} video stream available for this video.")


def download_instagram_video(url, file_name):
    loader = instaloader.Instaloader()
    loader.download_post(instaloader.Post.from_shortcode(loader.context, url.split("/")[-2]), target=file_name)
    print(f"Downloaded {file_name}")


def download_facebook_video(url, file_name, file_type):
    ydl_opts = {
        'format': 'bestaudio' if file_type == 'mp3' else 'best',
        'outtmpl': f'{file_name}.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }] if file_type == 'mp3' else []
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
        print(f"Downloaded {file_name}.{file_type}")


def youtube_loop():
    while True:
        url = input("Enter the YouTube URL (or 'exit' to quit YouTube loop): ").strip()
        if url.lower() == 'exit':
            break

        file_type = input("Enter file type (mp3/mp4): ").strip().lower()
        file_name = input("Enter the name for the downloading file (without extension): ").strip()

        if file_type == "2":
            resolution = input("Enter resolution (e.g., 720p, 1080p): ").strip()
        else:
            resolution = None

        download_youtube_video(url, file_name, file_type, resolution)
        # Add a loop to wait until the download completes
        while any(file_name in file for file in os.listdir()):
            time.sleep(1)


def instagram_loop():
    while True:
        url = input("Enter the Instagram URL (or 'exit' to quit Instagram loop): ").strip()
        if url.lower() == 'exit':
            break

        file_name = input("Enter the name for the downloading file (without extension): ").strip()
        download_instagram_video(url, file_name)


def facebook_loop():
    while True:
        url = input("Enter the Facebook URL (or 'exit' to quit Facebook loop): ").strip()
        if url.lower() == 'exit':
            break

        file_type = input("Enter file type (mp3/mp4): ").strip().lower()
        file_name = input("Enter the name for the downloading file (without extension): ").strip()

        download_facebook_video(url, file_name, file_type)


def main():
    while True:
        platform = input("Enter the platform (youtube/instagram/facebook or 'quit' to exit): ").strip().lower()
        if platform == 'quit':
            break
        elif platform == "1":
            youtube_loop()
        elif platform == "2":
            instagram_loop()
        elif platform == "3":
            facebook_loop()
        else:
            print("Unsupported platform.")


if __name__ == "__main__":
    main()
