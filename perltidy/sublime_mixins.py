# -*- coding: utf-8 -*-

"""
Mixins for Sublime Text classes providing additional functionality.
"""

from __future__ import print_function, unicode_literals
import sublime
import types


def view_remove_trailing_newlines(self, edit, region=None, keep_last_newline=True):
    """
    Remove trailing newlines from buffer.
    """

    while self.size() >= 2:
        if self.substr(sublime.Region(self.size() - 2, self.size())) == "\n\n":
            self.erase(edit, sublime.Region(self.size() - 1, self.size()))
        else:
            break


def view_append(self, edit, contents):
    """
    Append contents to end of buffer.
    """

    self.insert(edit, self.size(), "\n".join(contents) if isinstance(contents, types.ListType) else contents)


def view_whole_buffer_region(self):
    """
    Return region representing whole buffer.
    """

    return sublime.Region(0, self.size())


def view_sel_non_empty(self):
    """
    Return list of sublime.Region objects contaning all non-empty selections.
    """

    selections = []
    for region in self.sel():
        if not region.empty():
            selections.append(region)

    return selections


def view_replace_contents(self, edit, region, contents, method='default'):
    """
    Replace view contents using specified method.
    """

    if method == 'default':
        self.replace(edit, region, contents)

    elif method == 'warm':
        lines_left = contents.split("\n")
        regions_left = self.split_by_newlines(region)

        while lines_left and regions_left:
            cur_region = regions_left.pop(0)
            new_line = lines_left.pop(0)
            old_line = self.substr(cur_region)

            if self.substr(cur_region) != new_line:
                self.replace(edit, cur_region, new_line)
                regions_left = self.split_by_newlines(sublime.Region(cur_region.begin(), self.size()))
                regions_left.pop(0)

        # Erase rest of regions
        if regions_left:
            self.erase(edit, sublime.Region(regions_left[0].begin(), self.size()))

        # Add rest of lines
        if lines_left:
            self.append(edit, lines_left)

        # Remove trailing newlines (keep one at end of buffer)
        self.remove_trailing_newlines(edit)

    else:
        raise ValueError('Argument "method" must be either "default" or "warm"')


def enhance_sublime_view_instance(view):
    """
    Mix additional methods into sublime.View instance.
    """

    if not hasattr(view, '__perltidy_enhanced'):
        view.append = types.MethodType(view_append, view)
        view.remove_trailing_newlines = types.MethodType(view_remove_trailing_newlines, view)
        view.replace_contents = types.MethodType(view_replace_contents, view)
        view.sel_non_empty = types.MethodType(view_sel_non_empty, view)
        view.whole_buffer_region = types.MethodType(view_whole_buffer_region, view)

    return view
