import sublime
import sublime_plugin
import subprocess
import os
import os.path
import re
import pipes

# PerlTidy for Sublime Text 2
#   rbo@cpan.org
#
# TODO:
#   * Implementing isEnabled

class PerlTidyCommand(sublime_plugin.TextCommand):

    _perltidy_rc_paths = None
    _perltidy_default_rc_paths = ['.perltidyrc', 'perltidyrc']
    _perltidy_cmd = None
    _perltidy_default_cmd = '/usr/bin/perltidy'
    _perltidy_options = None
    _perltidy_default_options = ['-sbl', '-bbt=1', '-pt=2', '-nbbc', '-l=100', '-ole=unix', '-w', '-se']

    def run(self, edit):
        cmd = self.get_perltidy_cmd()
        if cmd is None:
            sublime.error_message(
                'PerlTidy error: Cannot find perltidy in PATH. Please setup your environment ' +
                'variable PATH, so it contains perltidy, or specify perltidy location in user ' +
                'setting "perltidy_cmd".')
            return

        selection = 0
        for r in self.view.sel():
            if not r.empty():
                selection += 1
                self.tidy_region(edit, r)

        if selection == 0:
            cursor = self.view.sel()[0]
            if self.tidy_region(edit, sublime.Region(0L, self.view.size())):
                if cursor.empty():
                    self.view.sel().add(cursor)
                    self.view.sel().subtract(self.view.sel()[1])
                    self.view.show_at_center(self.view.sel()[0].begin())

    def get_perltidy_cmd(self):
        # if not already done, load perltidy command from settings, or
        # fallback to default cmd defined above
        if self._perltidy_cmd is None:
            cmd = self.view.settings().get('perltidy_cmd')
            if cmd is None:
                cmd = self._perltidy_default_cmd
            if type(cmd) is not list:
                cmd = [cmd]

            # first element of self._perltidy_cmd must be a file, if not
            # assume that the command is invalid and try to find perltidy
            # within path
            if not os.path.isfile(cmd[0]):
                cmd = None
                for path in os.environ["PATH"].split(os.pathsep):
                    path_cmd = os.path.join(path, 'perltidy')

                    #print "PerlTidy: Checking for perltidy in " + path_cmd
                    if os.path.isfile(path_cmd):
                        cmd = [path_cmd]
                        break

            if cmd is not None:
                self._perltidy_cmd = cmd

        return self._perltidy_cmd

    def get_perltidy_options(self):
        if self._perltidy_options is None:
            self._perltidy_options = self.view.settings().get('perltidy_options')
            if self._perltidy_options is None:
                self._perltidy_options = self._perltidy_default_options

        return self._perltidy_options

    # return paths for perltidy configuration files; load them either from
    # setting "perltidy_rc_paths", or fallback to self._perltidy_default_rc_paths,
    # if none specified by user
    def get_perltidy_rc_paths(self):
        if self._perltidy_rc_paths is None:
            self._perltidy_rc_paths = self.view.settings().get('perltidy_rc_paths')
            if self._perltidy_rc_paths is None:
                self._perltidy_rc_paths = self._perltidy_default_rc_paths

        return self._perltidy_rc_paths

    # tidy given region; returns True on success or False on perltidy runtime
    # error.
    def tidy_region(self, edit, region):

        # build command
        cmd = []
        cmd.extend(self.get_perltidy_cmd())
        cmd.extend(self.get_perltidy_options())

        # try to find a tidyrc file, break on first tidyrc file found
        try:
            for folder in self.view.window().folders():
                for tidyrc_path in self.get_perltidy_rc_paths():
                    tidyrc_full_path = tidyrc_path if os.path.isabs(tidyrc_path) else os.path.join(folder, tidyrc_path)

                    # does this tidyrc file exist?
                    if os.path.isfile(tidyrc_full_path):

                        # on Win32, replace backslashes with forward slashed in
                        # perltidy.rc filepath, otherwise perltidy is unable to find
                        # the tidyrc file
                        if os.name.lower() == 'nt':
                            tidyrc_full_path = re.sub(r'\\', '/', tidyrc_full_path)

                        cmd.append('-pro={0}'.format(pipes.quote(tidyrc_full_path)))
                        raise StopIteration()

        except StopIteration:
            pass

        p = subprocess.Popen(
            cmd,
            bufsize = -1,
            shell   = True,
            stdout  = subprocess.PIPE,
            stderr  = subprocess.PIPE,
            stdin   = subprocess.PIPE)

        #print 'PerlTidy: running command: ' + ' '.join(cmd)

        output, error = p.communicate(self.view.substr(region))

        if not error:
            self.view.replace(edit, region, output)
            return True
        else:
            results = self.view.window().new_file()
            results.set_scratch(True)
            results.set_name('PerlTidy error output')
            edit = results.begin_edit()
            results.insert(edit, 0, error)
            results.end_edit(edit)
            return False
