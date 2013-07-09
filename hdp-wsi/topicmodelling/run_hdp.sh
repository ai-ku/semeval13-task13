
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
max_iter=3
seed=1373367764

#run hdp
#compile the code
cd hdp
make
cd ..

files=`find topicmodel_output/ -type d | grep "/*.[vnj]"`
num_files=`find topicmodel_output/ -type d | grep "/*.[vnj]" | wc -l `

echo ---------------------
echo Number of files: $num_files
echo ---------------------

for output_dir in $files
do
./hdp/hdp --algorithm train --data $output_dir/hdpdata.train.txt --directory $output_dir \
--max_iter $max_iter --save_lag -1 --gamma_b $gamma_b --alpha_b $alpha_b --random_seed $seed &
done
wait

echo ------Start----------
echo "hdp output ->> output"
echo ---------------------

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

echo ------Finish----------
echo "hdp output ->> output"
echo ---------------------
