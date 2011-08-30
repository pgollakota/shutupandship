#!/usr/bin/env python
#
# Author: Praveen Gollakota <http://shutupandship.com>
# Date: 2011-08-29
#end_pyfile_header

class Deck(object):
    def __init__(self):
	self.cards = []
	for s in ['S', 'D', 'C', 'H']:
	    for r in range(1, 14):
		self.cards.append(Card(r, s))
    
    def __iter__(self):
	return iter(self.cards)
