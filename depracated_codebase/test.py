from tmdbv3api import TMDb, TV, Movie, Season
import scraper as md

test = md.scraper("Halo").search
print(test)

#tmdb = TMDb()
#tmdb.api_key = "aead5a8921ae3e4a555aa2a78c4fa4f5"
#season = Season()
#print(season.details(64513, 0))