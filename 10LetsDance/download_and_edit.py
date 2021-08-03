from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import moviepy.editor
# import pytube
import imageio_ffmpeg
import os
import cv2
import subprocess
import youtube_dl

genres = ['chachacha','slowfox','jive','samba','tango','waltz','pasodoble','quickstep','rumba','viennesewaltz']

for genre in genres:
    f = open('dataset_text_files/'+genre+'_links.txt','r')
    lines = f.readlines()
    for idx_line,l in enumerate(lines):
        id, start_time, stop_time = l.split()
        DOWNLOAD_PATH = 'whole_videos/' + genre + '/'
        WHOLE_VIDEO_PATH = DOWNLOAD_PATH + id + '.mp4'
        VIDEO_URL = 'https://youtu.be/' + id
        CUT_VIDEO_PATH = 'cut_videos/'+genre+'/'+id+'.mp4'
        CUT_AUDIO_PATH = 'cut_audio/'+genre+'/'+id+'.wav'
        try:
            # youtube = pytube.YouTube(VIDEO_URL)
            # video = youtube.streams.filter(file_extension='mp4').first()
            # video.download(DOWNLOAD_PATH, filename=id)
            ydl_opts = {
                'outtmpl': WHOLE_VIDEO_PATH,
                'format': 'mp4',
                'continuedl': False
            }
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.cache.remove()
                ydl.download([VIDEO_URL])
            print("Video {} was downloaded to: {}".format(genre + '_' + str(idx_line), DOWNLOAD_PATH))

            end_time = int(stop_time)

            ffmpeg_extract_subclip(WHOLE_VIDEO_PATH, float(start_time), float(end_time), targetname=CUT_VIDEO_PATH)
            print("Short clip extracted")
            ### uncomment and perhaps create the directory to store audio files
            # clip = moviepy.editor.VideoFileClip(CUT_VIDEO_PATH)
            # clip.audio.write_audiofile(CUT_AUDIO_PATH)
            # print("Audio written")

            ### comment out the editing and disable this removal if we want the whole videos
            os.remove(WHOLE_VIDEO_PATH)
            print("Whole video removed")
            print('============================================================')

        except:
            file = open('dataset_text_files/broken_links.txt','a')
            file.write(genre + ' ' + str(idx_line) + ' ' + id +'\n')
            file.close()
            print('BROKEN LINK')



