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
parser.add_argument("-scrape", action=argparse.BooleanOptionalAction, dest="scrape", default=False)
args = parser.parse_args()

file1 = args.file
name = args.name
season = args.season
episode = args.episode
ending = "." + args.filetype
if args.boolean: verbose = " --verbose"
else: verbose = ""
driver = args.loader

def downloader(file, name, season, episode, ending, verbose, driver):
    links_in = open(file, "r")
    print("\x1b[0;30;43m" + "It is advised to only load one season at a time\x1b[0m")

    if args.scrape: 
        metadata = scraper.scraper(name)
        episode_overview = metadata.search()
        print(episode_overview)
        season_num = episode_overview[season]

    if not os.path.isdir(name):
        os.mkdir(name)
    if season < 10: season_str = "0" + str(season)
    else: season_str = str(season)
    if not os.path.isdir("%s/Season %s" % (name, season_str)):
        os.mkdir("%s/Season %s" %(name, season_str))
        print("\x1b[6;30;42m" + "Created folder %s/Season %s \x1b[0m" % (name, season_str))

    voe = loaders.voe(name, ending, driver, season, verbose)
    southpark = loaders.southpark(name, ending, driver, verbose=verbose)

    for link in links_in:
        if "/--/" in link: pass
        else:
            if "/voe/" in link:
                link = link.replace("/voe/", "")
                print(episode)
                voe.set_link(link)
                voe.set_season(season)
                voe.set_episode(episode)
                voe.link_download()
                episode = episode + 1
            elif "www.southpark" in link:
                southpark.set_link(link)
                southpark.set_season(season)
                southpark.set_episode(episode)
                southpark.link_download()
                if args.scrape:
                    if episode == season_num["episodes"]:
                            episode = 1
                            season = season + 1
                            os.mkdir("%s/Season %s" %(name, season_str))
                            season_num = episode_overview[season]
                else:
                    episode = episode + 1
            else:
                try:
                    cmd = "%s %s"%(driver, link)
                    if args.scrape:
                        if episode == season_num["episodes"]:
                                episode = 1
                                season = season + 1
                                os.mkdir("%s/Season %s" %(name, season_str))
                                season_num = episode_overview[season]
                    else:
                        episode = episode + 1
                    if season < 10: season_str = "0" + str(season)
                    else: season_str = str(season)
                    if episode < 10: episode_str = "0" + str(episode)
                    else: episode_str = str(episode)
                    if driver == "yt-dlp": os.rename("download/master" + ending, "download/master" + ending)
                    episode_name = name + " s" + season_str + "e" + episode_str + ending
                    os.rename("download/master" + ending, name + "/Season " + season_str + "/" + episode_name)
                    print("\x1b[6;30;42m" + "Success Downloaded Episode %s \x1b[0m" % (episode_name))
                    if episode == season_num["episodes"]:
                        episode = 1
                        season = season + 1
                        os.mkdir("%s/Season %s" %(name, season_str))
                        season_num = episode_overview[season]
                    else:
                        episode = episode + 1
                except:
                    print("\x1b[0;30;41m" + "Error fetching m3u8 info\x1b[0m")
                    if args.scrape:
                        if episode == season_num["episodes"]:
                                episode = 1
                                season = season + 1
                                os.mkdir("%s/Season %s" %(name, season_str))
                                season_num = episode_overview[season]
                    else:
                        episode = episode + 1
                        pass

    links_in.close()

print("\x1b[1;32;40m" + "File Type: " + ending + '\x1b[0m')
print("\x1b[1;32;40m" + "Loader: " + driver + '\x1b[0m')
downloader(file1, name, season, episode, ending, verbose, driver)
