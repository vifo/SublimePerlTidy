# perltidy for Sublime Text 2/3

[![Build Status](https://secure.travis-ci.org/vifo/SublimePerlTidy.png)](http://travis-ci.org/vifo/SublimePerlTidy)

PerlTidy is a plugin for [Sublime Text 2](http://www.sublimetext.com/) and [Sublime Text 3](http://www.sublimetext.com/3), which integrates the command line application [perltidy](http://perltidy.sourceforge.net/) into Sublime Text. It indents and reformats [Perl](http://www.perl.org/) source code to make it easier to read.

## Quick start

* Ensure, you have a Perl interpreter and perltidy installed (hint: `apt-get install perltidy`, `yum install perltidy`, `cpan[m] Perl::Tidy`, `ppm install Perl-Tidy`)
* Install this plugin in Sublime Text via Package Control, git or from ZIP (in Sublime Text the plugin is named *PerlTidy*, **not** *SublimePerlTidy*)
* Open a Perl source file and hit `Control+Shift+t`

Read on for detailed installation, usage, configuration and customization instructions.

## Naming conventions

Throughout this documentation, the following naming conventions are used:

* *perltidy*: Refers to the command line application [perltidy](http://perltidy.sourceforge.net/), which does the heavy lifting and tidies up messy Perl source code.

* *PerlTidy*: Refers to this Sublime Text plugin. This is also the name of this plugin within Sublime Text.

* *SublimePerlTidy*: This is the name of the GitHub repository which contains this plugin.

* *st2-perltidy*: This is the old name of this plugin, initially published by [Robert Bohne (rbo)](https://github.com/rbo/). It has been renamed in order to match the Sublime Text plugin naming conventions.

## Installation

* **With Sublime Package Control:** The easiest way to install PerlTidy is through [Sublime Package Control](http://wbond.net/sublime_packages/package_control). If you're not using it yet, get it. Seriously.

  Once you have installed Package Control, restart Sublime Text and bring up the Command Palette (press `Control+Shift+P` on Linux/Windows, `Command+Shift+P` on OS X, or select `Tools->Command Palette...` from menu). Select *Package Control: Install Package*, wait till latest package list has been fetched, then select *PerlTidy* from the list of available packages.

* **With Git:** Clone the repository in your Sublime Text *Packages* directory. Please note that the destination directory must be *PerlTidy*.

        git clone https://github.com/vifo/SublimePerlTidy PerlTidy

The advantage of using either Package Control or git is, that the plugin will be automatically kept up-to-date with the latest version.

* **From ZIP:** Download the latest version [as a ZIP archive](https://github.com/vifo/SublimePerlTidy/archive/master.zip) and copy the directory "SublimePerlTidy-master" from the archive to your Sublime Text *Packages* directory. Rename directory "SublimePerlTidy-master" to "PerlTidy".

The *Packages* directory locations are listed below. If using Sublime Text 3, be sure to replace "2" with "3" in directory names.  Alternatively, selecting `Preferences->Browse Packages...` from Sublime Text menu will get you to the *Packages* directory also.

| OS            | Packages location                                         |
| ------------- | --------------------------------------------------------- |
| OS X          | `~/Library/Application Support/Sublime Text 2/Packages/`  |
| Linux         | `~/.config/sublime-text-2/Packages/`                      |
| Windows       | `%APPDATA%\Sublime Text 2\Packages\`                      |

## Usage

After PerlTidy installation, open a Perl file of your choice and:

* hit `Control+Shift+t`
* or open Command Palette, start typing "perltidy", select "PerlTidy: Tidy" and hit return

to reformat the entire file. PerlTidy also works on selected text only. Give it a try.

## Configuration

Though usage of PerlTidy is quite simple and PerlTidy will do its very best to Just Work™, most aspects can be configured to suite your needs.

### perltidy locations

PerlTidy will try to locate perltidy by:

1. Checking the user setting "perltidy_cmd" for a (valid) user supplied perltidy location.

2. Searching for "perltidy" ("perltidy.bat" on Windows) within directories specified in environment variable *PATH*.

3. Searching for perltidy in platform specific default locations. These are:

* On Windows (in given order):

  Default [Strawberry Perl](http://strawberryperl.com/) installation location *C:\Strawberry*, i.e.:

  ```"perltidy_cmd": [ "C:\\Strawberry\\perl\\bin\\perl.exe", "C:\\Strawberry\\perl\\site\\bin\\perltidy" ]```

  Default [ActivePerl 64-bit](http://www.activestate.com/activeperl) installation location *C:\Perl64*, i.e.:

  ```"perltidy_cmd": [ "C:\\Perl64\\bin\\perl.exe", "C:\\Perl64\\site\\bin\\perltidy" ]```

  Default [ActivePerl 32-bit](http://www.activestate.com/activeperl) installation location *C:\Perl*, i.e.:

  ```"perltidy_cmd": [ "C:\\Perl\\bin\\perl.exe", "C:\\Perl\\site\\bin\\perltidy" ]```

  Default [Cygwin](http://cygwin.com/) installation location *C:\cygwin*, i.e.:

  ```"perltidy_cmd": [ "C:\\cygwin\\bin\\perl.exe", "/usr/local/bin/perltidy" ]```

* On Linux and OS X:

  */usr/bin/perltidy*, */usr/local/bin/perltidy* (which will most likely be in your *PATH* anyway), i.e.:

  ```"perltidy_cmd": [ "/usr/bin/perltidy" ]```

Let PerlTidy try to locate perltidy first. If this does not work, adjust user setting "perltidy_cmd" as needed.

### perltidy options

By default, PerlTidy uses perltidy options as suggested in Damian Conway's [Perl Best Practices (PBP)](http://en.wikipedia.org/wiki/Perl_Best_Practices). Though I don't agree with all of the perltidy settings in the PBP set, using them results in slightly better readable Perl code, than using perltidy's defaults. Since perltidy already supports the PBP set using the command line switch `-pbp` or `--perl-best-practices`, introducing just another set of options seems unnecessary.

So the default PerlTidy options are:

    "perltidy_options": [ "-pbp" ]

which, at least with a recent perltidy version is effectively the same as:

    "perltidy_options": [
        "-l=78", "-i=4", "-ci=4", "-vt=2", "-cti=0", "-pt=1", "-bt=1", "-sbt=1", "-bbt=1", "-nsfs", "-nolq",
        "-wbb=\"% + - * / x != == >= <= =~ !~ < > | & = **= += *= &= <<= &&= -= /= |= >>= ||= //= .= %= ^= x=\"",
        "-st", "-se"
    ]

Ermmm, what?! Fear not, here are the explanations (and differences with perltidy defaults):

| PBP Option      | perltidy Defaults | Description                                                   |
| --------------- | ----------------- | ------------------------------------------------------------- |
| `-l=78`         | `-l=80`           | Maximum line width is 78/80 columns                           |
| `-i=4`          | *same*            | Use 4 columns per indentation level                           |
| `-ci=4`         | `-ci=2`           | Continuation indentation is 4/2 columns                       |
| `-vt=2`         | `-vt=0`           | Vertical tightness set to maximum/minimum                     |
| `-cti=0`        | *same*            | No extra indentation for closing tokens                       |
| `-pt=1`         | *same*            | Medium parenthesis tightness                                  |
| `-bt=1`         | *same*            | Medium brace tightness                                        |
| `-sbt=1`        | *same*            | Medium square bracket tightness                               |
| `-bbt=1`        | `-bbt=0`          | Medium/minimal block brace tightness                          |
| `-nsfs`         | `-sfs`            | Additional space for semicolons in for loops disabled/enabled |
| `-nolq`         | `-olq`            | Outdenting of overly long quoted strings disabled/enabled     |
| `-wbb="..."`    | *none*            | Break before these tokens (operators)                         |
| `-st`           | *none*            | Output to STDOUT                                              |
| `-se`           | *none*            | Errors to STDERR                                              |

You may override any of the above settings by changing user setting "perltidy_options" in your preferences, preferably including the `-pbp` option like this:

    "perltidy_options": [ "-pbp", "-l=120" ]

Please refer to the official [perltidy Documentation](http://perltidy.sourceforge.net/perltidy.html) and the [perltidy Style Guide](http://perltidy.sourceforge.net/stylekey.html) for an explanation of all options available.

### Key bindings

Defaults to `Control+Shift+t` on all platforms. Feel free to change this in `Preferences->Key Bindings - User` by adding and adjusting following lines:

    // PerlTidy key bindings
    {
        "keys": ["ctrl+shift+t"],
        "command": "perl_tidy",
        "context": [ { "key": "selector", "operator": "equal", "operand": "source.perl", "match_all": true } ]
    }

### Other settings

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
    // Linux/OS X with non-standard location or explicit Perl interpreter:
    //"perltidy_cmd": "/opt/perl/bin/perltidy"
    //"perltidy_cmd": [ "/opt/perl-5.18.0/bin/perl", "/opt/perl-5.16.3/site/bin/perltidy" ]

    // Specify possible perltidyrc files to search for within current project. The
    // first matching perltidyrc will be used. Absolute paths may also be used, if
    // you have a global perltidyrc. Defaults to [ ".perltidyrc", "perltidyrc" ].
    //"perltidy_rc_paths": [ ".perltidyrc", "perltidyrc" ]
    //"perltidy_rc_paths": [ "C:\\Users\\USERNAME\\AppData\\Roaming\\perltidyrc" ]

    // Specify perltidy options. Defaults to: [ "-pbp" ]
    //"perltidy_options": [ "-pbp" ]

    // Specify, whether perltidy options given in "perltidy_options" take
    // precedence over options found in perltidyrc files. Defaults to "false"
    // (note: default value was "true" up to version 0.4.0). Adjust to "true" to
    // reverse this order.
    //"perltidy_options_take_precedence": false

    // Log level for perltidy operations. Set to 1 to enable informational
    // messages and to 2 for full debugging. Defaults to 0, so only warnings and
    // errors will be displayed on the console.
    //"perltidy_log_level": 0

    // If, for some reason, you'd like to disable PerlTidy entirely, set
    // "perltidy_enabled" to false. Defaults to true.
    //"perltidy_enabled": true

### Per project settings

You may override any of these settings per project, by adding a section named "settings" with overridden settings to your project file:

    {
        "folders": [
            {
                "path": "..."
            }
        ],
        "settings": {
            "perltidy_log_level": 2,
            "perltidy_options": [ "-pbp", "-l=120", "-w" ]
        }
    }

## Troubleshooting

During normal operation, PerlTidy will emit warnings and errors to the Sublime Text console (open with ``Control+` `` or select `View->Show Console` from menu). In order to enable additional diagnostic messages, adjust user setting "perltidy_log_level" as follows:

* 0 == Warnings and error messages only. This is the default.

* 1 == Print system commands used for tidying up content and perltidyrc file paths used (if any).

* 2 == Full debugging. In addition to the above, print where PerlTidy searches for perltidy and/or perltidyrc.

### Common Pitfalls

#### Windows Error 193

You are running Strawberry Perl/ActivePerl on Windows, and have set a custom path to perltidy via user setting "perltidy_cmd". While trying to run, PerlTidy bails out with the following error message on the ST console:

    PerlTidy: Unable to run perltidy: "C:\Strawberry\perl\site\bin\perltidy" ...
    PerlTidy: OS error was: WindowsError(193, '...')
    PerlTidy: Maybe you have specified the path to "perltidy" instead of "perltidy.bat" in your "perltidy_cmd"?

You have specified the path to the raw Perl "perltidy" file (without extension), instead of the batch wrapper file "perltidy.bat". Windows is unable to execute the former file directly. Yes, typing "perltidy" in *cmd.exe* will work, but only due to the way, how *cmd.exe* handles files without an extension: it will try extensions specified in environment variable *PATHEXT*, eventually find the file "perltidy.bat" and run it.

TL;DR: Assuming you are running a vanilla Strawberry Perl/ActivePerl installation: adjust user setting "perltidy_cmd" to one of the following:

    "perltidy_cmd": [ "C:\\Strawberry\\perl\\bin\\perl.exe", "C:\\Strawberry\\perl\\site\\bin\\perltidy" ]    # for Strawberry Perl
    "perltidy_cmd": [ "C:\\Perl64\\bin\\perl.exe", "C:\\Perl64\\site\\bin\\perltidy" ]                        # for ActivePerl 64-bit
    "perltidy_cmd": [ "C:\\Perl\\bin\\perl.exe", "C:\\Perl\\site\\bin\\perltidy" ]                            # for ActivePerl 32-bit

or, if you really need to use the batch wrapper for some (non-obvious) reasons, to:

    "perltidy_cmd": "C:\\Strawberry\\perl\\site\\bin\\perltidy.bat"       # for Strawberry Perl
    "perltidy_cmd": "C:\\Perl64\\site\\bin\\perltidy.bat                  # for ActivePerl 64-bit
    "perltidy_cmd": "C:\\Perl\\site\\bin\\perltidy.bat"                   # for ActivePerl 32-bit

or just let PerlTidy figure out where perltidy is located by **not setting** "perltidy_cmd" at all.

## Reporting bugs

In order to make bug hunting easier, please ensure, that you always run the *latest* version of PerlTidy. Apart from this, please ensure, that you've set PerlTidy log level to maximum (`"perltidy_log_level": 2` in user settings), in order to get all debugging information possible. Also please include the following information, when submitting an issue:

* Operating system name (i.e. "Windows XP SP3", **not** "Windows")

* Operating system architecture (i.e. 32-bit, 64-bit)

* Sublime Text build number (open `Help->About`)

* Output from Sublime Text console

To gather this information quickly, open ST console, type in the following Python code as-is (in one line) and include its output in your issue:

```python
from __future__ import print_function, unicode_literals;import platform, sublime, datetime;print('-' * 78);print('Date/time: {0}'.format(datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S +0000')));print('Sublime Text version: {0}'.format(sublime.version()));print('Platform: {0}'.format(sublime.platform()));print('CPU architecture: {0}'.format(sublime.arch()));print('OS info: {0}'.format(repr(platform.platform())));print('-' * 78)
```

## Miscellaneous

### Standalone perltidy executable for Windows

If you're running Sublime Text on Windows and don't like to install a complete Perl interpreter just for using perltidy, grab the standalone perltidy executable [from here](https://perltidy.s3.amazonaws.com/perltidy-20121207-x86.exe) and adjust your settings:

    "perltidy_cmd": [ "C:\\WHEREVER_YOU_HAVE_DOWNLOADED_THE_EXE_TO\\perltidy-20121207-x86.exe" ]

This executable has been built with [ActiveState ActivePerl 5.16.3.1603 x86](http://www.activestate.com/activeperl/downloads) using [PAR::Packer](https://metacpan.org/search?q=PAR%3A%3APacker+pp). It contains the Perl interpreter as well as the latest version of perltidy, including all required dependencies in a self contained executable (thus the size of 4.5 MB).

Please note: this executable works for me and is provided **as-is**, with no support whatsoever. If it also works for you, great! If not, please don't complain, but get a Perl interpreter and perltidy for Windows instead. Even better: fix errors, repackage (maybe using helper script "helpers/build_perltidy_20121207_x86.pl" as a starting point) and provide final executable to me for hosting on S3.

## TODOs

* Implement automatic tidying of Perl files upon save. Until then, [SublimeOnSaveBuild](https://github.com/alexnj/SublimeOnSaveBuild) might be an option to achieve this.

## Changes

Only latest changes are listed here. Refer to [full change log](https://github.com/vifo/SublimePerlTidy/blob/master/CHANGES.markdown) for all changes.

### v0.4.2 2013-11-09 13:27:11 +0100

* Update Package Control repository.json schema to version 2.0. (vifo)

### v0.4.1 2013-06-23 18:00:00 +0200

* Fixed bug with empty rows (CRLFs) being inserted into formatted source
  code under Windows. Fixes #17. (vifo)
* Support and tests for ActivePerl 64-bit added. (vifo)
