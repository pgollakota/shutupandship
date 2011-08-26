#!/usr/bin/env python
#
# Copyright 2011 Praveen Gollakota
#end_pyfile_header

def generate_power_func(n):
    print "id(n): %X" % id(n)
    def nth_power(x):
        return x**n
    print "id(nth_power): %X" % id(nth_power)
    return nth_power
