#!/bin/sh

# Sublime Text 2/3 PerlTidy Cygwin wrapper.
#
# Use, when running under Windows with Cygwin and getting warnings from
# Perl/Cygwin. Sets locale, so Perl does not complain and lets Cygwin accept
# the MS-DOS file paths of temporary files.

export LANG="C"
export CYGWIN="${CYGWIN} nodosfilewarning"

# Perl and perltidy in default locations of a Cygwin installation. Adjust, if
# necessary.
exec /usr/bin/perl /usr/local/bin/perltidy "$@"
