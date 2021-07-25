import os
import time
import re

lets_dance_genres = os.listdir('rgb/')
print(lets_dance_genres)

our_genres = ['chachacha','slowfox','jive','samba','tango','waltz','pasodoble','quickstep','rumba']
start_time = time.time()
jpg_names_dict = {}

def parse_list_of_names(jpg_names : list):
    genre_parsed = []
    for name in jpg_names:
        parsed = [name[:11], *list(filter(None,re.split('(_|\.)',name[11:])))]
        genre_parsed.append(parsed)
    return genre_parsed

for g in our_genres:
    jpg_names = os.listdir('rgb/'+g+'/')
    print('Genre {} listed in {} seconds'.format(g,time.time()-start_time))
    jpg_names_dict[g] = jpg_names


print('====================================================================================')
parsed_data = {}
for g in our_genres:
    listVar = parse_list_of_names(jpg_names_dict[g])
    start_times = [int(l[2][:-2])*60+int(l[2][-2:]) for l in listVar] #names encode the time in form MSS or MMSS where M are minutes, S seconds => convert to seconds
    frame_nums = [int(l[4]) for l in listVar]
    yt_ids = [l[0] for l in listVar]
    genre_dict = {}
    for id,start_time,f_no in zip(yt_ids,start_times,frame_nums):
        if id not in genre_dict.keys():
            genre_dict[id] = {start_time: [f_no]}
        elif start_time not in genre_dict[id].keys():
            genre_dict[id][start_time] = [f_no]
        else:
            genre_dict[id][start_time].append(f_no)
    parsed_data[g] = genre_dict

for g in our_genres:
    file = open('dataset_text_files_parsed/'+g+'_links.txt','w+')
    genre_at_hand_data = parsed_data[g]
    for id in genre_at_hand_data.keys():
        for start_time in genre_at_hand_data[id]:
            number_of_frames = max(genre_at_hand_data[id][start_time])
            file.write(id + ' ' + str(start_time) + ' ' + str(number_of_frames) + '\n')
    file.close()