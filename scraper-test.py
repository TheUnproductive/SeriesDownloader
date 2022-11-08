import libs.scraper as scraper

def main():
    metadata = scraper.scraper("South Park")
    episode_overview = metadata.search()
    print(episode_overview)
    for i in range(len(episode_overview)):
        print(episode_overview[i])
        print(episode_overview[i]["episodes"])

def example_download():
    start_season = 1
    episode = 1
    end_season = 10
    metadata = scraper.scraper("South Park")
    episode_overview = metadata.search()
    for i in range(start_season, end_season + 1):
        for episode in range(0, episode_overview[i]["episodes"] + 1):
            if episode == episode_overview[i]["episodes"]:
                episode = 1
                print(episode)
            else:
                episode = episode + 1
                print(episode)


if __name__ == "__main__":
    example_download()
