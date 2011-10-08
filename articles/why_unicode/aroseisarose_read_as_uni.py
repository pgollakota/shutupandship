#!/usr/bin/env python
#
# Author: Praveen Gollakota <http://shutupandship.com>
# Date: 2011-10-08
#end_pyfile_header
import codecs

def read_utf8_file_as_uni():
    with codecs.open('aroseisarose.txt', 'rb', 'UTF-8') as f:
        return f.read()

if __name__ == '__main__':
    rose_uni = read_utf8_file_as_uni()
    print "len(rose_uni): %d" %len(rose_uni)
    print "rose_uni: %r" %rose_uni
    print "rose_uni[2]: %r" %rose_uni[2]
