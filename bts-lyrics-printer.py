import re
import urllib.request
import sys
import html
import codecs

# boyTotals = {		#probably going to need to use defaultdict to change this to dynamically make a dict of member names
#	 "Rap Monster": 0,
#	 "Suga": 0,
#	 "J-Hope": 0,
#	 "V": 0,
#	 "Jimin": 0,
#	 "Jungkook": 0,
#	 "Jin": 0
# }
outfile = codecs.open(sys.argv[1], 'w', 'utf-8', 'ignore')

def getMemberLines(d, color, member, lyrics):
	 global boyTotals
	 global outfile
	 regexString = '<span style="color: ' + color + '">(.*?)</span>'
	 lines = re.findall(regexString, lyrics, re.DOTALL)
	 for line in lines:
		 line = line.replace('<br />', '').split()
		 for word in line:
			 d[member][1] += 1
	 outfile.write('\t\t%s: %s\n' % (member, d[member][1]))
	 boyTotals[member] += d[member][1]

btsDir = 'https://colorcodedlyrics.com/2014/01/bts-lyrics-index'	#change this to match group

siteHtml = html.unescape(urllib.request.urlopen(btsDir).read().decode('utf-8'))		#html.unescape: Convert all named and numeric character references (e.g. &gt; , &#62; , &x3e; ) in the string s to the corresponding unicode characters.

rows = re.findall('<tbody>(.*?)</tbody>', siteHtml, re.DOTALL)		#everything in first giant chunk (includes japanese albums)
rows = rows[0]

releases = re.findall('<td>(.*?)</td>', rows, re.DOTALL)		#each td is an album

releasesParsed = []

for release in releases:				#for each album
	title = re.findall('\[#\d+\](.*?)<', release, re.DOTALL)			#titles of albums in the form of one-item lists
	tracks = re.findall('href="(.*?)".*?>(.*?)<', release, re.DOTALL)		#list of tuples (accessed like a list) of titles and links to individual tracks

	titleAndTracks = [title, tracks]			#list containing string and another list
	releasesParsed.append(titleAndTracks)		#list wherein each item is a list containing two lists [[[album], [(link 1, track 1), (link 2, track 2)], [[album], [(link 1, track 1), (link 2, track 2)]]]

for album in releasesParsed:		#for each list containing string and other list within biggest container list
	albumTitle = album[0]
	outfile.write(albumTitle[0] + '\n')		#printing the album title - first item in probably one-item list, might be more items but we don't want those
	tracklist = album[1]					#sublist with track urls
	for song in tracklist:					#per track url
		outfile.write('\t' + song[1] + '\n')	#song title, second item in each tuple
		songDir = song[0]						#song link
		songHtml = html.unescape(urllib.request.urlopen(songDir).read().decode('utf-8'))	#open, decode, unescape characters
		romanization = re.findall('<tbody>.<tr>.*?</tr>.<tr>.<td>(.*?)</td>', songHtml, re.DOTALL)[0]	#maybe just change to 1 to get hangul
		#for korean:				<tbody>.<tr>.*?</tr>.<tr>.<td>.*?</td><td>(.*?)</td>
		#hangul = re.findall('<tbody>.<tr>.*?</tr>.<tr>.<td>.*?</td><td>(.*?)</td>', songHtml, re.DOTALL)[0]
		#hangul_text = hangul[0]
		romanization = romanization.replace('<br />', '')
		romanization = re.sub('<.*?>', '', romanization)
		romanization = romanization.split('\n')
		for line in romanization:
			print('New line: ' + line)
			line = line.strip()
			outfile.write('\t\t%s\n' % line)
		outfile.write('\n')


		# theBoys = {
		#	 "Rap Monster": ['#ea9947', 0],		  #manually find colors for members
		#	 "Suga": ['#46bd41', 0],				 #should be consistent for each member across songs
		#	 "J-Hope": ["#dd54a4", 0],
		#	 "V": ["#b7c185", 0],
		#	 "Jimin": ["#a28be3", 0],
		#	 "Jungkook": ["#c03f44", 0],
		#	 "Jin": ["#3544b5", 0]
		# }
		# for boy in theBoys:
		#	 color = theBoys[boy][0]
		#	 getMemberLines(theBoys, color, boy, romanization)	#for each member, find lyrics individually

# outfile.write('\n####################\n\nGLOBAL VALUES\n')
# for boy in boyTotals:
#	 outfile.write('\t%s:\t%s\t%.2f%%\n' % (boy, boyTotals[boy], float(boyTotals[boy]/sum(boyTotals.values()))*100))
