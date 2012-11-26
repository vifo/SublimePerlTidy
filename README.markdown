# PerlTidy for Sublime Text 2

PerlTidy is a plugin for [Sublime Text 2](http://www.sublimetext.com/), which integrates [perltidy](http://perltidy.sourceforge.net/) into ST2. It indents and reformats Perl scripts to make them easier to read.

## Installation

**With Sublime Package Control:**  The easiest way to install PerlTidy is through [Sublime Package Control](http://wbond.net/sublime_packages/package_control).

Once you have installed Package Control, restart Sublime Text 2 and bring up the Command Palette (press `Control+Shift+P` on Linux/Windows, `Command+Shift+P` on OS X, or select `Tools->Command Palette...` from menu). Select "Package Control: Install Package", wait till Package Control fetches the latest package list, then select "PerlTidy" from the list of available packages. The advantage of using this method is, that Package Control will automatically keep PerlTidy up to date with the latest version.

**Without Git:** Download the latest source from [GitHub](https://github.com/rbo/st2-perltidy/downloads) and copy the folder *st2-perltidy* to your Sublime Text *Packages* directory.

**With Git:** Clone the repository in your Sublime Text *Packages* directory:

    git clone https://github.com/rbo/st2-perltidy

The *Packages* directory is located at:

* OS X:

    ~/Library/Application Support/Sublime Text 2/Packages/

* Linux:

    ~/.config/sublime-text-2/Packages/

* Windows:

    %APPDATA%/Sublime Text 2/Packages/

## Configuration

### Key bindings

Defaults to `Ctrl+Shift+t` for Windows/Linux and `Super+Shift+t` for OS X, since `Ctrl+t` is used by some other plugins. Change in `Preferences->Key Bindings->Default` or `Preferences->Key Bindings - User`.

### Settings

Open `Preferences->Settings - Default` or `Preferences->Settings - User`. Add the following lines:

    // Specify full path to perltidy and optionally the Perl interpreter. If
    // not specified, will search PATH for perltidy. Please note, that on
    // Win32, you must either specify either the full path to the batch
    // wrapper "perltidy.bat"  (NOT "perltidy"), or specify the Perl
    // interpreter path AND the path to the "raw" "perltidy" file. The latter
    // is preferred, since we don't really need the batch wrapper at all.
    // Settings below are known to work with a default Strawberry Perl
    // installation.
    //"perltidy_cmd": "/opt/perl/bin/perltidy"
    //"perltidy_cmd": [ "C:\\strawberry\\perl\\bin\\perl.exe", "C:\\strawberry\\perl\\site\\bin\\perltidy" ]
    //"perltidy_cmd": [ "C:\\strawberry\\perl\\site\\bin\\perltidy.bat" ]   // possible, but not needed

    // Specify what perltidyrc files to search for within current project.
    // Note, that only the first matching perltidyrc within the project will
    // be used. Absolute paths may also be used.
    //"perltidy_rc_paths": [ ".perltidyrc", "perltidyrc" ]

    // Specify perltidy options. Defaults to
    // [ "-sbl", "-bbt=1", "-pt=2", "-nbbc", "-l=100", "-ole=unix", "-w", "-se" ]
    // if not given.
    //"perltidy_options": [ "-sbl", "-bbt=1", "-pt=2", "-nbbc", "-l=100", "-ole=unix", "-w", "-se" ]

    // Log level for perltidy operations. Set to 1 to enable informational
    // messages and to 2 for full debugging. Defaults to 0, so only warnings
    // and errors will be displayed on the console.
    //"perltidy_log_level": 0

    // If, for some reason, you'd like to disable PerlTidy entirely, set
    // "perltidy_enabled" to false. Defaults to true.
    //"perltidy_enabled": true

### Default perltidy options

The default perltidy options are set as follows (you may override them by setting "perltidy_options" in your user preferences). Please refer to the offical [perltidy Documentation](http://perltidy.sourceforge.net/perltidy.html) and the [perltidy Style Guide](http://perltidy.sourceforge.net/stylekey.html) for an explanation of all options available.

* -sbl

  Opening sub braces on new line. Details: [perltidy Documentation | Opening Sub Brace On New Line](http://perltidy.sourceforge.net/perltidy.html#sbl_opening_sub_brace_on_new_line).

* -bbt=1

   Block brace tightness. Details: [perltidy Documentation | Tightness of curly braces, parentheses, and square brackets](http://perltidy.sourceforge.net/perltidy.html#tightness_of_curly_braces_parentheses_and_square_brackets).

* -pt=2

  Parens tightness. Details: [perltidy Documentation | Tightness of curly braces, parentheses, and square brackets](http://perltidy.sourceforge.net/perltidy.html#tightness_of_curly_braces_parentheses_and_square_brackets).

* -nbbc

  No blanks before comments. Details: [perltidy Documentation | Blank Line Control](http://perltidy.sourceforge.net/perltidy.html#blank_line_control).

* -l=100

  Maximum line length is 100 characters. Details: [perltidy Documentation | Maximum Line Length](http://perltidy.sourceforge.net/perltidy.html#l_n_maximum_line_length_n).

* -ole=unix

  Output line endings are UNIX style. Details: [perltidy Documentation | Output Line Endings](http://perltidy.sourceforge.net/perltidy.html#ole_s_output_line_ending_s).

* -w

  All warnings enabled. Details: [perltidy Documentation | Warning Output](http://perltidy.sourceforge.net/perltidy.html#w_warning_output).

* -se

  Errors go to STDERR. **Please ensure, that you include this settings, when changing default options.** Otherwise, perltidy error messages won't appear in a separate window. Details: [perltidy Documentation | Standard Error Output](http://perltidy.sourceforge.net/perltidy.html#se_standard_error_output).

## Troubleshooting

During normal operation, PerlTidy will emit warnings and errors to the Sublime Text 2 console (open with ``Ctrl+` ``). In order to enable additional diagnostic messages, adjust user setting "perltidy_log_level" as follows:

* 0 == Warnings and error messages only. This is the default.

* 1 == Print system commands used for tidying up content and perltidyrc file paths used (if any).

* 2 == Full debugging. In addition to the above, print where PerlTidy searches for perltidy and/or perltidyrc.

### Common Errors

#### Windows Error 193

You are running on Win32, and have set a custom perltidy path via user setting "perltidy_cmd". While trying to run, PerlTidy bails out with the following error message on the ST2 console:

    PerlTidy: Unable to run perltidy: "C:\Strawberry\perl\site\bin\perltidy" ...
    PerlTidy: OS error was: WindowsError(193, '...')
    PerlTidy: Maybe you have specified the path to "perltidy" instead of "perltidy.bat" in your "perltidy_cmd"?

You have specified the path to the *perltidy* Perl file, instead of the batch wrapper *perltidy.bat*. Win32 is unable to execute this file directly. Yes, running this file in *cmd.exe* will work, but only due to the way, how cmd.exe handles files without an extension: it will add extensions in environment variable *PATHEXT*, eventually finally find the *perltidy.bat* and run it.

TL/DR: Assuming you are running a vanilla installation of [Strawberry Perl](http://strawberryperl.com/): adjust "perltidy_cmd" user setting to either:

    "perltidy_cmd": [ "C:\\Strawberry\\perl\\bin\\perl.exe", "C:\\Strawberry\\perl\\site\\bin\\perltidy" ]

or to the following, if you really need to use the batch wrapper for some (non-obvious) reason:

    "perltidy_cmd": "C:\\Strawberry\\perl\\site\\bin\\perltidy.cmd"

## TODOs

* Implement automatic tidying upon save.


## Changes

### v0.1.0 - 2012-11-26 19:20:35 +0100

* WindowsError 6 "Invalid handle" occured, while running perltidy via
  subprocess and using temporary files for I/O with perltidy. The error
  occured, because we were not passing PIPEs for STDIN/STDOUT to
  subprocess. This seems to occur on Windows XP only and is somehow
  related to http://bugs.python.org/issue3905. Fixed by always
  providing subprocess.PIPE for all three handles. (vifo)
* Exception handling for running perltidy added. Errors will be checked
  for some common errors and additional hints will be printed on the
  ST2 console. (vifo)
* Restructured code and moved perltidy command validation to
  is_valid_perltidy_cmd(). (vifo)
* get_perltidy_rc_path() renamed to find_perltidyrc_in_project(). (vifo)
* Default settings now in DEFAULT_SETTINGS. (vifo)
* User will now get a warning, if the command provided in "perltidy_cmd" is
  invalid. (vifo)
* When running on Win32, will now search for "perltidy.bat" instead of
  "perltidy", if user did not specify "perltidy_cmd". (vifo)
* Changed subprocess handling. Now using Shell=False, when running commands,
  so we won't have to escape arguments, before passing them to perltidy. This
  will most likely fix issue #3, though I am not able to test it. (vifo)
* Changed passing input to perltidy/reading output from perltidy. If the data
  to be tidied contains any non-ASCII characters, temporary files will be
  used to pass/read data. This allows us for non-ASCII data to be handled
  correctly. Fixes: issue #4. (vifo)
* Added debugging messages. Verbosity level can be set by user in
  "perltidy_log_level". (vifo)
* Reformatted JSON sublime-keymap files. (vifo)
* Fixed #7. Apparently, the Sublime Text 2 API changed and method names are
  now underscored in Sublime Text 2 API. This broke opening of the error output
  view. Not sure, whether compatibiity with earlier ST2 APIs might be an issue? 
  (vifo)
* Removed '-sbdl' from default PerlTidy options and added '-sbl'. '-sbdl' is
  an unknown option. (vifo)
* All configuration settings are now user configurable, with sane fallback
  values. In addition to "perltidy_cmd", now also "perltidy_options" and
  "perltidy_default_rc_paths" may be specified. (vifo)
* Changed "perltidy_cmd" handling. Now, its value may also be an array,
  specifying where the Perl interpreter and where PerlTidy is separately, i.e.
  [ "C:\\strawberry\\perl\\bin\\perl.exe", "C:\\strawberry\\perl\\site\\bin\\perltidy" ]
  instead of using wrapper "C:\\strawberry\\perl\\site\\bin\\perltidy.bat".
  Useful on Win32 systems, or where the shebang in perltidy specifies a wrong
  Perl interpreter. (vifo)
* "perltidy_rc_paths" now allows the user to specify possible perltidy.rc
  locations. Full file paths are also allowed and will be handled properly.
  Note that now only the first perltidy.rc found in project will be used.  This
  prevents error messages from perltidy. (vifo)
* Output from PerlTidy is now only inserted, if no error occured while
  running PerlTidy. (vifo)
* Cursor repositioning after running PerlTidy is done now only, if no
  error occured running PerlTidy. (vifo)
* Improve the documentation. (vifo)
* Fix error in commands file (kassi)

### v0.0.1 - 2012-07-25 22:00:00 +0100

* Initial version



