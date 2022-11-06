import os, re

class loaders:
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
                self.link_download()
        links_in.close()
    
    def loader(self):
            os.system('.\%s -o download/master%s %s "%s"' % (self.loader, self.ending, self.verbose, self.link))
            if int(self.season) < 10: season_str = "0" + str(self.season)
            else: season_str = str(self.season)
            if int(self.episode) < 10: episode_str = "0" + str(self.episode)
            else: episode_str = str(self.episode)
            if self.loader == "yt-dlp": os.rename("download/master" + self.ending, "download/master" + self.ending)
            episode_name = self.name + " s" + season_str + "e" + episode_str + self.ending
            os.rename("download/master" + self.ending, self.name + "/Season " + season_str + "/" + episode_name)
            print("\x1b[6;30;42m" + "Success Downloaded Episode %s \x1b[0m" % (episode_name))

class voe(loaders):
    def set_episode(self, episode):
        self.episode = episode
        #print(self.episode)

    def set_link(self, link):
        self.link = link
        #print(self.link)

    def set_season(self, season):
        self.season = season
        #print(self.season)

    def link_download(self):
        try:
            cmd = "curl -o data.txt " + self.link
            #print(cmd)
            os.system(cmd)
            data_file = open("data.txt", "r")
            for line in data_file:
                if "404 Page not Found" in line: 
                    os.remove("data.txt")
                    break
                if "m3u8" in line:
                    m3u8_info = line.split("'")
                    data_file.close()
                    os.remove("data.txt")
                    break
            #print(m3u8_info)
            for item in m3u8_info:
                if "m3u8" in item:
                    self.link = re.search("(?P<url>https?://[^\s]+)", item).group("url")
                    #print(self.link)
                    print("Loading...")
                    loaders.loader(self)
                    print("Loaded!")
        except:
            print("\x1b[0;30;41m" + "Error fetching m3u8 info\x1b[0m")
            if data_file:
                data_file.close()
                os.remove("data.txt")
            pass
    def loader(self):
        loaders.loader(self)

class southpark(loaders):
    def link_download(self):
        try:
            cmd = self.loader  + " " + self.link
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

            cmd = "ffmpeg -f concat -safe 0 -i 'in.txt' -c copy master" + self.ending

            os.system(cmd)

            if self.season < 10:
                season_str = "0" + str(self.season)
            else:
                season_str = str(self.season)
            if self.episode < 10:
                episode_str = "0" + str(self.episode)
            else:
                episode_str = str(self.episode)
            episode_name = self.name + " s" + season_str + "e" + episode_str + self.ending
            os.rename("master" + self.ending, self.name + "/Season " + season_str + "/" + episode_name)
            print("\x1b[6;30;42m" + "Success Downloaded Episode %s \x1b[0m" % (episode_name))
            os.system("rm *.mp4")
        except:
            print("\x1b[0;30;41m" + "Error fetching m3u8 info\x1b[0m")
            pass
