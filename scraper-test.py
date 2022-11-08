import libs.scraper as scraper

def main():
    metadata = scraper.scraper("South Park")
    episode_overview = metadata.search()
    print(episode_overview)
    for i in range(len(episode_overview)):
        print(episode_overview[i])
        print(episode_overview[i]["episodes"])

if __name__ == "__main__":
    main()
