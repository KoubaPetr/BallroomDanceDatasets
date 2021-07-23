Directory structure prepared for the download of the "Tutorials Dataset". This is a dataset of videos of 10 different ballroom dances corresponding to the International Style, i.e.: Cha-Cha,Rumba,Jive,Paso Doble, Samba, Waltz, Viennese Waltz, Quickstep, Slowfox and Tango.

Each class holds instances corresponding to segments of Youtube videos, where there is single dancepair clearly visible and performing the dance corresponding to the class label. The dataset was handpicked and annotated manually. Each class has total footage of at least 10 minutes, coming from at least 13 different videos, with no video contributing by more than 80 seconds and each dance performance not contributing by more than 60 seconds.

The script called download_and_edit.py downloads the videos, cuts out the relevant segments and merges them into single instance (if they come from the same video) and stores them in the folder cut_videos (and given subfolder corresponding to the label). By commenting out a single line (with os.remove()) in the script, the original videos in their full length will also be stored.

The script download_and_edit.py depends on moviepy and pytube (to be replaced by youtube-dl, which is morereliable).

The collection of the relevant IDs of the Youtube videos can be found in the folder dataset_text_files. The text files with the IDs also hold the indication of relevant segments of the video, lines of these text files obey the following structure: 

YoutubeID segment1_start_sec segment1_end_sec segment2_start_sec segment2_end_sec ... 
