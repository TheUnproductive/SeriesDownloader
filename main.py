import os, argparse
import libs.loaders as loaders
import libs.scraper as scraper

parser = argparse.ArgumentParser()
parser.add_argument("-n", action="store", dest="name", type=str, required=True)
parser.add_argument("-in", action="store", dest="file", type=str, default="txt/videos.txt")
parser.add_argument("-s", action="store", dest="season", type=int, default=1)
parser.add_argument("-e", action="store", dest="episode", type=int, default=1)
parser.add_argument("-t", action="store", dest="filetype", type=str, default="mkv")
parser.add_argument("-v", action=argparse.BooleanOptionalAction, dest="boolean", default=False)
parser.add_argument("-d", action="store", dest="loader", type=str, default="yt-dlp")
parser.add_argument("--proxy", action="store", dest="proxy", type=str, default="")
parser.add_argument("-scrape", action=argparse.BooleanOptionalAction, dest="scrape", default=False)
args = parser.parse_args()

file: str = args.file
name: str = args.name
season: int = args.season
episode: int = args.episode
ending: str = f".{args.filetype}"
verbose: str = " --verbose" if args.boolean else " "
driver: str = args.loader
proxy: str = " " if args.proxy == "" else f"--proxy {args.proxy}"

def generate_season_string(season: int) -> str:
        return f"0{str(season)}" if season < 10 else str(season)

def _extracted_from_downloader_1_(arg0, proxy: str, season: int, link: str) -> None:
    arg0.set_link(link)
    arg0.set_proxy(proxy)
    arg0.set_season(season)

def _link_behaviour(link: str, episode: int, season: int, season_str: str, episode_overview, season_num, voe: loaders.voe, southpark: loaders.southpark, name: str, ending: str, driver: str, verbose: str = "", proxy: str = "") -> int:
    if "/--/" not in link:
        if "/voe/" in link:
            link = link.replace("/voe/", "")
            print(episode)
            _extracted_from_downloader_1_(voe, proxy, season, link)
            voe.set_episode(episode)
            voe.link_download()
            return episode + 1
        elif "www.southpark" in link:
            southpark.set_episode(episode)
            _extracted_from_downloader_1_(southpark, proxy, season, link)
            southpark.link_download()
            if episode == season_num["episodes"]:
                    episode = 1
                    season = season + 1
                    os.mkdir(f"{name}/Season {season_str}")
                    season_num = episode_overview[season]
            else:
                episode = episode + 1

        elif "s.to" in link:
            loaders.sto(link, episode)
            return
        else:
            try:
                loader = loaders.loaders(name, ending, driver, link, season, episode, verbose)
                loader.set_episode(episode)
                _extracted_from_downloader_1_(loader, proxy, season, link)
                loader.downloader()
                print("World")
                episode = episode + 1
            except:
                print("\x1b[0;30;41m" + "Error fetching m3u8 info\x1b[0m")
                if args.scrape:
                    if episode == season_num["episodes"]:
                            episode = 1
                            season = season + 1
                            os.mkdir(f"{name}/Season {season_str}")
                            season_num = episode_overview[season]
                else:
                    episode = episode + 1
    return episode
    
def downloader(file: str, name: str, season: int, episode: int, ending: str, verbose: str, driver: str, proxy: str) -> None:
    print(episode)
    with open(file, "r") as links_in:
        print("\x1b[0;30;43m" + "It is advised to only load one season at a time\x1b[0m")

        if args.scrape: 
            metadata = scraper.scraper(name)
            episode_overview = metadata.search()
            print(episode_overview)
            season_num = episode_overview[season]
        else:
            episode_overview = {}
            season_num = args.season

        if not os.path.isdir(name):
            os.mkdir(name)

        season_str = generate_season_string(season)

        if not os.path.isdir(f"{name}/Season {season_str}"):
            os.mkdir(f"{name}/Season {season_str}")
            print("\x1b[6;30;42m" + "Created folder %s/Season %s \x1b[0m" % (name, season_str))

        voe = loaders.voe(name, ending, driver, season, verbose)
        southpark = loaders.southpark(name, ending, driver, season=season, verbose=verbose)

        for link in links_in:
            print(episode)
            episode_buf = _link_behaviour(link, episode, season, season_str, episode_overview, season_num, voe, southpark, name, ending, driver)
            episode = episode_buf

        links_in.close()

print("\x1b[1;32;40m" + "File Type: " + ending + '\x1b[0m')
print("\x1b[1;32;40m" + "Loader: " + driver + '\x1b[0m')

print(episode)

downloader(file, name, season, episode, ending, verbose, driver, proxy)
