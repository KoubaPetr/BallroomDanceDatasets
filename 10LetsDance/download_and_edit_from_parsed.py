from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import moviepy.editor
# import pytube
import imageio_ffmpeg
import os
import cv2
import youtube_dl

genres = ['chachacha','slowfox','jive','samba','tango','waltz','pasodoble','quickstep','rumba']

for genre in genres:
    f = open('dataset_text_files_parsed/'+genre+'_links.txt','r')
    lines = f.readlines()
    for idx_line,l in enumerate(lines):
        if idx_line == 0:
            continue
        id,start_time,num_frames = l.split()
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

            cap = cv2.VideoCapture(WHOLE_VIDEO_PATH)
            # width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
            # height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
            frame_rate = cap.get(cv2.CAP_PROP_FPS)
            end_time = int(start_time) + int(num_frames)/float(frame_rate)

            ffmpeg_extract_subclip(WHOLE_VIDEO_PATH, float(start_time), float(end_time), targetname=CUT_VIDEO_PATH)
            print("Short clip extracted")
            # clip = moviepy.editor.VideoFileClip(CUT_VIDEO_PATH)
            # clip.audio.write_audiofile(CUT_AUDIO_PATH)
            # print("Audio written")
            del cap
            os.remove(WHOLE_VIDEO_PATH) # comment out the editing and disable this removal if we want the whole videos
            print("Whole video removed")
            print('============================================================')
            ### below just producing new representation of the dataset
            file = open('dataset_textfiles/' + genre + '_links.txt', 'a') ### Appending here. To regenerate the list of links with start and end times of segments, prepare corresponding empty text files
            file.write(id + ' ' + str(start_time) + ' ' + str(end_time) + '\n')
            file.close()

        except:
            file = open('dataset_text_files/broken_links.txt','a')
            file.write(genre + ' ' + str(idx_line) + ' ' + id +'\n')
            file.close()
            print('BROKEN LINK')



