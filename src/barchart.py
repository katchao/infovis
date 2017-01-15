#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""barchart

a toy bar chart in text mode.
"""


# imports ###################################################################

from collections import defaultdict
from os import path


# data ######################################################################

DATA_PATH = path.join(path.abspath(path.dirname(__file__)), '..', 'data')

POINTS = { # maps ranks to points in order to compute the BBC ranking
	str(i+1): 10-i
	for i in range(10)
}
POINTS[''] = 0

BAR = u' ▁▂▃▄▅▆▇█'

top = []
movies = open(path.join(DATA_PATH, 'movies.csv'))
next(movies) # skip csv header
for line in movies:
	imdbid, title, director, year, *ranks = line.strip('\n').split('; ')
	score = sum(POINTS[rank] for rank in ranks)
	top.append((score, title, imdbid, ranks))
top.sort(reverse=True)

for score, title, imdbid, ranks in top:
	if score < 20:
		break
	distribution = defaultdict(int)
	for rank in ranks:
		if rank:
			distribution[int(rank)] += 1
	distribution = list(distribution[i+1] for i in range(10))
	top    = list(max(0, d-len(BAR)) for d in distribution)
	bottom = list(min(d, len(BAR)-1) for d in distribution)
	if any(t!=0 for t in top):
		print(*(BAR[t] for t in top), sep='')
	print(*(BAR[b] for b in bottom), sep='', end=' ')
	print(title)
