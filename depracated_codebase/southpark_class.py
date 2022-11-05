import os

class southpark:
    def __init__(self, name, ending, loader, link="0", file="0", season=1, episode=1, verbose=""):
        self.name = name
        self.season = season
        self.episode = episode
        self.ending = ending
        self.verbose = verbose
        if link == "0": pass
        else: self.link = link
        if file == "0": pass
        else: self.file = file
        self.loader = loader

    def link_download(self):
        try:
            cmd = loader  + " " + link
            os.system(cmd)

            files = os.listdir("./")
            for file in files:
                if file.endswith(".mp4"):
                    if "S1" in file:
                        os.rename(file, "part1.mp4")
                    elif "S2" in file:
                        os.rename(file, "part2.mp4")
                    elif "S3" in file:
                        os.rename(file, "part3.mp4")
                    elif "S4" in file:
                        os.rename(file, "part4.mp4")

            cmd = "ffmpeg -f concat -safe 0 -i 'in.txt' -c copy master" + ending

            os.system(cmd)

            if season < 10:
                season_str = "0" + str(season)
            else:
                season_str = str(season)
            if episode < 10:
                episode_str = "0" + str(episode)
            else:
                episode_str = str(episode)
            episode_name = name + " s" + season_str + "e" + episode_str + ending
            os.rename("master" + ending, name + "/Season " + season_str + "/" + episode_name)
            print("\x1b[6;30;42m" + "Success Downloaded Episode %s \x1b[0m" % (episode_name))
            os.system("rm *.mp4")
            episode = episode + 1
        except:
            print("\x1b[0;30;41m" + "Error fetching m3u8 info\x1b[0m")
            pass

    def file_download(self):
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
                    cmd = loader  + " " + link
                    os.system(cmd)

                    files = os.listdir("./")
                    for file in files:
                        if file.endswith(".mp4"):
                            if "S1" in file:
                                os.rename(file, "part1.mp4")
                            elif "S2" in file:
                                os.rename(file, "part2.mp4")
                            elif "S3" in file:
                                os.rename(file, "part3.mp4")
                            elif "S4" in file:
                                os.rename(file, "part4.mp4")

                    cmd = "ffmpeg -f concat -safe 0 -i in.txt -c copy master" + ending

                    os.system(cmd)

                    if season < 10:
                        season_str = "0" + str(season)
                    else:
                        season_str = str(season)
                    if episode < 10:
                        episode_str = "0" + str(episode)
                    else:
                        episode_str = str(episode)
                    os.rename("master" + ending, name + "/Season " + season_str + "/" + name + " s" + season_str + "e" + episode_str + ending)
                    os.system("rm *.mp4")
                    episode = episode + 1
                except:
                    print("\x1b[0;30;41m" + "Error fetching m3u8 info\x1b[0m")
                    pass
        links_in.close()
