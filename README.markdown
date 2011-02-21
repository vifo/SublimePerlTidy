# PerlTidy for Sublime Text 2 - rbo@cpan.org

## Added key binding:
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
