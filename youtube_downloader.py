import pytube
import requests
from pytube import YouTube, Playlist
import ffmpeg
import shutil
import os
from os import startfile

# -- constants --
#   TODO: write the path of project temp folder
# TEMP_FOLDER_DIRECTORY = 'C:/Users/[username]/youtube_downloader/temp'
TEMP_FOLDER_DIRECTORY = 'C:/Users/reemn/ReeM-C/Coding/youtube_downloader/temp'
#   Messages
ERROR_CONNECTION_MESSAGE = 'Unable to download, there is no connection'
RESOLUTION_MESSAGE = 'resolution options: [4K] [2K] [FHD] [HD] [480] [360p] [240p] [144p]: '
ERROR_INVALID_URL = 'Invalid youtube video URL'
#   High Resolution Tags
TAG4K = 313
TAG1080 = 137
TAG1440 = 271

#   Global Variables
#   TODO: write the path where you want to save downloaded video
# download_path = 'C:/Users/[username]/Downloads'
download_path = 'C:/Users/reemn/Downloads/'
video_title = 'final'
user_choice = 'V'

#   Functions

def download_144_720p(resolution_choice, youtube_video):
    res_adapted = resolution_choice

    def downloading(resolution):
        print('Downloading video ...')
        global video_title
        youtube_video.streams.get_by_resolution(resolution).download()
        print('Done')
        opening_moving_video()
        youtube_video.register_on_complete_callback(finish())
        return

    while True:
        if res_adapted == 'HD' or res_adapted == 'hd':
            if youtube_video.streams.get_by_resolution('720p') != 'None':
                downloading('720p')
                return
            else:
                res_adapted = '480p'
        if res_adapted == '480' or res_adapted == '480p':
            try:
                downloading('480p')
                return
            except AttributeError:
                res_adapted = '360p'
        if res_adapted == '360' or res_adapted == '360p':
            try:
                downloading('360p')
                return
            except AttributeError:
                res_adapted = '240p'
        if res_adapted == '240' or res_adapted == '240p':
            try:
                downloading('240p')
                return
            except AttributeError:
                res_adapted = '144p'
        if res_adapted == '144' or res_adapted == '144p':
            try:
                downloading('144p')
                return
            except AttributeError:
                res_adapted = 'HD'
        else:
            downloading('360p')
            return


def download_1080_1440(tag, youtube_video, title):
    download_audio(youtube_video=youtube_video, title=title)
    youtube_video.streams.get_by_itag(tag).download()
    os.rename(title + '.mp4', 'downloaded_video.mp4')
    merging_audio_video_1080_4k()
    naming_video(title)
    opening_moving_video()
    finish()


def download_4k(tag, youtube_video):
    global video_title
    download_audio(youtube_video=youtube_video, title=video_title)
    youtube_video.streams.get_by_itag(tag).download()
    os.rename(video_title + '.webm', 'downloaded_video.mp4')
    merging_audio_video_1080_4k()
    naming_video(video_title)
    opening_moving_video()
    finish()


def download_audio(youtube_video, title):
    youtube_video.streams.get_by_itag(251).download()
    os.rename(title + '.webm', 'downloaded_audio.webm')
    print('Audio downloaded successfully')


def merging_audio_video_1080_4k():
    #   adding the input video and audio in ffempeg
    ffmpeg
    d_video = ffmpeg.input('downloaded_video.mp4')
    d_audio = ffmpeg.input('downloaded_audio.webm')

    final_video_path = 'C:/Users/reemn/ReeM-C/Coding/youtube_downloader/final.mp4'

    #   Download Video
    print('---------------------- [ Downloading video ... ] --------------------------')

    out = ffmpeg.output(d_video, d_audio, final_video_path, vcodec='copy', acodec='aac', strict='experimental')
    out.run()

    print('-------------------------------- [ Done ] --------------------------------')


def naming_video():
    global video_title
    os.rename('final.mp4', video_title + '.mp4')
    os.remove('Downloaded_Video.mp4')
    os.remove('Downloaded_Audio.webm')


def opening_moving_video():
    # in case there is a file with the same name inside the downloaded_video_path
    global video_title
    while True:
        try:
            shutil.move(video_title + '.mp4', download_path)
            break
        except shutil.Error:
            print('there is already a video file named (', video_title, ') inside (', download_path, ')')
            temp = video_title
            video_title = input('Please change the file name: ')
            if temp != video_title:
                os.rename(temp + '.mp4', video_title + '.mp4')
                print('--------------------------------------------------------------')
                continue

    if user_choice == 'v' or user_choice == 'V':
        startfile(download_path + "/" + video_title + '.mp4')


def finish():
    global video_title
    print('Video Downloaded Successfully :)')
    print('Find it inside:', '(' + download_path + ') named: (' + video_title + ')' + '.mp4')


def checking_connection_url(url, download_type):

    if download_type=='v' or download_type=='V':
        if 'www.youtube.com/watch?' in url:
            return True

    elif download_type=='p' or download_type=='P':
        if 'https://www.youtube.com/playlist?' in url:
            return True

    print(ERROR_CONNECTION_MESSAGE)
    return False


def video_downloader(downloaded_video, res_choice):
    global video_title
    try:
        video_title = downloaded_video.title.replace('\"', '').replace('/', '').replace('\\', '').replace(':',
                                                                                                        '').replace(
            '<', '').replace('>', '').replace('|', '').replace(',', '').replace('?', '').replace('#', '').replace('.', '').replace('\'', '')
    except:
        video_title = downloaded_video.title

    if res_choice == "4k" or res_choice == "4K":
        if downloaded_video.streams.get_by_resolution('2160p') == "None":
            download_4k(tag=TAG4K, youtube_video=downloaded_video)
        else:
            if downloaded_video.streams.get_by_resolution('1440p') == "None":
                download_1080_1440(tag=TAG1440, youtube_video=downloaded_video)
            else:
                if downloaded_video.streams.get_by_resolution('1080p') == "None":
                    download_1080_1440(tag=TAG1080, youtube_video=downloaded_video)
                else:
                    download_144_720p(resolution_choice=res_choice, youtube_video=downloaded_video)

    elif res_choice == "2k" or res_choice == "2K":
        if downloaded_video.streams.get_by_resolution('1440p') == "None":
            download_1080_1440(tag=TAG1440, youtube_video=downloaded_video)
        else:
            if downloaded_video.streams.get_by_resolution('1080p') == "None":
                download_1080_1440(tag=TAG1080, youtube_video=downloaded_video)
            else:
                download_144_720p(resolution_choice=res_choice, youtube_video=downloaded_video)

    elif res_choice == "fhd" or res_choice == "fHD":
        if downloaded_video.streams.get_by_resolution('1080p') == "None":
            download_1080_1440(tag=TAG1080, youtube_video=downloaded_video)
        else:
            download_144_720p(resolution_choice=res_choice, youtube_video=downloaded_video)

    else:
        download_144_720p(resolution_choice=res_choice, youtube_video=downloaded_video)


#   Starting point
while True:
    os.chdir(TEMP_FOLDER_DIRECTORY)
    user_choice = input('For Video Downloader type V, Playlist Downloader type P: ')

    if user_choice == "V" or user_choice == "v":

        # taking the url and resolution option from the user
        url = input("Please enter the video url: ")

        if not checking_connection_url(url, user_choice):
            print(ERROR_INVALID_URL)
            break
        try:
            downloaded_video = YouTube(url)
        except pytube.exceptions.RegexMatchError:
            print(ERROR_INVALID_URL)
            break

        res_choice = input(RESOLUTION_MESSAGE)

        video_downloader(downloaded_video=downloaded_video, res_choice=res_choice)


    elif user_choice == "P" or user_choice == "p":

        playlist_link = input("Please enter the playlist url: ")


        if not checking_connection_url(playlist_link, user_choice):
            print(ERROR_INVALID_URL)
            break

        try:
            playlist = Playlist(playlist_link)
        except pytube.exceptions.RegexMatchError:
            print(ERROR_INVALID_URL)
            break

        res_choice = input(RESOLUTION_MESSAGE)

        #------- Validating the playlist status
        try:
            download_path += playlist.title
            os.mkdir(download_path)
            os.chdir(TEMP_FOLDER_DIRECTORY)
        except:
            print('Couldn\'t download the playlist, please make sure that the playlist is (public) and not private')
            pass
        # -------

        for video in playlist.videos:
            video_downloader(downloaded_video=video, res_choice=res_choice)

    elif user_choice == "Q" or user_choice == "q":
        break

    else:
        print("invalid input")
