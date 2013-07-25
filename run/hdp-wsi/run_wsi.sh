#!/bin/bash
#Main script that drives the WSI system. Uses HDP as the topic model for inducing senses.

if [ $# != 2 ] 
then
    echo "Wrong #of args: Provide gamma and alpha. Default: 0.1 1"
    echo $#, $0, $1, $2
    exit
else
    gamma=$1
    alpha=$2
fi

#parameters
input_dir="wsi_input/example"
output_dir="wsi_output"
wsd_output="tm_wsi" #output file that contains the sense distribution for each document

#variables (shouldn't need to change this)
wsi_type="all"

#check if necessary output directories are created
if ! [ -d $output_dir/topic_wordprob ]
then
    mkdir -p $output_dir/topic_wordprob
fi

#delete the any previously generated wsd prediction
rm $output_dir/$wsd_output 2>/dev/null
rm $output_dir/$wsd_output.topics 2>/dev/null

#extract the sentences from the dataset (test then train)
for file in `ls $input_dir/$wsi_type`
do
    echo "Processing $file"

    #get the word
    word=`basename $file .lemma`
    word_pat=`echo $word | sed -e 's/\./\\\./g'`

    #get the number of test_instances
    #num_test_inst=`grep "^$word_pat" $input_dir/num_test_instances.$wsi_type.txt | cut -f 2-2 -d \ `
    #echo -e "\tNumber of test instances = $num_test_inst"

    #link the input text in the hdp directory
    cd topicmodelling/
    rm $word.input.txt 2>/dev/null
    ln -s ../$input_dir/$wsi_type/$word.lemma $word.input.txt

    #do topic modelling
    target_word=`echo $word | cut -f 1-1 -d\.`
    #remove hyphen
    target_word=`echo $target_word | cut -f 1-1 -d-`
    rm topicmodel_output/$word/* 2>/dev/null
    # only one time needs to be run topicmodelprep
    ./run_topicmodelprep.sh $target_word $word

    #remove the softlinked file
    rm $word.input.txt

    #change back to wsi directory
    cd ../
done

# run hdp in parallel
cd topicmodelling/
./run_hdp.sh $gamma $alpha
#creating results
../run_create_res_files.sh
cd ../
