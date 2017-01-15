#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""top100

A simple visualisation of the movies with more than 20 points (~ top 100).
Uses the OMDb API to get the posters, and generates a web page with the size of the poster linked to the socre.
"""


# imports ###################################################################

from os import path

import omdbapi


# data ######################################################################

DATA_PATH = path.join(path.abspath(path.dirname(__file__)), '..', 'data')

POINTS = { # maps ranks to points in order to compute the BBC ranking
	str(i+1): 10-i
	for i in range(10)
}
POINTS[''] = 0

top = []
movies = open(path.join(DATA_PATH, 'movies.csv'))
next(movies) # skip csv header
for line in movies:
	imdbid, title, director, year, *ranks = line.strip('\n').split('; ')
	score = sum(POINTS[rank] for rank in ranks)
	top.append((score, title, imdbid))

print('<html><body>')
for score, title, imdbid in top:
	if score < 20:
		continue
	infos = omdbapi.infos(imdbid)
	if not infos:
		continue
	src = infos['Poster']
	if src == 'N/A':
		continue
	print("<img alt='%s' src='%s' width='%s' />" % (title, src, score))
print('</body></html>')
