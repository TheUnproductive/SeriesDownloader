from tmdbv3api import TMDb, TV, Movie, Season

class scraper:
    def __init__(self, name) -> None:
        self.tmdb = TMDb()
        self.tmdb.api_key = open("key.txt", "r").read()

        self.tv = TV()

        self.search_name = name

    def search(self) -> list:
        self.search = self.tv.search(self.search_name)
        self.season_list = []
        for result in self.search:
            if result.name == self.search_name:
                print(result)
                idx = result.id
                season = Season()
                for i in range(99):
                    try:
                        episodes = len(season.details(idx, i).episodes)
                        self.season_list.append({"season":i, "episodes":episodes})
                        #print(self.season_list)
                    except:
                        if i == 0:
                            self.season_list.append({"season":0, "episodes":0})
                        else:
                            break
                break
        if not self.season_list:
            self.season_list.append({"season":0, "episodes":99})   
            self.season_list.append({"season":1, "episodes":99})             
        return self.season_list