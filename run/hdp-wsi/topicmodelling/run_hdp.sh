#!/bin/bash
############
#parameters#
############
#hdp parameters
gamma_b=0.1
alpha_b=$1
#topic model output directory
output_dir="topicmodel_output"
#stopword file to use
stopword_file="stopwords.txt"
#minimum vocab frequency to filter
voc_minfreq=0
max_iter=1000
CPU=10

#run hdp
#compile the code
cd hdp
make
cd ..

files=`find topicmodel_output/ -type d | grep "/*.[vnj]" | sort`
num_files=`find topicmodel_output/ -type d | grep "/*.[vnj]" | wc -l `

echo ---------------------
echo Number of files: $num_files
echo ---------------------


# parameter details for hdp are in run_hdp_args.py
./run_hdp_args.py $max_iter $gamma_b $alpha_b $files | \
    xargs -n 14 -P $CPU ./hdp/hdp


#count=0
#for output_dir in $files
#do
    #./hdp/hdp --algorithm train --data $output_dir/hdpdata.train.txt --directory $output_dir \
        #--max_iter $max_iter --save_lag -1 --gamma_b $gamma_b --alpha_b $alpha_b &
    #count=$(($count + 1))
    #n=$(($count%$CPU))
    #if [ $n -eq 0 ]
    #then
        #wait
    #fi
#done
#wait

echo -----------------------
echo "all HDP processes done"
echo -----------------------

for output_dir in $files
do
    echo $output_dir
#print the topic/sense distribution for each document
python CalcHDPTopics.py -1 $output_dir/mode-word-assignments.dat \
    $output_dir/docword.train.txt.empty > $output_dir/topicsindocs.txt

#print the induced topics/senses
./hdp/print.topics.R $output_dir/mode-topics.dat $output_dir/vocabs.txt \
    $output_dir/topics.txt 10
python hdp/ConvertTopicDisplayFormat.py < $output_dir/topics.txt > $output_dir/topics.txt.tmp 
mv $output_dir/topics.txt.tmp $output_dir/topics.txt
 
#create the topic-word-probability pickle
python hdp/CreateTopicWordProbPickle.py $output_dir/mode-topics.dat \
    $output_dir/vocabs.txt $output_dir/topics.pickle
done
