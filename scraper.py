from tmdbv3api import TMDb, TV, Movie, Season

class scraper:
    def __init__(self, name):
        self.tmdb = TMDb()
        self.tmdb.api_key = "aead5a8921ae3e4a555aa2a78c4fa4f5"

        self.tv = TV()

        self.search_name = name

    def search(self):
        self.search = self.tv.search(self.search_name)
        self.season_list = []
        for result in self.search:
            if result.name == self.search_name:
                print(result)
                id = result.id
                season = Season()
                for i in range(99):
                    try:
                        episodes = len(season.details(id, i).episodes)
                        self.season_list.append({"season":i, "episodes":episodes})
                        #print(self.season_list)
                    except:
                        if i == 0:
                            self.season_list.append({"season":0, "episodes":0})
                            pass
                        else:
                            break
                break
        if self.season_list == []:
            self.season_list.append({"season":0, "episodes":99})   
            self.season_list.append({"season":1, "episodes":99})             
        return self.season_list

#scraper("American Crime Story")