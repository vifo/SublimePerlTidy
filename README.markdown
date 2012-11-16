# PerlTidy for Sublime Text 2

## Installation

**With Sublime Text 2 Package Control:** Open *Package Control: Install Package*, search for "PerlTidy" and install.

**Without Git:** Download the latest source from [GitHub](https://github.com/rbo/st2-perltidy/downloads) and copy the st2-perltidy folder to your Sublime Text *Packages* directory.

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

Defaults to *ctrl+shift+t* for Windows / Linux and *super+shift+t* for OSX, since *ctrl+t* is used by some other plugins. Change in *Sublime Text 2 => Preferences => Key Bindings - Default* or *Key Bindings - User*.

### Settings

Open *Sublime Text 2 -> Preferences -> Settings - Default* or *Settings - User*. Add the following lines:

    // Specify full path to perltidy and optionally the Perl interpreter. If
    // not specified, will search PATH for perltidy.
    //"perltidy_cmd": "/opt/perl/bin/perltidy"
    //"perltidy_cmd": [ "C:\\strawberry\\perl\\bin\\perl.exe", "C:\\strawberry\\perl\\site\\bin\\perltidy" ]

    // Specify what perltidy profiles to search for within current project. Note, that
    // only the first matching profile within the project will be used. Absolute paths
    // may also be used.
    //"perltidy_rc_paths": [ "perltidy.rc", ".perltidy.rc" ]

    // Specify perltidy options. Defaults to ['-sbl', '-bbt=1', '-pt=2', '-nbbc', '-l=100', '-ole=unix', '-w', '-se']
    // if not specified.
    //"perltidy_options": ['-sbl', '-bbt=1', '-pt=2', '-nbbc', '-l=100', '-ole=unix', '-w', '-se']

Note that you may also override these global settings by project. In order to do this, add the above lines to your .sublime-project file.

### Default perltidy options

The default perltidy options are set as follows (you may override them by setting *perltidy_options* in your user preferences):

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

  Errors go to STDERR. Please keep this setting, if you want perltidy error messages to apperar in a separate window. Details: [perltidy Documentation | Standard Error Output](http://perltidy.sourceforge.net/perltidy.html#se_standard_error_output).

## TODOs:

* Implement isEnabled

## Known issues:

* On Win32, files containing UTF-8 characters (more specifically: characters that are not within the currently configured Win32 console charmap), will not be formatted properly. This is a limitation of the Win32 console I/O / Python subprocess combo, and may be fixed in the future with temporary files (See Issue #4).
