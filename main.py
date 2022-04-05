import os, argparse

parser = argparse.ArgumentParser()
parser.add_argument("-in", action="store", dest="file", type=str, default="videos.txt")
parser.add_argument("-n", action="store", dest="name", type=str, required=True)
parser.add_argument("-s", action="store", dest="season", type=int, required=True)
parser.add_argument("-e", action="store", dest="episode", type=int, default=1)
parser.add_argument("-t", action="store", dest="filetype", type=str, default="mkv")
parser.add_argument("-v", action=argparse.BooleanOptionalAction, dest="boolean", default=False)
args = parser.parse_args()

file1 = args.file
name = args.name
season = args.season
episode = args.episode
ending = "." + args.filetype
if args.boolean: verbose = " --verbose"
else: verbose = ""

links_in = open(file1, "r")
print("It is advised to only load one season at a time")

if not os.path.isdir(name):
    if season < 10: season_str = "0" + str(season)
    else: season_str = str(season)
    os.mkdir(name)
    os.mkdir(name + "/Season " + season_str)

for link in links_in:
    if "/--/" in link: pass
    else:
        if "voe.sx" in link:
            os.system('python3 voe.py -n "%s" -s %s -e %s -l %s' % (name, season, episode, link))
            episode = episode + 1
        else:
            try:
                os.system("youtube-dl -o download/master" + ending + verbose + " " + link)
                if season < 10: season_str = "0" + str(season)
                else: season_str = str(season)
                if episode < 10: episode_str = "0" + str(episode)
                else: episode_str = str(episode)
                os.rename("download/master" + ending, name + "/Season " + season_str + "/" + name + " s" + season_str + "e" + episode_str + ending)
                episode = episode + 1
            except:
                print("Error fetching m3u8 info")
                episode = episode + 1
                pass

links_in.close()