import os, argparse

parser = argparse.ArgumentParser()
parser.add_argument("-in", action="store", dest="file", type=str, default="test.txt")
parser.add_argument("-n", action="store", dest="name", type=str, required=True)
parser.add_argument("-s", action="store", dest="season", type=int, required=True)
parser.add_argument("-e", action="store", dest="episode", type=int, required=True)
args = parser.parse_args()

file1 = args.file
name = args.name
season = args.season
episode = args.episode

links_in = open(file1, "r")
print("It is advised to only load one season at a time")

if not os.path.isdir(name):
    if season < 10:
        season_str = "0" + str(season)
    else:
        season_str = str(season)
    os.mkdir(name)
    os.mkdir(name + "/Season " + season_str)

for link in links_in:
    try:
        os.system("youtube-dl -o download/master.mkv " + link)
        if season < 10:
            season_str = "0" + str(season)
        else:
            season_str = str(season)
        if episode < 10:
            episode_str = "0" + str(episode)
        else:
            episode_str = str(episode)
        os.rename("download/master.mkv", name + "/Season " + season_str + "/" + name + " s" + season_str + "e" + episode_str + ".mkv")
        episode = episode + 1
    except:
        print("Error fetching m3u8 info")
        pass

links_in.close()
