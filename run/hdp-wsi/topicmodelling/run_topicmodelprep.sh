#!/bin/bash
#argument 1: target word (for adding positional word information)

############
#parameters#
############
#hdp parameters
gamma_b=0.1
alpha_b=1.0
#topic model output directory
output_dir="topicmodel_output"
#stopword file to use
stopword_file="stopwords.txt"
#minimum vocab frequency to filter
voc_minfreq=0

######
#main#
######

#get the target word (if given)
if [ -z $1 ]
then
    echo "./run_topicmodel.sh <target_word>"
    exit 1
fi
if [ -z $2 ]
then
    target_word=$1
else
    target_word=$1
    word=$2
    output_dir=$output_dir/$word
fi

#create generated folder if it hasn't been created
if ! [ -d $output_dir ]
then
    mkdir $output_dir
fi

#generate word stream
python MakeWordStream.py $word.input.txt $output_dir 0

#add positional word information
#echo "adding positional word information to wordstream"
#python AddContextWord.py $target_word < $output_dir/wordstream.train.txt \
    #> $output_dir/wordstream.train.txt.tmp
#mv $output_dir/wordstream.train.txt.tmp $output_dir/wordstream.train.txt  

#generate vocabulary
python MakeVocab.py $output_dir/wordstream.train.txt $output_dir $voc_minfreq

#generate docword
python MakeDocword.py "$output_dir/wordstream.train.txt" \
    "$output_dir/vocabs.txt" "$output_dir/docword.train.txt"

#convert docword to hdp's data format
python ConvertToHDPDataFormat.py < $output_dir/docword.train.txt > \
    $output_dir/hdpdata.train.txt
