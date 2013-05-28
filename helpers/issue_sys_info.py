#!/usr/bin/env python

from __future__ import print_function, unicode_literals
import platform, sublime, datetime

print('-' * 78)
print('Date/time: {0}'.format(datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S +0000')))
print('Sublime Text version: {0}'.format(sublime.version()))
print('Platform: {0}'.format(sublime.platform()))
print('CPU architecture: {0}'.format(sublime.arch()))
print('OS info: {0}'.format(repr(platform.platform())))
print('-' * 78)
