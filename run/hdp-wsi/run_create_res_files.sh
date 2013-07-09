#!/bin/bash
#parameters
input_dir="wsi_input/example"
output_dir="wsi_output"
wsd_output="tm_wsi" #output file that contains the sense distribution for each document
#variables (shouldn't need to change this)
wsi_type="all"

for file in `ls ../$input_dir/$wsi_type`
do

    word=`basename $file .lemma`
    word_pat=`echo $word | sed -e 's/\./\\\./g'`
    num_test_inst=`grep "^$word_pat" ../$input_dir/num_test_instances.$wsi_type.txt | cut -f 2-2 -d \ `
    echo -e "\tNumber of test instances for $word = $num_test_inst"
    #get the sense distribution and print it to the output file
    for i in `seq 1 $num_test_inst`
    do
        instance_id="$word.$i"
      
        data=`head -n $i topicmodel_output/$word/topicsindocs.txt | tail -n 1 | cut -f 3- -d \ `
        if ! [ ${#data} -eq 0 ]
        then
            echo "$word $instance_id $data" >> ../$output_dir/$wsd_output
        #no data, default to topic 1
        else
            echo "$word $instance_id t.1/1.0000" >> ../$output_dir/$wsd_output
        fi
    done

    sed "s/^/$word: /g" topicmodel_output/$word/topics.txt >> ../$output_dir/$wsd_output.topics
    cp topicmodel_output/$word/topics.pickle ../$output_dir/topic_wordprob/$word.topics.pickle
done

