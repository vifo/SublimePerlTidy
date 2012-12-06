# -*- coding: utf-8 -*-

import sys


def platform():
    if sys.platform.startswith('win'):
        return "windows"

    return "linux"
