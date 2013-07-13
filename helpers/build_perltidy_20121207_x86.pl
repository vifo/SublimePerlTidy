#!/usr/bin/env perl

# Build standalone perltidy executable on and for Windows using PAR::Packer.
# So far, tested with ActiveState Perl 5.16.3 (32-bit) only.

use 5.010001;
use strict;
use warnings;
use autodie;
use Digest::MD5;
use Digest::SHA1;
use Carp;

sub run {
    my ( $header, $cmd ) = @_;
    print_header($header);

    if ( ref $cmd eq 'CODE' ) {
        $cmd->();
    }
    else {
        say join ' ', @{$cmd};
        system @{$cmd};
    }
}

sub print_header {
    my $header = shift;

    say '';
    say $header;
    say '=' x length $header;
}

$^O =~ m/win32/i or croak 'This script must be run on Windows';

print_header 'Building standalone perltidy';

run 'Date/time (UTC)',        sub { say scalar gmtime };
run 'Build environment',      ['set'];
run 'Perl version',           [ 'perl', '-V' ];
run 'Installed CPAN modules', [ 'cpan', '-l' ];

run 'PAR::Packer version', sub { require PAR::Packer; say $PAR::Packer::VERSION };
run 'Perl::Tidy version',  sub { require Perl::Tidy;  say $Perl::Tidy::VERSION };

mkdir 'build';
chdir 'build';
my $perltidy_version = $Perl::Tidy::VERSION;
my $perltidy_exe_filename = sprintf 'perltidy-%s-x86.exe', $perltidy_version;

run 'Running build', [ 'pp', '-v', '-o', $perltidy_exe_filename, 'C:\\Perl\\site\\bin\\perltidy' ];

print_header 'Build done';

run 'Running standalone perltidy', [ $perltidy_exe_filename, '--version' ];

run 'Digests/filesize', ['dir'];

open my $fh, '<', $perltidy_exe_filename;
binmode $fh;

my $md5_ctx = Digest::MD5->new;
$md5_ctx->addfile($fh);
say sprintf 'MD5 sum:  %s', $md5_ctx->hexdigest;

seek $fh, 0, 0;

my $sha1_ctx = Digest::SHA1->new;
$sha1_ctx->addfile($fh);
say sprintf 'SHA1 sum: %s', $sha1_ctx->hexdigest;

print_header 'All done'
