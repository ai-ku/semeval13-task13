#!/usr/bin/perl -w
use strict;
use PDL;

my $pos = $ARGV[0];

my %X;
my %W;
open(FP, "zcat $pos.variance.scode.gz |");
while(<FP>) {
    my ($word, $count, @rest) = split;
    $W{$word} = $count;
    $X{$word} = pdl(@rest);
}
close(FP);

my %sum;
my %cnt;
open(FP, "zcat $pos.variance.pairs.100.gz |");
while(<FP>) {
    my ($wx, $wy) = split;
    my $x = $X{"0:$wx"};
    my $y = $X{"1:$wy"};
    my $d = $x - $y;
    $sum{$wx} += inner($d, $d);
    $cnt{$wx}++;
}
close(FP);

for my $w (keys %sum) {
    my $std = sqrt($sum{$w} / $cnt{$w});
    print "$w\t$std\n";
}


#zcat adj.all.scode.gz | grep -P  '^0:<.*.\d{1,3}>'

