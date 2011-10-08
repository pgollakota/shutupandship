#!/usr/bin/env python
#
# Author: Praveen Gollakota <http://shutupandship.com>
# Date: 2011-10-08
#end_pyfile_header
def save_utf8_file():
    with open('aroseisarose.txt', 'wb') as f:
        f.write(u'A \u73ab is a rose'.encode('utf_8'))
        
if __name__ == '__main__':
    save_utf8_file()
