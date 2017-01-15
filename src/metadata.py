#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""metadata

Gathers a table of movie's metadata using the OMDb API.
"""


# imports ###################################################################

from os import path

import omdbapi


# data ######################################################################

DATA_PATH = path.join(path.abspath(path.dirname(__file__)), '..', 'data')
OMDB_KEYS = [
	'Director',
	'Poster',
	'Country',
	'Genre',
	'Rated',
	'Type',
	'Title',
	'Language',
	'Plot',
	'Awards',
	'Runtime',
	'Year',
	'Metascore',
	'Released',
	'Writer',
	'Actors',
	'imdbID',
	'imdbRating',
	'imdbVotes',
]

metadata = open(path.join(DATA_PATH, 'metadata.csv'), 'w')
print('#title', *OMDB_KEYS, sep='; ', file=metadata)

movies = open(path.join(DATA_PATH, 'movies.csv'))
next(movies) # skip csv header
for line in movies:
	imdbid, title, director, year, *_ = line.strip('\n').split('; ')
	infos = omdbapi.infos(imdbid)
	if not infos:
		infos = {k: '' for k in OMDB_KEYS}
	print(title, *(infos[k].replace(';', ',') for k in OMDB_KEYS), sep='; ', file=metadata)

