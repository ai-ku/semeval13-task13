#!/usr/bin/env bash

for n in {1..100}
do
    echo $n
    awk '{printf("%s %s",$1,$2);for(i=0;i<'$n';i++){printf(" %s_%d/1",$1,i)}printf("\n")}' keys/gold-standard/trial.gold-standard.key > out.key
    java -jar supervised/weighted-tau.jar --no-remapping keys/gold-standard/trial.gold-standard.key out.key
    rm out.key
done
