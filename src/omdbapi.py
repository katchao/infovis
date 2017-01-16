#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
A omdb api client

Copyright (c) 2016, IIHM/LIG - Renaud Blanch <http://iihm.imag.fr/blanch/>
Licence: GPLv3 or higher <http://www.gnu.org/licenses/gpl.html>
"""


# imports ###################################################################

from urllib.request import urlopen
from urllib.parse import urlencode

import json


# twitter query ##############################################################

OMDBAPI_URL = "http://www.omdbapi.com/"

def get(query):
	search = urlopen("?".join([OMDBAPI_URL, query]))
	info = search.info()
	content_type = info['Content-type']
	mime_type, encoding = content_type.split(';')
	assert mime_type == "application/json"
	encoding = encoding.split('=')[-1].strip()
	text_response = search.read().decode(encoding)
	return json.loads(text_response)

def imdbid(title, year):
	query = {
		't': title.strip(),
		'y': str(year).strip(),
		'r': 'json',
	}
	response = get(urlencode(query))
	if response['Response'] != 'True':
		return None
	return response['imdbID']

def infos(imdbid):
	query = {
		'i': imdbid.strip(),
		'r': 'json',
	}
	response = get(urlencode(query))
	if response['Response'] != 'True':
		return None
	return response
