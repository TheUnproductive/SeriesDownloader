import os, argparse, re

parser = argparse.ArgumentParser()
parser.add_argument("-in", action="store", dest="file", type=str)
parser.add_argument("-n", action="store", dest="name", type=str, required=True)
parser.add_argument("-s", action="store", dest="season", type=int, required=True)
parser.add_argument("-e", action="store", dest="episode", type=int, required=True)
parser.add_argument("-t", action="store", dest="filetype", type=str, default="mkv")
parser.add_argument("-l", action="store", dest="link", type=str)
parser.add_argument("-v", action=argparse.BooleanOptionalAction, dest="boolean", default=False)
parser.add_argument("-d", action="store", dest="loader", type=str, default="youtube-dl")
args = parser.parse_args()

name = args.name
season = args.season
episode = args.episode
ending = "." + args.filetype
if args.boolean: verbose = " --verbose"
else: verbose = ""
loader = args.loader
link = args.link

print(link)

def link_download(name, season, episode, ending, verbose, link, loader):
    try:
        cmd = "curl -o data.txt " + link
        os.system(cmd)
        data_file = open("data.txt", "r")
        for line in data_file:
            if "m3u8" in line:
                m3u8_info = line.split("'")
                data_file.close()
                os.remove("data.txt")
                break
        print(m3u8_info)
        for item in m3u8_info:
            if "m3u8" in item:
                item = re.search("(?P<url>https?://[^\s]+)", item).group("url")
                print(item)
                os.system('%s -o download/master%s %s "%s"' % (loader, ending, verbose, item))
                if season < 10:
                    season_str = "0" + str(season)
                else:
                    season_str = str(season)
                if episode < 10:
                    episode_str = "0" + str(episode)
                else:
                    episode_str = str(episode)
                episode_name = name + " s" + season_str + "e" + episode_str + ending
                os.rename("download/master" + ending, name + "/Season " + season_str + "/" + episode_name)
                print("\x1b[6;30;42m" + "Success Downloaded Episode %s \x1b[0m" % (episode_name))
                episode = episode + 1
    except:
        print("\x1b[0;30;41m" + "Error fetching m3u8 info\x1b[0m")
        if data_file:
            data_file.close()
            os.remove("data.txt")
        pass

def file_download(name, season, episode, ending, verbose, file, loader):
    links_in = open(file, "r")
    print("\x1b[0;30;43m" + "It is advised to only load one season at a time\x1b[0m")

    if not os.path.isdir(name):
        if season < 10:
            season_str = "0" + str(season)
        else:
            season_str = str(season)
        os.mkdir(name)
        os.mkdir("%s/Season %s" % (name, season_str))
        print("\x1b[6;30;42m" + "Created folder %s/Season %s \x1b[0m" % (name, season_str))

    for link in links_in:
        if "/--/" in link: pass
        else:
            try:
                cmd = "curl -o data.txt " + link
                os.system(cmd)
                data_file = open("data.txt", "r")
                for line in data_file:
                    if "m3u8" in line:
                        m3u8_info = line.split('"')
                        data_file.close()
                        os.remove("data.txt")
                        break
                print(m3u8_info)
                for item in m3u8_info:
                    if "m3u8" in item:
                        os.system("%s -o download/master%s %s %s" % (loader, ending, verbose, item))
                        if season < 10:
                            season_str = "0" + str(season)
                        else:
                            season_str = str(season)
                        if episode < 10:
                            episode_str = "0" + str(episode)
                        else:
                            episode_str = str(episode)
                        os.rename("download/master" + ending, name + "/Season " + season_str + "/" + name + " s" + season_str + "e" + episode_str + ending)
                        episode = episode + 1
            except:
                print("\x1b[0;30;41m" + "Error fetching m3u8 info\x1b[0m")
                if data_file:
                    data_file.close()
                    #os.remove("data.txt")
                pass

    links_in.close()

if args.file:
    file1 = args.file
    file_download(name, season, episode, ending, verbose, file1, loader)
elif args.link:
    link = args.link
    link_download(name, season, episode, ending, verbose, link, loader)
else:
    print("Please provide either a file or a link to download from")
    exit()