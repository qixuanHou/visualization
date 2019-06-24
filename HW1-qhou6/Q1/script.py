import http.client
import json
import time
import sys
import collections

# get API key

def getAPIKey():
	if (len(sys.argv) == 2):
		return sys.argv[1]
	else:
		return

def getMovies(api_key):
	conn = http.client.HTTPSConnection("api.themoviedb.org")
	payload = "{}"
	f = open("movie_ID_name.csv", "w")
	count = 0
	page_num = 1
	failure = 1
	movieIDs = []
	while (count < 350):
		url = "/3/discover/movie?with_genres=18&primary_release_date.gte=2004&page=%d&include_video=false&include_adult=false&sort_by=popularity.desc&api_key=%s"%(page_num, api_key)
		conn.request("GET", url, payload)
		res = conn.getresponse()
		data = res.read()
		try:
			movies = json.loads(data)["results"]	
			for movie in movies:
				if (count == 350):
					return movieIDs
				movieIDs.append(movie["id"])
				f.write("%s,%s\n"%(movie["id"], movie["title"]))
				count = count + 1
			page_num = page_num + 1
		except:
			if (json.loads(data)["status_code"] == 25):
				time.sleep(3)
				print("sleeping for few seconds")

def getSimilarMovies(movieIds, api_key):
	conn = http.client.HTTPSConnection("api.themoviedb.org")
	payload = "{}"
	f = open("movie_ID_sim_movie_ID.csv", "w")
	pairs = []
	for ID in movieIds:
		url = "/3/movie/%d/similar?page=1&language=en-US&api_key=%s"%(ID, api_key)
		conn.request("GET", url, payload)
		res = conn.getresponse()
		data = res.read()
		try:
			movies = json.loads(data)["results"]
			if (len(movies) > 5):
				movies = movies[:5]
			for movie in movies:
				if ([movie["id"], ID] not in pairs):
					f.write("%s,%s\n"%(movie["id"], ID))
					pairs.append([movie["id"], ID])
					pairs.append([ID, movie["id"]])
		except:
			if (json.loads(data)["status_code"] == 25):
				time.sleep(3)
				print("sleeping for few seconds")
			

api_key = getAPIKey()
movieIds = getMovies(api_key)
getSimilarMovies(movieIds, api_key)



