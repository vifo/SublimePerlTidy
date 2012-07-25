# PerlTidy for Sublime Text 2

## Adding key binding:
Defaults to ctrl+shift+t for Windows / Linux and super+shift+t for OSX,
since ctrl+t is used by some other plugins.

## Configuring the command perltidy
Sublime Text 2 -> Preferences -> User File Preferences
Add line:
    "perltidy_cmd": "/opt/perl/bin/perltidy"

## TODO:
* Implementing isEnabled
* Read perltidyrc from project root, possible?
  or read perldity config from st2 config
