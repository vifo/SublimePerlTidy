# PerlTidy for Sublime Text 2

## Adding key binding:
Defaults to ctrl+shift+t for Windows / Linux and super+shift+t for OSX,
since ctrl+t is used by some other plugins.

To change:
Sublime Text 2 -> Preferences -> User Key Bindings
Add line:
    { "keys": ["ctrl+t"], "command":"perl_tidy"}

## Configuring the command perltidy
Sublime Text 2 -> Preferences -> User File Preferences
Add line:
    "perltidy_cmd": "/opt/perl/bin/perltidy"

## TODO:
* Implementing isEnabled
* Read perltidyrc from project root, possible?
  or read perldity config from st2 config
