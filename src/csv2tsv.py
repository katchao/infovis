#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
for line in sys.stdin:
	words = line.split(';')
	line = '\t'.join(word.strip() for word in words)
	sys.stdout.write(line)
	sys.stdout.write('\n')

