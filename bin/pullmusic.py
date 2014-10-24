#!/usr/bin/env python 

#	download all media files from given URL which contains a directory listing of same
#
#	previous to executing this script, first google using following search criteria to discover an above mentioned URL :
#
#	   some-cool-song-album-video   "parent directory " "Index of" -wally -xxx -html -htm -php -shtml -opendivx -md5 -md5sums 
#
#	___ such as ___ :
#
#			justice genesis   "parent directory " "Index of" -wally -xxx -html -htm -php -shtml -opendivx -md5 -md5sums
#
#	... now troll through search results of above listing to discover a good URL mentioned at top line above
#
#	___ such as ___ :
#
#			http://web.mit.edu/ridonk/Music%20for%20Fall%202008/Popping/
#
#	... so now we have a good URL - let's get the songs - execute below script using :
#
#	pullmusic.py  http://web.mit.edu/ridonk/Music%20for%20Fall%202008/Popping/
#
#	which will first download the index file / parse it to discover each media link / do a wget to download each media file
#
#	enjoy - Scott Stensland



import glob
import subprocess

import sys


def cut_grep_function(given_music_suffix):
	print ("here is given_music_suffix ")
	print given_music_suffix

	length_given_music_suffix = len(given_music_suffix)

	count_num_matches_per_column = {}

	matched_elements_by_field_count = {}

	entire_index_file = file( "index.html", "r" )
	for curr_line in entire_index_file:
		all_delimited_fields = curr_line.split( '"' )
		print ("length of all_delimited_fields" + str(len(all_delimited_fields)))

		for curr_index in range(len(all_delimited_fields)):

			# if (str(len(all_delimited_fields[curr_index])) == (1 + length_given_music_suffix + all_delimited_fields[curr_index].find(given_music_suffix))):

			if (all_delimited_fields[curr_index].endswith(given_music_suffix)):

				print "YES seeing trailing suffix match"
				print (str(curr_index) + " here is element -->" + all_delimited_fields[curr_index] + \
					"<-- of length " + str(len(all_delimited_fields[curr_index])))

				if curr_index not in count_num_matches_per_column:
					count_num_matches_per_column[curr_index] = 1
					matched_elements_by_field_count[curr_index] = [all_delimited_fields[curr_index]]
				else:
					count_num_matches_per_column[curr_index] += 1
					matched_elements_by_field_count[curr_index].append(all_delimited_fields[curr_index])

	entire_index_file.close()
	print "here is count_num_matches_per_column"
	print count_num_matches_per_column

	print "here is matched_elements_by_field_count"
	print matched_elements_by_field_count

	bogus_index = -1

	index_with_most_matches = bogus_index
	count_max_matches = bogus_index

	for curr_index in count_num_matches_per_column:
		print "here is index entry from count_num_matches_per_column"
		print curr_index
		print "here is count for given index "
		print count_num_matches_per_column[curr_index]
		if count_num_matches_per_column[curr_index] > count_max_matches:
			count_max_matches = count_num_matches_per_column[curr_index]
			index_with_most_matches = curr_index

	if index_with_most_matches == bogus_index:
		return []
	else:
		print "finally ... index_with_most_matches is " + str(index_with_most_matches) + " with " + str(count_num_matches_per_column[index_with_most_matches]) + " matches"
		print matched_elements_by_field_count[index_with_most_matches]
		return (matched_elements_by_field_count[index_with_most_matches])


def show_it():

	print "here it is"
	print "and no more"


def main_function():

	print "another here"

	# for given_input in sys.stdin:
	# 	given_input = sys.stdin.readlines()

	chosen_url = sys.argv[1:][0]

	# chosen_url="http://78.142.45.23/dataup/MUSIC/Music-classical/Classics%2002/MOZART,%20Wolfgang%20Amadeus%20-%20Symphonies%20No.40%20&%20No.41/";
	# chosen_url="http://jesujej.serval.feralhosting.com/RTORRENT/Johann%20Sebastian%20Bach%20-%20Keyboard%20Concertos%201,%202,%20&%204%20%20(2001)%20%5bFLAC%5d/";
	# chosen_url=given_input

	print chosen_url

	set_music_suffixes = []
	set_music_suffixes.append("flac")
	set_music_suffixes.append("mp3")
	set_music_suffixes.append("ogg")

	print "about to show set_music_suffixes "
	print set_music_suffixes

	# subprocess.call(["ls", "-l"])
	# subprocess.call(["rm", "index*"])
	# subprocess.call(["wget", chosen_url])

	# all_index_files = glob.glob("index*")
	# subprocess.call(["rm", all_index_files])

	proc = subprocess.Popen('rm index*', shell=True,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE)

	# subprocess.call([proc])

	subprocess.call(["wget", chosen_url])

	list_suffix_matches_by_suffix = {}

	for curr_suffix in set_music_suffixes:

		curr_suffix_lc = curr_suffix.lower()
		curr_suffix_uc = curr_suffix.upper()
		list_suffix_matches_by_suffix[curr_suffix_lc] = cut_grep_function(curr_suffix_lc)
		list_suffix_matches_by_suffix[curr_suffix_uc] = cut_grep_function(curr_suffix_uc)

	print "\n\nhere is list_suffix_matches_by_suffix"
	print list_suffix_matches_by_suffix

	best_suffix = 'bogus'
	max_songs_best_suffix = 0

	for curr_suffix in list_suffix_matches_by_suffix:
		print "here is current suffix " + curr_suffix
		if (len(list_suffix_matches_by_suffix[curr_suffix]) > max_songs_best_suffix):
			max_songs_best_suffix = len(list_suffix_matches_by_suffix[curr_suffix])
			best_suffix = curr_suffix

	print "now we're burning gas ... here are the songs : " 
	for curr_song_mini_url in list_suffix_matches_by_suffix[best_suffix]:
		print curr_song_mini_url
		curr_url = chosen_url + "/" + curr_song_mini_url
		print ("\n\n... attempting URL " + curr_url)
		subprocess.call(["wget", "-c", curr_url])
		




# ------------ main() ------------ #

main_function()


