from moviepy.editor import VideoFileClip, concatenate_videoclips
import pytube
import os

genres = ['chachacha','slowfox','jive','samba','tango','waltz','pasodoble','quickstep','rumba','viennesewaltz']

for genre in genres:
    f = open('dataset_text_files/'+genre+'_links.txt','r')
    lines = f.readlines()
    for idx_line,l in enumerate(lines):
        parsed_line = l.split()
        id = parsed_line[0]
        start_times = []
        stop_times = []
        for i in range(int((len(parsed_line)-1)/2)):
            start_times.append(int(parsed_line[2*i+1]))
            stop_times.append(int(parsed_line[2*i+2]))

        DOWNLOAD_PATH = 'whole_videos/' + genre + '/'
        WHOLE_VIDEO_PATH = DOWNLOAD_PATH + id + '.mp4'
        VIDEO_URL = 'https://youtu.be/' + id
        CUT_VIDEO_PATH = 'cut_videos/'+genre+'/'+id+'.mp4'
        try:
            youtube = pytube.YouTube(VIDEO_URL)
            video = youtube.streams.filter(file_extension='mp4').first()
            video.download(DOWNLOAD_PATH, filename=id)
            print("Video {} was downloaded to: {}".format(genre + '_' + str(idx_line), DOWNLOAD_PATH))

            video_clip = VideoFileClip(WHOLE_VIDEO_PATH)

            #obtain the relevant segments
            clips = []
            for start_time,end_time in zip(start_times,stop_times):
                clips.append(video_clip.subclip(start_time,end_time))
            if len(clips)>1:
                final_video = concatenate_videoclips(clips)
            elif len(clips) == 1:
                final_video = clips[0]
            else:
                print('NO CLIP!!!')
            final_video.write_videofile(CUT_VIDEO_PATH)

            ###Close video_clip
            video_clip.reader.close()
            del video_clip.reader
            if video_clip.audio != None:
                video_clip.audio.reader.close()
                del video_clip.audio
            del video_clip

            ###Close final_video
            final_video.close()
            del final_video


            print("Short clip extracted")
            os.remove(WHOLE_VIDEO_PATH) # comment out the editing and disable this removal if we want the whole videos
            print("Whole video removed")
            print('============================================================')

        except:
            file = open('dataset_text_files/broken_links.txt','a')
            file.write(genre + ' ' + str(idx_line) + ' ' + id +'\n')
            file.close()
            print('BROKEN LINK')



