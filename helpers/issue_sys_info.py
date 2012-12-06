#!/usr/bin/env python

import platform; import sublime; import datetime; print '-' * 78; print "Date/time: " + datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S +0000'); print "ST2 version: " + sublime.version(); print "ST2 platform: " + sublime.platform(); print "CPU architecture: " + sublime.arch(); print "OS info: " + repr(platform.platform()); print '-' * 78
