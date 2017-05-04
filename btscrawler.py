import sqlite3
import re
import urllib.request
import sys
import html
import codecs

boyTotals = {
    "Rap Monster": 0,
    "Suga": 0,
    "J-Hope": 0,
    "V": 0,
    "Jimin": 0,
    "Jungkook": 0,
    "Jin": 0
}
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

btsDir = 'https://colorcodedlyrics.com/2014/01/bts-lyrics-index'

siteHtml = html.unescape(urllib.request.urlopen(btsDir).read().decode('utf-8'))

rows = re.findall('<tbody>(.*?)</tbody>', siteHtml, re.DOTALL)
rows = rows[0]

releases = re.findall('<td>(.*?)</td>', rows, re.DOTALL)

releasesSorted = []

for release in releases:
    title = re.findall('\[#\d+\](.*?)<', release, re.DOTALL)
    tracks = re.findall('href="(.*?)">(.*?)<', release, re.DOTALL)

    titleAndTracks = [title, tracks]
    releasesSorted.append(titleAndTracks)

for album in releasesSorted:
    albumTitle = album[0]
    outfile.write(albumTitle[0] + '\n')
    tracklist = album[1]
    for song in tracklist:
        outfile.write('\t' + song[1] + '\n')
        songDir = song[0]
        songHtml = html.unescape(urllib.request.urlopen(songDir).read().decode('utf-8'))
        romanization = re.findall('<tbody>.<tr>.*?</tr>.<tr>.<td>(.*?)</td>', songHtml, re.DOTALL)[0]
        theBoys = {
            "Rap Monster": ['#ea9947', 0],
            "Suga": ['#46bd41', 0],
            "J-Hope": ["#dd54a4", 0],
            "V": ["#b7c185", 0],
            "Jimin": ["#a28be3", 0],
            "Jungkook": ["#c03f44", 0],
            "Jin": ["#3544b5", 0]
        }
        for boy in theBoys:
            color = theBoys[boy][0]
            getMemberLines(theBoys, color, boy, romanization)
