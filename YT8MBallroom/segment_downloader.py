from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import moviepy.editor
#import pytube
import youtube_dl
import imageio_ffmpeg
import os
import time
import random
import cv2
import subprocess
from urllib.error import HTTPError

genres = [
    'chachacha', 'jive', 'pasodoble', 'quickstep', 'rumba',
    'samba', 'slowfox', 'waltz', 'tango', 'viennesewaltz',
]

for genre in genres:
    f = open('dataset_text_files/'+genre+'_links.txt','r')
    lines = f.readlines()
    for idx_line,l in enumerate(lines):
        id,start_time,stop_time = l.split()
        DOWNLOAD_PATH = 'whole_videos/' + genre + '/'
        WHOLE_VIDEO_PATH = DOWNLOAD_PATH + id + '.mp4'
        VIDEO_URL = 'https://www.youtube.com/watch?v='+id #'https://youtu.be/' + id
        CUT_VIDEO_PATH = 'cut_videos/'+genre+'/'+id+'.mp4'
        CUT_AUDIO_PATH = 'cut_audio/'+genre+'/'+id+'.wav'
        try:
            keepTrying = True
            try_num = 0
            while keepTrying:
                time.sleep(random.randrange(0,2))
                try:
                    ydl_opts = {
                        'outtmpl': WHOLE_VIDEO_PATH,
                        'format': 'mp4',
                        'continuedl': False
                    }
                    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                        ydl.cache.remove()
                        ydl.download([VIDEO_URL])
                    # youtube = pytube.YouTube(VIDEO_URL)
                    # video = youtube.streams.filter(file_extension='mp4').first()
                    keepTrying = False
                    print(try_num)
                except : #HTTPError:
                    if try_num > 5:
                        keepTrying = False
                    try_num += 1

            #video.download(DOWNLOAD_PATH, filename=id+'.mp4') #probably necessary to add the extension in the new version of pytube
            print("Video {} was downloaded to: {}".format(genre + '_' + str(idx_line), DOWNLOAD_PATH))

            ffmpeg_extract_subclip(WHOLE_VIDEO_PATH, float(start_time), float(stop_time), targetname=CUT_VIDEO_PATH)
            print("Short clip extracted")
            # This would store the audio clips separately
            # clip = moviepy.editor.VideoFileClip(CUT_VIDEO_PATH)
            # clip.audio.write_audiofile(CUT_AUDIO_PATH)
            # print("Audio written")
            os.remove(WHOLE_VIDEO_PATH) # comment out the editing and disable this removal if we want the whole videos
            print("Whole video removed")
            print('============================================================')


        except: #HTTPError:
            file = open('dataset_text_files/broken_links.txt','a')
            file.write(genre + ' ' + str(idx_line) + ' ' + id +'\n')
            file.close()
            print('BROKEN LINK')
