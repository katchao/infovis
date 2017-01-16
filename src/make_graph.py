#!/usr/bin/env python3

# imports ###################################################################
import json
import csv
from os import path

DATA_PATH = path.join(path.abspath(path.dirname(__file__)), '..', 'data')
MAIN_PATH = path.join(path.abspath(path.dirname(__file__)), '..')

POINTS = { # maps ranks to points in order to compute the BBC ranking
	str(i+1): 10-i
	for i in range(10)
}
POINTS[''] = 0

json_array = {}
nodes = []
links = []

rankings = []

critic_to_movie = {}

movies = open(path.join(DATA_PATH, 'movies.csv'))
next(movies) # skip csv header
for line in movies:
	imdbid, title, director, year, *ranks = line.strip('\n').split('; ')
	score = sum(POINTS[rank] for rank in ranks)
	movie = {}
	movie["id"] = title
	movie["group"] = int(year)
	movie["radius"] = score
	nodes.append(movie)
	critic_to_movie[title] = ranks

#print(critic_to_movie)

crits = {}
critics = open(path.join(DATA_PATH, 'critics.csv'))
next(critics) # skip csv header
for crit_num,line in enumerate(critics):
	cid, name, media, country = line.strip('\n').split('; ')
	crit = {}
	crit["id"] = name
	crit["group"] = 1
	crit["radius"] = 20
	nodes.append(crit)
	crits[crit_num] = name
	#crit.append((cid, name, country))

for movie in critic_to_movie.items():
	for i,critic_rank in enumerate(movie[1]):
		if critic_rank:
			#print(i,critic_rank)
			link = {}
			link["source"] = crits[i]
			link["target"] = movie[0]
			link["value"] = int(critic_rank)
			#print(link)
			links.append(link)

json_array["nodes"] = nodes
json_array["links"] = links
#print(json_array)

with open(path.join(DATA_PATH, 'graph.json'), 'w') as graph: 
	json.dump(json_array, graph, sort_keys=True, indent=4, ensure_ascii=False)

