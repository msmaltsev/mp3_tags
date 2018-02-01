import taglib
import os, sys
from time import sleep

def autoCap(line):
    l_w = line.split(' ')
    n_l = ' '.join([w[0].upper()+w[1:] for w in l_w if len(w) > 0])
    return n_l


def parseSongName(song_name):
    song_name = song_name[:-4]
    artist, title = song_name.split(' - ')
    artist, title = autoCap(artist), autoCap(title)
    return (artist, title)


def songsList(songs_dir = os.getcwd()):
    songs = []
    for f in os.listdir(songs_dir):
        if os.path.splitext(f)[-1] in ['.mp3', '.MP3']:
            songs.append(f)
    return songs


def processSong(s):
    try:
        song = taglib.File(s)
        song_tags = song.tags
        artist, title = parseSongName(s)
        song.tags['ARTIST'] = [artist]
        song.tags['TITLE'] = [title]
        song.save()
        return True
    except Exception as e:
        print(e)
        return False


def names():
    songs_list = songsList()
    sl_len = len(songs_list)
    pr_cnt = 0
    fl_cnt = 0
    failed = []
    for s in songs_list:
        sys.stdout.flush()
        sys.stdout.write('\rprocessed: %s, failed: %s, current song: %s'%(pr_cnt, fl_cnt, s))
        p = processSong(s)
        if p:
            pr_cnt += 1
        else:
            fl_cnt += 1
        # sleep(0.3333333)
    if len(failed) != 0:
        f = open('failures.txt', 'w', encoding='utf8')
        for i in failed:
            print(i, file=f)
        f.close()


def albums():
    songs_list = open('list.csv', 'r', encoding='utf8').read().split('\n')
    sl_len = len(songs_list)
    pr_cnt = 0
    fl_cnt = 0
    failed = []
    for line in songs_list:
        try:
            line = line.split('\t')
            status, song, album = line[0], '%s - %s.mp3'%(line[1], line[2]), line[3]
            sys.stdout.flush()
            sys.stdout.write('\rprocessed: %s, failed: %s, current song: %s'%(pr_cnt, fl_cnt, song))
            if status == 'SUCCESS':
                song = taglib.File(song)
                song.tags['ALBUM'] = [album]
                song.save()
                pr_cnt += 1
                
            
        except Exception as e:
            print(e)
            fl_cnt += 1

        if len(failed) != 0:
            f = open('failures.txt', 'w', encoding='utf8')
            for i in failed:
                print(i, file=f)
            f.close()



if __name__ == '__main__':
    albums()