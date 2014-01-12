#!/usr/bin/perl -w
use strict;
use File::Temp qw/tempdir/;

my $usage = q{Usage: y-cluster.pl seed cluster
};

my $seed = shift or die $usage;
my $clusters = shift or die $usage;


# gold 
my %targets = ("add.v" => 7, "appear.v" => 13, "ask.v" => 8, "become.v" => 2, "board.n" => 8, "book.n" => 16, "book.v" => 11, "color.n" => 12, "common.j" => 11, "control.n" => 16, "dark.j" => 10, "date.n" => 8, "dismiss.v" => 17, "familiar.j" => 21, "family.n" => 6, "find.v" => 15, "force.n" => 16, "help.v" => 9, "image.n" => 11, "late.j" => 15, "life.n" => 9, "live.v" => 9, "lose.v" => 12, "meet.v" => 13, "new.j" => 9, "number.n" => 13, "paper.n" => 20, "part.n" => 15, "people.n" => 17, "poor.j" => 11, "power.n" => 14, "read.v" => 13, "serious.j" => 9, "serve.v" => 18, "severe.j" => 14, "sight.n" => 12, "sound.n" => 10, "state.n" => 15, "strike.v" => 12, "strong.j" => 13, "suggest.v" => 18, "trace.n" => 12, "trace.v" => 6, "transfer.v" => 11, "wait.v" => 6, "warm.j" => 13, "way.n" => 14, "window.n" => 11, "win.v" => 10, "write.v" => 11);

my $tmp = tempdir("semeval-XXXX", CLEANUP => 1);

my $input = "zcat pairs.100.gz";
my $scode = "../bin/scode -i 50 -a -r 1 -d 25 -z 0.166 -p 50 -u 0.2 -s $seed -v";
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

    #print join(" | ", $input, $filter, $scode, "gzip > $tmp/$key.scode.gz")." & ";
    $process_all .= join(" | ", $input, $filter, $scode, $column, $km, "gzip > $tmp/km$key.gz")." & ";
    #$process_all .= join(" | ", $input, $filter, $scode, "gzip > $tmp/$key.scode.gz")." & ";
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
