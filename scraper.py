from tmdbv3api import TMDb, TV, Movie, Season

class scraper:
    def __init__(self, name):
        self.tmdb = TMDb()
        self.tmdb.api_key = "aead5a8921ae3e4a555aa2a78c4fa4f5"

        self.tv = TV()

        self.search_name = name

    def search(self):
        self.search = self.tv.search(self.search_name)

        for result in self.search:
            if result.name == self.search_name:
                print(result)
                id = result.id
                season = Season()
                self.season_list = []
                for i in range(99):
                    try:
                        episodes = len(season.details(id, i).episodes)
                        self.season_list.append([i, episodes])
                    except:
                        break
                break
        return self.season_list