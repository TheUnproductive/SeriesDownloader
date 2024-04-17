import os, re

from selenium import webdriver
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.support.wait import WebDriverWait

class loaders:
    def __init__(self, name: str, ending: str, loader: str, link: str = "0", file: str = "0", season: int = 1, episode: int = 1, verbose: str = "", proxy: str = "") -> None:
        self.name = name
        self.season = season
        self.episode = episode
        self.ending = ending
        self.verbose = verbose
        if link != "0": self.link = link
        if file != "0": self.file = file
        self.loader = loader
        self.proxy = proxy
    
    def set_episode(self, episode: int):
        self.episode = episode

    def set_link(self, link: str):
        self.link = link

    def set_proxy(self, proxy: str):
        self.proxy = proxy

    def set_season(self, season: int):
        self.season = season

    def generate_season_string(self) -> str:
        return f"0{str(self.season)}" if self.season < 10 else str(self.season)

    def generate_episode_string(self) -> str:
        return f"0{str(self.episode)}" if self.episode < 10 else str(self.episode)

    def file_download(self):
        with open(self.file, "r") as links_in:
            print("\x1b[0;30;43m" + "It is advised to only load one season at a time\x1b[0m")
    
            if not os.path.isdir(self.name):
                season_str = self.generate_season_string()
                os.mkdir(self.name)
                os.mkdir(f"{self.name}/Season {season_str}")
                print("\x1b[6;30;42m" + "Created folder %s/Season %s \x1b[0m" % (self.name, season_str))
    
            for link in links_in:
                if "/--/" not in link:
                    self.link_download()
            links_in.close()
    
    def downloader(self):
            os.system(f'.\{self.loader} {self.proxy} -o download/master{self.ending} {self.verbose} -R infinite "{self.link}"')
            season_str = self.generate_season_string()
            episode_str = self.generate_episode_string()
            episode_name = f"{self.name} s{season_str}e{episode_str}{self.ending}"
            os.rename(f"download/master{self.ending}", f"{self.name}/Season {season_str}/{episode_name}")
            print("\x1b[6;30;42m" + "Success! Downloaded Episode '%s'\x1b[0m" % (episode_name))

class voe(loaders):
    def link_download(self):
        try:
            cmd = f"curl -o data.txt {self.link}"

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

            for item in m3u8_info:
                if "m3u8" in item:
                    self.link = re.search("(?P<url>https?://[^\s]+)", item)["url"]
                    print(self.link)
                    print("Loading...")
                    loaders.downloader(self = self)
                    print("Loaded!")
        except:
            print("\x1b[0;30;41m" + "Error fetching m3u8 info\x1b[0m")
            if data_file:
                data_file.close()
                os.remove("data.txt")

    def downloader(self):
        loaders.downloader(self)

class southpark(loaders):
    def link_download(self):
        try:
            cmd = f"{self.loader} {self.link}"
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

            cmd = f"ffmpeg -f concat -safe 0 -i in.txt -c copy master{self.ending}"

            os.system(cmd)

            season_str = self.generate_season_string()
            episode_str = self.generate_episode_string()
            episode_name = f"{self.name} s{season_str}e{episode_str}{self.ending}"
            os.rename(f"master{self.ending}", f"{self.name}/Season {season_str}/{episode_name}")
            os.system("rm *.mp4")
        except:
            print("\x1b[0;30;41m" + "Error fetching m3u8 info\x1b[0m")

class sto():
    def __init__(self, link: str, start:int = 1) -> None:

        self.name = re.search("https://s\.to/serie/stream/(?P<name>[\w-]+)", link)["name"]

        if "staffel" in link:
            self.season = re.search("https://s\.to/serie/stream/[\w-]+(/staffel-(?P<season>\d)){0,}", link)["season"]
        else:
            self.season = 1

        if os.path.exists("cache-sto.txt"):
            link_list = open("cache-sto.txt", "r").read().split("\n")
            if "" in link_list:
                link_list.remove("")

        else:

            link_list = []

            binary = FirefoxBinary(r"D:\Tor Browser\Browser\firefox.exe")
            profile = FirefoxProfile(r"D:\Tor Browser\Browser\TorBrowser\Data\Browser\profile.default")

            driver = webdriver.Firefox(profile, binary)

            wait = WebDriverWait(driver, 20)

            driver.get(link)

            if driver.current_url != link:
                print(link)
                print("Redirected to: %s" % driver.current_url)
                element = WebDriverWait(driver, 1000).until(lambda x: driver.current_url == link)
        
            for episode in driver.find_elements(by="tag name", value="a"):
                try:
                    if "episode-" in episode.get_attribute("href"):
                        print(episode.get_attribute("href"))
                        if episode.get_attribute("href") not in link_list:
                            link_list.append(episode.get_attribute("href"))

                except:
                    pass

            driver.quit()

        print(link_list)

        cache = open("cache-sto.txt", "w")
        for item in link_list:
            cache.write(item + "\n")

        for i in range(start-1, len(link_list)):
            self.get_stream_url(link_list[i])

        cache.close()

        os.remove("cache-sto.txt")


    def get_stream_url(self, link: str) -> str:
        binary = FirefoxBinary(r"D:\Tor Browser\Browser\firefox.exe")
        profile = FirefoxProfile(r"D:\Tor Browser\Browser\TorBrowser\Data\Browser\profile.default")

        driver = webdriver.Firefox(profile, binary)
        driver.get(link)

        if driver.current_url != link:
            print("Redirected to: %s" % driver.current_url)
            element = WebDriverWait(driver, 100).until(lambda x: driver.current_url == link)
            driver.get(link)

        for video in driver.find_elements(by="class name", value="watchEpisode"):
            driver.get(video.get_attribute("href"))
            break

        open("{}-{}.txt".format(self.name, self.season), "a").write("/voe/" + driver.current_url + "\n")

        driver.quit()