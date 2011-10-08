#!/usr/bin/env python
#
# Author: Praveen Gollakota <http://shutupandship.com>
# Date: 2011-10-08
#end_pyfile_headerrose_uni = u'\u73ab'
encodings = ['big5', 'big5hkscs', 'cp950', 'gb2312', 'gbk',
            'gb18030', 'hz', 'iso2022_jp_2', 'utf_16',
            'utf_16_be', 'utf_16_le', 'utf_8', 'utf_8_sig']
print "Rose (code point U+73AB) in various encodings"
print "*"*45
for e in encodings:
    rose_encoded = rose_uni.encode(e)
    print '%12s:' %e,
    for c in rose_encoded:
        print '%02X' %ord(c),
    print '\n'
