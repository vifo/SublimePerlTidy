#!/usr/bin/env perl

use 5.010001;
use strict;
use warnings;
use autodie;

say do {
    open my $fh, '<', 'issue_sys_info.py';
    join ';', grep { !/^(?:\#.*|\s*)$/x } map { s/\r?\n//x; $_ } <$fh>;
};
