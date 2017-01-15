#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""vote2csv

Parse the votes scrapped from the BBC web site, and output 2 csv files:
- critics.csv with the details (name, media and country) of the critics
- movies.csv   with the details of the movies (imdbid, title, director, year, ranks for each critic)
"""


# imports ###################################################################

from os import path
from collections import defaultdict
import omdbapi


# data ######################################################################

DATA_PATH = path.join(path.abspath(path.dirname(__file__)), '..', 'data')

votes = {
#	critic: preference
#	critic is a tuple (name, media, country)
#   preference is an ordered list of films [(rank, title, director, year), ...]
}


# parsing ###################################################################

def parse_film(line):
	"""parse a film from the votes.txt file
	
	>>> parse_film("1. Mulholland Drive (David Lynch, 2001)")
	('1', 'Mulholland Drive', 'David Lynch', '2001')
	"""
	rank,     line = line.split('. ', 1)
	title,    line = line.rsplit(' (', 1)
	director, line = line.rsplit(', ', 1)
	year,     line = line.rsplit(')', 1)
	return rank, title, director, year


def parse_critic(line):
	"""parse a critic
	
	>>> parse_critic("Simon Abrams – Freelance film critic (US)")
	('Simon Abrams', 'Freelance film critic', 'US')
	"""
	name,    line = line.split(' – ', 1)
	media,   line = line.rsplit(' (', 1)
	country, line = line.rsplit(')', 1)
	return name, media, country


# processing votes ##########################################################

for line in open(path.join(DATA_PATH, 'votes.txt')):
	line = line.strip()
	if line == '':
		continue
	if line[0] not in '123456789':
		critic = parse_critic(line)
		preference = []
		votes[critic] = preference
	else:
		film = parse_film(line)
		preference.append(film)

# critics
critics = list(votes)
critics.sort()

output = open(path.join(DATA_PATH, 'critics.csv'), 'w')
output.write('#critic_id; name; media; country\n')
for i, (name, media, country) in enumerate(critics):
	output.write('c%03i; %s; %s; %s\n' % (i+1, name, media, country))
output.close()

# movies
movies = defaultdict(lambda :['']*len(critics))
for i, critic in enumerate(critics):
	vote = votes[critic]
	for rank, title, director, year in vote:
		movie = movies[title, director, year]
		movie[i] = rank

output = open(path.join(DATA_PATH, 'movies.csv'), 'w')
output.write('#imdbid; title; director; year')
for i in range(len(critics)):
	output.write('; c%03i' % (i+1))
output.write('\n')
for title, director, year in sorted(movies):
	imdbid = omdbapi.imdbid(title, year)
	output.write('%s; %s; %s; %s; %s\n' % (imdbid, title, director, year, '; '.join(movies[title, director, year])))
output.close()
