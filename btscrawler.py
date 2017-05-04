import sqlite3
import re
import urllib.request
import sys
import html
import codecs

btsDir = 'https://colorcodedlyrics.com/2014/01/bts-lyrics-index'
outfile = codecs.open(sys.argv[1], 'w', 'utf-8', 'ignore')

siteHtml = html.unescape(urllib.request.urlopen(btsDir).read().decode('utf-8'))
#outfile.write(siteHtml)

rows = re.findall('<tbody>(.*?)</tbody>', siteHtml, re.DOTALL)
rows = rows[0]

releases = re.findall('<td>(.*?)</td>', rows, re.DOTALL)

releasesSorted = []
boyTotals = {
    "rapmon": 0,
    "suga": 0,
    "hobie": 0,
    "v": 0,
    "jimin": 0,
    "jungkook": 0,
    "jin": 0
}
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
            "rapmon": 0,
            "suga": 0,
            "hobie": 0,
            "v": 0,
            "jimin": 0,
            "jungkook": 0,
            "jin": 0
        }
        rapmonLines = re.findall('<span style="color: #ea9947">(.*?)</span>', romanization, re.DOTALL)
        for line in rapmonLines:
            line = line.replace('<br />', '').split()
            for word in line:
                theBoys["rapmon"] += 1
        sugaLines = re.findall('<span style="color: #46bd41">(.*?)</span>', romanization, re.DOTALL)
        for line in sugaLines:
            line = line.replace('<br />', '').split()
            for word in line:
                theBoys["suga"] += 1
        hobieLines = re.findall('<span style="color: #dd54a4">(.*?)</span>', romanization, re.DOTALL)
        for line in hobieLines:
            line = line.replace('<br />', '').split()
            for word in line:
                theBoys["hobie"] += 1
        vLines = re.findall('<span style="color: #b7c185">(.*?)</span>', romanization, re.DOTALL)
        for line in vLines:
            line = line.replace('<br />', '').split()
            for word in line:
                theBoys["v"] += 1
        jiminLines = re.findall('<span style="color: #a28be3">(.*?)</span>', romanization, re.DOTALL)
        for line in jiminLines:
            line = line.replace('<br />', '').split()
            for word in line:
                theBoys["jimin"] += 1
        jungkookLines = re.findall('<span style="color: #c03f44">(.*?)</span>', romanization, re.DOTALL)
        for line in jungkookLines:
            line = line.replace('<br />', '').split()
            for word in line:
                theBoys["jungkook"] += 1
        jinLines = re.findall('<span style="color: #3544b5">(.*?)</span>', romanization, re.DOTALL)
        for line in jinLines:
            line = line.replace('<br />', '').split()
            for word in line:
                theBoys["jin"] += 1

        outfile.write('\t\tRap Monster: %s\n' % theBoys["rapmon"])
        boyTotals['rapmon'] += theBoys['rapmon']
        outfile.write('\t\tSuga: %s\n' % theBoys["suga"])
        boyTotals['suga'] += theBoys['suga']
        outfile.write('\t\tJ-Hope: %s\n' % theBoys["hobie"])
        boyTotals['hobie'] += theBoys['hobie']
        outfile.write('\t\tJimin: %s\n' % theBoys["jimin"])
        boyTotals['jimin'] += theBoys['jimin']
        outfile.write('\t\tV: %s\n' % theBoys["v"])
        boyTotals['v'] += theBoys['v']
        outfile.write('\t\tJungkook: %s\n' % theBoys["jungkook"])
        boyTotals['jungkook'] += theBoys['jungkook']
        outfile.write('\t\tJin: %s\n' % theBoys["jin"])
        boyTotals['jin'] += theBoys['jin']
