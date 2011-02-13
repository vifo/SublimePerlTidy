import sublime
import sublime_plugin
import subprocess
import os.path

#
# PerlTidy for Sublime Text 2
#   rbo@cpan.org
#
# Added key binding:
#	Sublime Text 2 -> Preferences -> User Key Bindings
#		Add line: { "keys": ["ctrl+t"], "command":"perl_tidy"}
# 
# TODO: 
#	* Implementing isEnabled
#	* Configurable perltidy command
#   * Read perltidyrc from project root, possible?
#     or read perldity config from st2 config
#

class PerlTidyCommand(sublime_plugin.TextCommand):

	perltidy_cmd = '/Users/rbo/Perl/perls/current/bin/perltidy'

	def run(self, edit):
		if not os.path.isfile(self.perltidy_cmd):
			sublime.error_message("Perltidy Error: Command not found:" + self.perltidy_cmd);
			return

		selection=0;
		for r in self.view.sel():
			if not r.empty():
				selection += 1
				self.tidy_region(edit,r)

		if selection == 0:
			self.tidy_region(edit,sublime.Region(0L, self.view.size()))


	def tidy_region(self,edit, region):
		cmd = [
			self.perltidy_cmd,
			"-sbdl","-bbt=1","-pt=2", "-nbbc", "-l=100","-ole=unix",
			"-w",
			"-se"
		]

		p = subprocess.Popen(
			cmd,
			shell   = True,
			bufsize = -1,
			stdout  = subprocess.PIPE,
			stderr  = subprocess.PIPE,
			stdin   = subprocess.PIPE)

		output, error = p.communicate(self.view.substr(region))
		self.view.replace(edit,region, output)

		if error:
			results = self.view.window().newFile()
			results.setScratch(True)
			results.setName("PerlTidy error output")
			results.insert(0, error)
