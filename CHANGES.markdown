# perltidy for Sublime Text 2/3

## Changes

### v0.4.2 2013-11-09 13:27:11 +0100

* Update Package Control repository.json schema to version 2.0.

### v0.4.1 2013-06-23 18:00:00 +0200

* Fixed bug with empty rows (CRLFs) being inserted into formatted source
  code under Windows. Fixes #17. (vifo)
* Support and tests for ActivePerl 64-bit added. (vifo)

### v0.4.0 2013-05-31 20:00:00 +0200

* Sublime Text 3 support added. Most of porting to Python 3 has been done
  using information from http://python3porting.com/noconv.html. (vifo)
* Default perltidy options changed. PerlTidy will now use the PBP set of
  perltidy options. (vifo)
* Default key binding for OS X changed from `Command+Shift+t` to
  `Control+Shift+t`, the former fires a terminal. (vifo)
* Options found in perltidyrc files will now override default/user options.
  The former processing of perltidy options was counter-intuitive. Old
  behavior can be restored by setting "perltidy_options_take_precedence" to
  "true" in user settings. (vifo)
* Error output from perltidy is now displayed via class
  PerlTidyErrorOutputCommand, ST3 restricts editing of view contents. (vifo)
* Fixed Python code used for bug reports and added helper script
  "helpers/create_issue_sys_info.pl" used to generate the required one-liner.
  (vifo)
* Documentation updated, Package Control messages updated. (vifo)
* Full changelog moved to CHANGES.markdown. (vifo)

### v0.3.0 2013-04-28 12:40:00 +0200

Repo/plugin renamed from rbo/st2-perltidy to vifo/SublimePerlTidy.

* Version number bumped to 0.3.0. (vifo)
* Documentation updated according to renaming done. (vifo)

### v0.2.1 2013-04-13 14:38:00 +0200

Version number bumped. Latest package was missing in package repository.

### v0.2.0 2012-12-20 09:45:00 +0100

Cygwin support added. Tests added. Settings now reloaded on each PerlTidy run.

* User setting "perltidy_options_take_precedence" added. If set to "true",
  which is the default, options from user setting "perltidy_options" will take
  precedence over options found in perltidyrc files. (vifo)
* Running Perl/perltidy under Cygwin is now supported. PerlTidy will set required
  environment variables, if running on Windows, so we won't get any warnings
  from Cygwin/Perl (i.e. LANG="C" and CYGWIN+="nodosfilewarning"). (vifo)
* Added automatic detection of perltidy in default installations of Strawberry
  Perl/ActivePerl/Cygwin on Windows. (vifo)
* Settings are now reloaded on each run of PerlTidy. (vifo)
* Now using sublime.platform() instead of os.name for getting platform name.
  (vifo)
* Now catching EnvironmentError exceptions instead of OSError in
  tidy_region(). This will also catch IOError exceptions, which previously
  were not catched at all. (vifo)
* Added messages to be displayed by Package Control on installation and
  upgrades in "messages/". Added "messages.json" to link the messages. (vifo)
* Removed accessors: get_perltidy_options(), get_perltidy_rc_paths(). (vifo)
* Refactored most of the code and moved it to perltidy/helpers.py, so we can
  test it, without mocking too much. (vifo)
* Documentation improved. (vifo)

### v0.1.0 - 2012-11-26 19:20:35 +0100

* WindowsError 6 "Invalid handle" occured, while running perltidy via
  subprocess and using temporary files for I/O with perltidy. The error
  occured, because we were not passing PIPEs for STDIN/STDOUT to subprocess.
  This seems to occur on Windows XP only and is somehow related to
  http://bugs.python.org/issue3905. Fixed by always providing subprocess.PIPE
  for all three handles. (vifo)
* Exception handling for running perltidy added. Errors will be checked for
  some common errors and additional hints will be printed on the ST2 console.
  (vifo)
* Restructured code and moved perltidy command validation to
  is_valid_perltidy_cmd(). (vifo)
* get_perltidy_rc_path() renamed to find_perltidyrc_in_project(). (vifo)
* Default settings now in DEFAULT_SETTINGS. (vifo)
* User will now get a warning, if the command provided in "perltidy_cmd" is
  invalid. (vifo)
* When running on Windows, will now search for "perltidy.bat" instead of
  "perltidy", if user did not specify "perltidy_cmd". (vifo)
* Changed subprocess handling. Now using Shell=False, when running commands, so
  we won't have to escape arguments, before passing them to perltidy. This will
  most likely fix issue #3, though I am not able to test it. (vifo)
* Changed passing input to perltidy/reading output from perltidy. If the data
  to be tidied contains any non-ASCII characters, temporary files will be used
  to pass/read data. This allows us for non-ASCII data to be handled correctly.
  Fixes: issue #4. (vifo)
* Added debugging messages. Verbosity level can be set by user in
  "perltidy_log_level". (vifo)
* Reformatted JSON sublime-keymap files. (vifo)
* Fixed #7. Apparently, the Sublime Text 2 API changed and method names are now
  underscored in Sublime Text 2 API. This broke opening of the error output
  view. Not sure, whether compatibiity with earlier ST2 APIs might be an issue?
  (vifo)
* Removed '-sbdl' from default PerlTidy options and added '-sbl'. '-sbdl' is an
  unknown option. (vifo)
* All configuration settings are now user configurable, with sane fallback
  values. In addition to "perltidy_cmd", now also "perltidy_options" and
  "perltidy_default_rc_paths" may be specified. (vifo)
* Changed "perltidy_cmd" handling. Now, its value may also be an array,
  specifying where the Perl interpreter and where PerlTidy is separately, i.e.
  [ "C:\\strawberry\\perl\\bin\\perl.exe", "C:\\strawberry\\perl\\site\\bin\\perltidy" ]
  instead of using wrapper "C:\\strawberry\\perl\\site\\bin\\perltidy.bat".
  Useful on Windows systems, or where the shebang in perltidy specifies a wrong
  Perl interpreter. (vifo)
* "perltidy_rc_paths" now allows the user to specify possible perltidy.rc
  locations. Full file paths are also allowed and will be handled properly.
  Note that now only the first perltidy.rc found in project will be used.  This
  prevents error messages from perltidy. (vifo)
* Output from PerlTidy is now only inserted, if no error occured while running
  PerlTidy. (vifo)
* Cursor repositioning after running PerlTidy is done now only, if no error
  occured running PerlTidy. (vifo)
* Improve the documentation. (vifo)
* Fix error in commands file (kassi)

### v0.0.1 - 2012-07-25 22:00:00 +0100

* Initial version
