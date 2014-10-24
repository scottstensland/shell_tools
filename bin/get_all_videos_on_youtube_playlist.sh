
#	download all videos in youtube playlist URL
#
#    usage (this script is called gvp)  
#
#    gvp  https://www.youtube.com/playlist?list=PL6299F3195349CCDA
#



given_playlist_url=$1

echo given_playlist_url $given_playlist_url


curr_date=`date '+%Y%m%d_%H%M%S'`

video_tag_outputfile=/tmp/video_tag_outputfile_${curr_date}
index_outputfile=/tmp/video_index_file_${curr_date}


wget $given_playlist_url -O $index_outputfile


cat $index_outputfile |grep watch | grep list| cut -d/ -f2 | cut -d'&' -f1 | grep watch | cut -d= -f2 | egrep -v '(channel)'  >  $video_tag_outputfile


cat $video_tag_outputfile

for curr_video_tab in `cat $video_tag_outputfile`; do

	echo curr_video_tab $curr_video_tab

	gvv $curr_video_tab

done




