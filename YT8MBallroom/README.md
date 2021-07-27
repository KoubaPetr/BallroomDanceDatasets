# YT8M Ballroom
Directory containing the structure of the 'YT8M Ballroom' dataset - structure similar to 'Tutorials Dataset' - see corresponding folder for details.

Script segment_downloader.py downloads the dataset into cut_videos/ folder. The folder dataset_textfiles/ contains the files with Youtube IDs and times of relevant segments in those videos - this is based on the selection of 3000 segments with minimal entropy of softmax scores of the audio classification.

The textfiles Ballroom_Dance_IDs.txt and Latin_Dance_IDs.txt contain the video IDs of the corresponding classes in Youtube-8M dataset. The file union_ordering.txt containes the union of these two classes.

File softmax_scores.pickle contains the softmax scores of the audio classifications of all non-overlapping 5.2s segments of all the available videos. Contained is a dictionary - keys in this dictionary provide the list of all the video IDs out of union_ordering.txt which we were able to download.

The folder final_selection_links/ contains the Youtube IDs which made it into our final video (after performing the cutoff at max 251 videos per class).
