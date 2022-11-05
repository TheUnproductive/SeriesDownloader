import os

class voe:
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
            cmd = "curl -o data.txt " + self.link
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
                    os.system("%s -o download/master%s %s %s" % (self.loader, self.ending, self.verbose, item))
                    if self.season < 10:
                        season_str = "0" + str(self.season)
                    else:
                        season_str = str(self.season)
                    if self.episode < 10:
                        episode_str = "0" + str(self.episode)
                    else:
                        episode_str = str(episode)
                    episode_name = self.name + " s" + season_str + "e" + episode_str + self.ending
                    os.rename("download/master" + ending, name + "/Season " + season_str + "/" + episode_name)
                    print("\x1b[6;30;42m" + "Success Downloaded Episode %s \x1b[0m" % (episode_name))
                    self.episode = self.episode + 1
        except:
            print("\x1b[0;30;41m" + "Error fetching m3u8 info\x1b[0m")
            if data_file:
                data_file.close()
                os.remove("data.txt")
            pass

    def file_download(self):
        links_in = open(self.file, "r")
        print("\x1b[0;30;43m" + "It is advised to only load one season at a time\x1b[0m")

        if not os.path.isdir(self.name):
            if self.season < 10:
                season_str = "0" + str(self.season)
            else:
                season_str = str(self.season)
            os.mkdir(self.name)
            os.mkdir("%s/Season %s" % (self.name, season_str))
            print("\x1b[6;30;42m" + "Created folder %s/Season %s \x1b[0m" % (self.name, season_str))

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
                            os.system("%s -o download/master%s %s %s" % (self.loader, self.ending, self.verbose, item))
                            if self.season < 10:
                                season_str = "0" + str(self.season)
                            else:
                                season_str = str(self.season)
                            if self.episode < 10:
                                episode_str = "0" + str(self.episode)
                            else:
                                episode_str = str(self.episode)
                            os.rename("download/master" + self.ending, self.name + "/Season " + season_str + "/" + self.name + " s" + season_str + "e" + episode_str + self.ending)
                            self.episode = self.episode + 1
                except:
                    print("\x1b[0;30;41m" + "Error fetching m3u8 info\x1b[0m")
                    if data_file:
                        data_file.close()
                        os.remove("data.txt")
                    pass

        links_in.close()