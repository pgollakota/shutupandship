#!/usr/bin/env python
#
# Author: Praveen Gollakota <http://shutupandship.com>
# Date: 2011-10-08
#end_pyfile_header
def read_utf8_file():
    with open('aroseisarose.txt', 'rb') as f:
        return f.read()

if __name__ == '__main__':
    rose = read_utf8_file()
    rose_uni = unicode(read_utf8_file(), 'utf8')
    print "len(rose): %d, len(rose_uni): %d" % (len(rose), len(rose_uni))
    print "rose: %r, rose_uni: %r" %(rose, rose_uni)
    print "rose[2]: %r, rose_uni[2]: %r" %(rose[2], rose_uni[2])
