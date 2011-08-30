#!/usr/bin/env python
#
# Author: Praveen Gollakota <http://shutupandship.com>
# Date: 2011-08-29
#end_pyfile_header

class MyList(list):
    def __iter__(self):
        return MyListIter(self)
    
class MyListIter(object):
    """ A sample implementation of a list iterator. NOTE: This is just a 
    demonstration of concept!!! YOU SHOULD NEVER IMPLEMENT SOMETHING LIKE THIS!
    Even if you have to (for any reason), there are many better ways to 
    implement this."""
	
    def __init__(self, lst):
        self.lst = lst
	self.i = -1

    def __iter__(self):
	return self
	
    def next(self):
	if self.i<len(self.lst)-1:
    	    self.i += 1	        
            return self.lst[self.i]
	else:
	    raise StopIteration
