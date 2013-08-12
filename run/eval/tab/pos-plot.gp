set title "POS-based Experiments on Task13 Dataset"
set xlabel "k values (for k-means)"
set ylabel "Performance (0-1)"
set key right center
plot "pos.tab" u 1:4 w lp title "Single Sense Fscore" 
replot "pos.tab" u 1:5 w lp title "Perception Score" 
replot "pos.tab" u 1:3 w lp title "S-Sense Fscore" 
replot "pos.tab" u 1:2 w lp title "Perception Score" 
replot "<echo '22 0.64'"   with points lc rgb 'black' title "AI-KU Single Sense Fscore" 
