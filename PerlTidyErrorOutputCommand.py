# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals
import sublime
import sublime_plugin


class PerlTidyErrorOutputCommand(sublime_plugin.TextCommand):

    """Write error messages to PerlTidy error output buffer."""

    def run(self, edit, output=''):
        final_output = "PerlTidy: Errors reported by perltidy during last run\n"
        final_output += "=====================================================\n"
        final_output += output
        self.view.insert(edit, self.view.size(), final_output)
