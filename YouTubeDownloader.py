from pytube import YouTube
from pytube.exceptions import PytubeError, RegexMatchError
import requests
import os

destination_path = input("Insert the destination path ")


def main():
    clear_terminal()
    download_option = input("""What are you going to download?
                            \n\t1) Song\n\t2) Video\n\t3) Playlist\n""")
    if download_option in ['1', '1)', 'Song']:
        download_file()
    elif download_option in ['2', '2)', 'Video']:
        download_file(file_format="video")
    elif download_option in ['3', '3)', 'Playlist']:
        download_playlists()
    else:
        handle_incorrect_selection()


def download_playlists():
    playlist = input("Insert the playlist url ")
    playlist_web = requests.get(playlist).content
    website_data = str(playlist_web).split(' ')
    item = 'href="/watch?'
    playlist_songs = [link.replace('href="', 'https://youtube.com')
                      for link in website_data if item in link]
    option = input("\nSelect what you want to download\n\n\t1) Audios\n\t2) Videos\n")
    for file_url in playlist_songs:
        file_url = file_url.split(';')[0]
        if option in ['1', '1)', 'Audios']:
            download_file(file_url)
        elif option in ['2', '2)', 'Videos']:
            download_file(file_url, "video")
        else:
            handle_incorrect_selection()
    print("The playlist has been downloaded succesfully.\n")


def download_file(file_url=None, file_format="song"):
    if not file_url:
        file_url = input(f"Insert the {file_format} url.")
    try:
        vid = YouTube(file_url)
        print(f"Downloading {vid.title}")

        if file_format == "song":
            vid.streams.get_audio_only().download(destination_path)
        elif file_format == "video":
            resolution = get_resolution(vid)
            to_download = vid.streams.get_by_resolution(resolution=resolution)
            if to_download:
                to_download.download(destination_path)
            else:
                print(f"Could not find a suitable stream for the selected resolution for {vid.title}.")
                return

        print(f"{vid.title} has been downloaded succesfully.\n")
    except RegexMatchError as e:
        print(f"{file_url} is not a valid youtube link. Please try again.")
        download_file(file_format=file_format)
    except (IOError, OSError, PytubeError) as e:
        print(f"{file_url} couldn't be downloaded.\n{e}\n")


def get_resolution(vid):
    available_resolutions = list({stream.resolution for stream in vid.fmt_streams})

    if None in available_resolutions:
        available_resolutions.remove(None)

    available_resolutions.sort(key=lambda x: int(x.split("p")[0]))
    resolution = input(f"Choose one of {', '.join(available_resolutions)} ")
    while resolution not in available_resolutions:
        resolution = input(f"Choose one of {', '.join(available_resolutions)} ")
    return resolution


def handle_incorrect_selection():
    input("\n\n\tError: Incorrect selection.")
    return main()


def clear_terminal():
    return os.system('cls' if os.name == 'nt' else 'clear')


if __name__ == '__main__':
    main()
