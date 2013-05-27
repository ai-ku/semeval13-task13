#!/usr/bin/perl -w
use strict;
use File::Temp qw/tempdir/;

my $usage = q{Usage: y-cluster.pl seed cluster
};

my $seed = shift or die $usage;
my $clusters = shift or die $usage;

my %targets = ("add.v" => 6,
	       "appear.v" => 6,
	       "ask.v" => 6,
	       "become.v" => 6,
	       "board.n" => 6,
	       "book.n" => 6,
	       "book.v" => 6,
	       "color.n" => 6,
	       "common.j" => 6,
	       "control.n" => 6,
	       "dark.j" => 6,
	       "date.n" => 6,
	       "dismiss.v" => 6,
	       "familiar.j" => 6,
	       "family.n" => 6,
	       "find.v" => 6,
	       "force.n" => 6,
	       "help.v" => 6,
	       "image.n" => 6,
	       "late.j" => 6,
	       "life.n" => 6,
	       "live.v" => 6,
	       "lose.v" => 6,
	       "meet.v" => 6,
	       "new.j" => 6,
	       "number.n" => 6,
	       "paper.n" => 6,
	       "part.n" => 6,
	       "people.n" => 6,
	       "poor.j" => 6,
	       "power.n" => 6,
	       "read.v" => 6,
	       "serious.j" => 6,
	       "serve.v" => 6,
	       "severe.j" => 6,
	       "sight.n" => 6,
	       "sound.n" => 6,
	       "state.n" => 6,
	       "strike.v" => 6,
	       "strong.j" => 6,
	       "suggest.v" => 6,
	       "trace.n" => 6,
	       "trace.v" => 6,
	       "transfer.v" => 6,
	       "wait.v" => 6,
	       "warm.j" => 6,
	       "way.n" => 6,
	       "window.n" => 6,
	       "win.v" => 6,
	       "write.v" => 6);

my $tmp = tempdir("semeval-XXXX", CLEANUP => 1);

my $input = "zcat pairs.100.gz";
my $scode = "scode -i 50 -a -r 1 -d 25 -z 0.166 -p 50 -u 0.2 -s $seed -v";
my $column = "perl -ne 'print if s/^1://'";
my $kmeans = "wkmeans -r 128 -l -w -v -s $seed -k ";

my $process_all = "";
foreach my $key (keys %targets) {
    my $filter = "grep -P '^<$key'";

    my $km = $kmeans.$targets{$key};
    if ($clusters ne "gold") {
	$km = $kmeans.$clusters;
    }
#    print join(" | ", $input, $filter, $scode, $column, $km, "gzip > $tmp/km$key.gz")." &\n";

    $process_all .= join(" | ", $input, $filter, $scode, $column, $km, "gzip > $tmp/km$key.gz")." & ";
}

system($process_all."wait");

$process_all = "";
foreach my $key (keys %targets) {
    $process_all .= "zcat pairs.100.gz | grep -P '^<$key.\\d{1,3}>' | find-sense-test.py $tmp/km$key.gz >> $tmp/out$key.key & ";
}

system($process_all."wait");

foreach my $key (keys %targets) {
    open(OUT, "<$tmp/out$key.key");
    while (<OUT>) {
	print $_;
    }
    close(OUT);
}
