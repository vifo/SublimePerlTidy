# PerlTidy for Sublime Text 2

PerlTidy is a plugin for [Sublime Text 2](http://www.sublimetext.com/), which integrates [perltidy](http://perltidy.sourceforge.net/) into ST2. It indents and reformats Perl source code to make it easier to read.

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

    %APPDATA%\Sublime Text 2\Packages\

## Configuration

### perltidy locations

PerlTidy will try to locate perltidy by:

1. Checking the user setting "perltidy_cmd" for a (valid) user supplied perltidy location.

2. Searching for "perltidy" ("perltidy.bat" on Windows) within directories specified in environment variable *PATH*.

3. Searching for perltidy in platform specific default locations. These are:

* On Windows (in given order):

  Default [Strawberry Perl](http://strawberryperl.com/) installation location *C:\Strawberry*, i.e.:

  ```"perltidy_cmd": [ "C:\\Strawberry\\perl\\bin\\perl.exe", "C:\\Strawberry\\perl\\site\\bin\\perltidy" ]```

  Default [ActivePerl](http://www.activestate.com/activeperl) installation location *C:\Perl*, i.e.:

  ```"perltidy_cmd": [ "C:\\Perl\\bin\\perl.exe", "C:\\Perl\\site\\bin\\perltidy" ]```

  Default [Cygwin](http://cygwin.com/) installation location *C:\cygwin*, i.e.:

  ```"perltidy_cmd": [ "C:\\cygwin\\bin\\perl.exe", "/usr/local/bin/perltidy" ]```

* On Linux and OSX:

  */usr/bin/perltidy*, */usr/local/bin/perltidy* (which will most likely be in your *PATH* anyway).

Let PerlTidy try to locate perltidy first. If this does not work, adjust user setting "perltidy_cmd" as needed.

### Default perltidy options

The default perltidy options are set as follows (you may override them by changing user setting "perltidy_options" in your preferences). Please refer to the official [perltidy Documentation](http://perltidy.sourceforge.net/perltidy.html) and the [perltidy Style Guide](http://perltidy.sourceforge.net/stylekey.html) for an explanation of all options available.

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

### Key bindings

Defaults to `Control+Shift+t` for Windows/Linux and `Command+Shift+t` for OS X, since `Control+t` is used by some other plugins. Change in `Preferences->Key Bindings - User` by adding and adjusting following lines:

    // PerlTidy key bindings
    {
        "keys": ["ctrl+shift+t"],
        "command": "perl_tidy",
        "context": [ { "key": "selector", "operator": "equal", "operand": "source.perl", "match_all": true } ]
    }

### Settings

If you'd like to override specific settings, open `Preferences->Settings - User` and add/adjust the following lines:

    // Specify full path to perltidy and optionally the Perl interpreter. If not
    // specified, will search PATH for perltidy and fall back to platform default
    // locations.
    //
    // Please note, that with Strawberry Perl/ActivePerl on Windows, you have to
    // either specify the full path to the Perl interpreter AND the perltidy file
    // (NOT "perltidy.bat"), OR the full path to the batch wrapper file
    // "perltidy.bat". The former is preferred, we don't need the batch wrapper.
    //
    // Windows/Strawberry Perl/ActivePerl:
    //"perltidy_cmd": [ "C:\\Strawberry\\perl\\bin\\perl.exe", "C:\\Strawberry\\perl\\site\\bin\\perltidy" ]
    //"perltidy_cmd": [ "C:\\Perl\\bin\\perl.exe", "C:\\Perl\\site\\bin\\perltidy" ]
    //
    // Windows/Cygwin:
    //"perltidy_cmd": [ "C:\\cygwin\\bin\\perl.exe", "/usr/local/bin/perltidy" ]
    //
    // Linux/OSX with non-standard location or explicit Perl interpreter:
    //"perltidy_cmd": "/opt/perl/bin/perltidy"
    //"perltidy_cmd": [ "/opt/perl-5.16.2/bin/perl", "/opt/perl-5.10.1/site/bin/perltidy" ]

    // Specify possible perltidyrc files to search for within current project. The
    // first matching perltidyrc will be used. Absolute paths may also be used, if
    // you have a global perltidyrc. Defaults to [ ".perltidyrc", "perltidyrc" ].
    //"perltidy_rc_paths": [ ".perltidyrc", "perltidyrc" ]
    //"perltidy_rc_paths": [ "C:\\Users\\USERNAME\\AppData\\Roaming\\perltidyrc" ]

    // Specify perltidy options. Defaults to: [ "-sbl", "-bbt=1", "-pt=2", "-nbbc", "-l=100", "-ole=unix", "-w", "-se" ]
    //"perltidy_options": [ "-sbl", "-bbt=1", "-pt=2", "-nbbc", "-l=100", "-ole=unix", "-w", "-se" ]

    // Specify, whether perltidy options given in "perltidy_options" take
    // precedence over options found in perltidyrc files. Defaults to "true".
    // Adjust to "false" to reverse this order.
    //"perltidy_options_take_precedence": true

    // Specify, whether PerlTidy should always use temporary files, instead
    // of process pipes to filter code. Using temporary files is slower, but
    // fails, if the source code contains non ASCII characters. Set this option
    // to true, to force temporary file usage, or to 'auto', to let PerlTidy
    // decide. Defaults to 'auto'.
    //"perltidy_use_temporary_files": 'auto'

    // Log level for perltidy operations. Set to 1 to enable informational
    // messages and to 2 for full debugging. Defaults to 0, so only warnings and
    // errors will be displayed on the console.
    //"perltidy_log_level": 0

    // If, for some reason, you'd like to disable PerlTidy entirely, set
    // "perltidy_enabled" to false. Defaults to true.
    //"perltidy_enabled": true

You may override any of these settings per project, by adding a section named "settings" with overridden settings to your project file:

    {
        "folders": [
            {
                "path": "..."
            }
        ],
        "settings": {
            "perltidy_log_level": 2,
            "perltidy_options": [ "-l=120", "-ole=unix", "-w", "-se" ]
        }
    }

## Troubleshooting

During normal operation, PerlTidy will emit warnings and errors to the Sublime Text 2 console (open with ``Control+` `` or select `View->Show Console` from menu). In order to enable additional diagnostic messages, adjust user setting "perltidy_log_level" as follows:

* 0 == Warnings and error messages only. This is the default.

* 1 == Print system commands used for tidying up content and perltidyrc file paths used (if any).

* 2 == Full debugging. In addition to the above, print where PerlTidy searches for perltidy and/or perltidyrc.

### Common Pitfalls

#### Windows Error 193

You are running Strawberry Perl/ActivePerl on Windows, and have set a custom path to perltidy via user setting "perltidy_cmd". While trying to run, PerlTidy bails out with the following error message on the ST2 console:

    PerlTidy: Unable to run perltidy: "C:\Strawberry\perl\site\bin\perltidy" ...
    PerlTidy: OS error was: WindowsError(193, '...')
    PerlTidy: Maybe you have specified the path to "perltidy" instead of "perltidy.bat" in your "perltidy_cmd"?

You have specified the path to the raw Perl "perltidy" file (without extension), instead of the batch wrapper file "perltidy.bat". Windows is unable to execute the former file directly. Yes, typing "perltidy" in *cmd.exe* will work, but only due to the way, how *cmd.exe* handles files without an extension: it will try extensions specified in environment variable *PATHEXT*, eventually find the file "perltidy.bat" and run it.

TL/DR: Assuming you are running a vanilla Strawberry Perl/ActivePerl installation: adjust user setting "perltidy_cmd" to one of the following:

    "perltidy_cmd": [ "C:\\Strawberry\\perl\\bin\\perl.exe", "C:\\Strawberry\\perl\\site\\bin\\perltidy" ]    # for Strawberry Perl
    "perltidy_cmd": [ "C:\\Perl\\bin\\perl.exe", "C:\\Perl\\site\\bin\\perltidy" ]                            # for ActivePerl

or, if you really need to use the batch wrapper for some (non-obvious) reasons, to:

    "perltidy_cmd": "C:\\Strawberry\\perl\\site\\bin\\perltidy.bat"       # for Strawberry Perl
    "perltidy_cmd": "C:\\Perl\\site\\bin\\perltidy.bat"                   # for ActivePerl

or just let PerlTidy figure out where perltidy is located by *not setting* "perltidy_cmd" at all.

## Reporting bugs

In order to make bug hunting easier, please ensure, that you always run the *latest* version of PerlTidy. Apart from this, please ensure, that you've set PerlTidy log level to maximum (`"perltidy_log_level": 2` in user settings), in order to get all debugging information possible. Also please include the following information, when submitting an issue:

* Operating system name (i.e. "Windows XP SP3", **not** "Windows")

* Operating system architecture (i.e. 32-bit, 64-bit)

* Sublime Text 2 build number (open `Help->About`)

* Output from Sublime Text 2 console

To gather this information quickly, open ST2 console, type in the following Python code as-is (in one line) and include its output in your issue:

```
import platform; import sublime; import datetime; print '-' * 78; print "Date/time: " + datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S +0000'); print "ST2 version: " + sublime.version(); print "ST2 platform: " + sublime.platform(); print "CPU architecture: " + sublime.arch(); print "OS info: " + repr(platform.platform()); print '-' * 78
```

## TODOs

* Implement automatic tidying of Perl files upon save. Until then, [SublimeOnSaveBuild](https://github.com/alexnj/SublimeOnSaveBuild) might be an option to achieve this.

## Changes

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
