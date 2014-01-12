#!/usr/bin/perl -w
use strict;
use File::Temp qw/tempdir/;

my $usage = q{Usage: y-cluster.pl seed cluster
};

my $seed = shift or die $usage;
my $clusters = shift or die $usage;

my %targets = ("add.v" => 6,
	       "ask.v" => 7,
	       "win.v" => 4,
	       "argument.n" => 7,
	       "interest.n" => 7,
	       "paper.n" => 7,
	       "different.a" => 5,
	       "important.a" => 5);

my $tmp = tempdir("semeval-XXXX", CLEANUP => 1);

my $input = "zcat pairs.100.gz";
my $scode = "scode -i 50 -a -r 1 -d 25 -z 0.166 -p 50 -u 0.2 -s $seed -v";
my $column = "perl -ne 'print if s/^1://'";
my $kmeans = "wkmeans -r 128 -l -w -v -s $seed -k ";

my $process_all = "";
foreach my $key (keys %targets) {
    (my $target = $key) =~ s/\.a/.[aj]/;
    my $filter = "grep -P '^<$target'";

    my $km = $kmeans.$targets{$key};
    if ($clusters ne "gold") {
	$km = $kmeans.$clusters;
    }
#    print join(" | ", $input, $filter, $scode, $column, $km, "gzip > $tmp/km$key.gz")." &\n";

    $process_all .= join(" | ", $input, $filter, $scode, $column, $km, "gzip > $tmp/km$key.gz")." & ";
}

system($process_all."wait");

foreach my $key (keys %targets) {
    system("zcat pairs.100.gz | grep -P '^<$key.[^\\d]' | find-sense.py $tmp/km$key.gz >> $tmp/out.key");
}

open(OUT, "<$tmp/out.key");
while (<OUT>) {
    print $_;
}
close(OUT);
