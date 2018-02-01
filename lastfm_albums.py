import os, sys
from lastfm import *

def songsList(songs_dir = os.getcwd()):
    songs = []
    for f in os.listdir(songs_dir):
        if os.path.splitext(f)[-1] in ['.mp3', '.MP3']:
            songs.append(f)
    return songs


def parseSongName(song_name):
    song_name = song_name[:-4]
    artist, title = song_name.split(' - ')
    return (artist, title)


def makeHardSongsList(f='songs.txt'):
    sl = songsList()
    slist = open(f, 'w', encoding='utf8')
    for song in sl:
        artist, title = parseSongName(song)
        print('%s\t%s'%(artist, title), file=slist)
    slist.close()


def main():
    fres = open('list.csv', 'w', encoding='utf8')
    failures = open('failed.txt', 'w', encoding='utf8')
    sccs, fail = 0, 0
    status = None
    
    makeHardSongsList('songs.txt')
    sl = open('songs.txt', 'r', encoding='utf8').read().split('\n')
    for song in sl:
        print(song)
        artist, title = song.split('\t')

        try:
            a_name = getAlbName(artist, title)
            sccs += 1
            status = 'SUCCESS'
        except Exception as e:
            # print('no album due to: %s'%e)
            fail += 1
            status = 'FAIL'
            a_name = 'not found'

        print('STATUS: %s\nalbum: %s'%(status, a_name))
        print('%s\t%s\t%s\t%s'%(status, artist, title, a_name), file=fres)

        print('')
    fres.close()


if __name__ == '__main__':
    main()
    


