SRILM_PATH=/opt/srilm/bin/i686-m64
export PATH := ${PATH}:/work/_upos_new/bin:${SRILM_PATH}

TRAIN1=$(shell ls ../data/UKWAC-* | sort -k 2 -t - -n | head -5 | tail -5)
TRAIN2=$(shell ls ../data/UKWAC-* | sort -k 2 -t - -n | head -10 | tail -5)
TRAIN3=$(shell ls ../data/UKWAC-* | sort -k 2 -t - -n | head -15 | tail -5)
TRAIN4=$(shell ls ../data/UKWAC-* | sort -k 2 -t - -n | head -20 | tail -5)
TRAIN5=$(shell ls ../data/UKWAC-* | sort -k 2 -t - -n | head -25 | tail -5)
TRIAL=../data/trial.xml
TRIAL_WORDS=$(shell awk '{printf("%s.xml\n", $$1)}' ../data/baselines/mfs.key | sort -u)
TEST=$(shell find ../test_data/contexts/ -name "*.xml" | sort)

SEED=1
GOLD_ALL=../test_data/keys/gold/all.key
GOLD_SINGLE=../test_data/keys/gold/all.singlesense.key

# train.tok.gz train.pos.gz train.lemma.gz: ${TRAIN1} ${TRAIN2} ${TRAIN3} ${TRAIN4} ${TRAIN5}
# 	zcat ${TRAIN1} | perl -pe 's/[^ -~\s]+/\<uni\>/g' | extract-train.py 1 &\
# 	zcat ${TRAIN2} | perl -pe 's/[^ -~\s]+/\<uni\>/g' | extract-train.py 2 &\
# 	zcat ${TRAIN3} | perl -pe 's/[^ -~\s]+/\<uni\>/g' | extract-train.py 3 &\
# 	zcat ${TRAIN4} | perl -pe 's/[^ -~\s]+/\<uni\>/g' | extract-train.py 4 &\
# 	zcat ${TRAIN5} | perl -pe 's/[^ -~\s]+/\<uni\>/g' | extract-train.py 5 &\
# 	wait
# 	zcat tok*.gz | gzip > train.tok.gz &\
# 	zcat pos*.gz | gzip > train.pos.gz &\
# 	zcat lemma*.gz | gzip > train.lemma.gz &\
# 	wait
#	rm tok*.gz pos*.gz lemma*.gz

tok1.gz tok2.gz tok3.gz tok4.gz tok5.gz pos1.gz pos2.gz pos3.gz pos4.gz pos5.gz lemma1.gz lemma2.gz lemma3.gz lemma4.gz lemma5.gz: ${TRAIN1} ${TRAIN2} ${TRAIN3} ${TRAIN4} ${TRAIN5}
	zcat ${TRAIN1} | perl -pe 's/[^ -~\s]+/\<uni\>/g' | ./extract-train.py 1 &\
	zcat ${TRAIN2} | perl -pe 's/[^ -~\s]+/\<uni\>/g' | ./extract-train.py 2 &\
	zcat ${TRAIN3} | perl -pe 's/[^ -~\s]+/\<uni\>/g' | ./extract-train.py 3 &\
	zcat ${TRAIN4} | perl -pe 's/[^ -~\s]+/\<uni\>/g' | ./extract-train.py 4 &\
	zcat ${TRAIN5} | perl -pe 's/[^ -~\s]+/\<uni\>/g' | ./extract-train.py 5 &\
	wait

train.tok.gz train.pos.gz train.lemma.gz: tok1.gz tok2.gz tok3.gz tok4.gz tok5.gz pos1.gz pos2.gz pos3.gz pos4.gz pos5.gz lemma1.gz lemma2.gz lemma3.gz lemma4.gz lemma5.gz
	zcat tok*.gz | gzip > train.tok.gz
	zcat pos*.gz | gzip > train.pos.gz
	zcat lemma*.gz | gzip > train.lemma.gz

LM_NGRAM=4  # n-gram order
LM_VOCAB=400 # words seen less than this in GETTRAIN will be replaced with <unk>

train.vocab-all.gz: train.tok.gz
	zcat $< | awk 'length($$0) < 1001' | \
	ngram-count -write-order 1 -text - -write - | gzip > $@

train.vocab.gz: train.vocab-all.gz
	zcat $< | awk '{if ($$2 >= ${LM_VOCAB}) print $$1}' | gzip > $@
	zcat $@ | wc -l

train.lm.gz: train.tok.gz train.vocab.gz
	zcat $< | awk 'length($$0) < 1001' | \
	ngram-count -order ${LM_NGRAM} -kndiscount -interpolate -unk -vocab train.vocab.gz -text - -lm $@

trial.tok.gz: extract-test.py
	extract-test.py ${TRAIL} | gzip > $@

test.tok.gz: extract-test.py
	extract-test.py EST} | gzip > $@

trial.ppl.gz: train.lm.gz trial.tok.gz
	PATH=../bin/tree-tagger/cmd:../bin/tree-tagger/bin:$$PATH;\
	zcat trial.tok.gz | awk '{print $$0, "</s>"}' |\
	../bin/tree-tagger/cmd/tree-tagger-english | token2sent.py |\
	ngram -order ${LM_NGRAM} -unk -lm $< -ppl - -debug 2 | gzip > $@

test.ppl.gz: train.lm.gz test.tok.gz
	PATH=../bin/tree-tagger/cmd:../bin/tree-tagger/bin:$$PATH;\
	zcat test.tok.gz | awk '{print $$0, "</s>"}' |\
	../bin/tree-tagger/cmd/tree-tagger-english | token2sent.py |\
	ngram -order ${LM_NGRAM} -unk -lm $< -ppl - -debug 2 | gzip > $@

train.context.gz: train.tok.gz train.pos.gz train.lemma.gz
	extract-train-context.py $^ ${TEST} ${TRIAL_WORDS} | gzip > $@

trial.context.gz: extract-trial-context.py
	PATH=../bin/tree-tagger/cmd:../bin/tree-tagger/bin:$$PATH;\
	extract-trial-context.py ${TRIAL} | awk '{print $$0, "</s>"}' |\
	../bin/tree-tagger/cmd/tree-tagger-english | token2sent.py |\
	merge-left-right-context.py | gzip > $@

test.context.gz: extract-test-context.py
	PATH=../bin/tree-tagger/cmd:../bin/tree-tagger/bin:$$PATH;\
	extract-test-context.py ${TEST} | awk '{print $$0, "</s>"}' |\
	../bin/tree-tagger/cmd/tree-tagger-english | token2sent.py |\
	merge-left-right-context.py | gzip > $@

random.context.gz: train.context.gz
	zcat $< | sample-contexts.py 20000 | gzip > $@

FS_NSUB=100 # go until you have this many substitutes
FS_PSUB=1.0 # or this much cumulative probability
FS_OPTIONS=-n ${FS_NSUB} -p ${FS_PSUB}
# all.sub.gz: train.lm.gz train.context.gz trial.context.gz test.context.gz
# 	zcat train.context.gz trial.context.gz test.context.gz |\
# 	fastsubs ${FS_OPTIONS} train.lm.gz | gzip > $@

all.sub.1.gz all.sub.2.gz all.sub.3.gz all.sub.4.gz: train.lm.gz random.context.gz trial.context.gz test.context.gz
	zcat random.context.gz trial.context.gz test.context.gz |\
	tail -n +000001 | head -250000 |\
	fastsubs ${FS_OPTIONS} train.lm.gz | gzip > all.sub.1.gz &\
	zcat random.context.gz trial.context.gz test.context.gz |\
	tail -n +250001 | head -250000 |\
	fastsubs ${FS_OPTIONS} train.lm.gz | gzip > all.sub.2.gz &\
	zcat random.context.gz trial.context.gz test.context.gz |\
	tail -n +500001 | head -250000 |\
	fastsubs ${FS_OPTIONS} train.lm.gz | gzip > all.sub.3.gz &\
	zcat random.context.gz trial.context.gz test.context.gz |\
	tail -n +750001 |\
	fastsubs ${FS_OPTIONS} train.lm.gz | gzip > all.sub.4.gz &\
	wait

noksan.sub.gz: random.noksan.context.gz
	zcat $< | fastsubs ${FS_OPTIONS} train.lm.gz | grep -P '^<\w+\.\w+' |  gzip > $@

target.sub.gz: all.sub.1.gz all.sub.2.gz all.sub.3.gz all.sub.4.gz
	zcat $^ | grep -P '^<\w+\.\w+' | gzip > $@

pairs.100.gz: target.sub.gz
	perl -le 'print "$<" for 1..100' | xargs zcat | wordsub -s ${SEED} | gzip > $@

noksan.pairs.100.gz: noksan.sub.gz
	perl -le 'print "$<" for 1..100' | xargs zcat | wordsub -s ${SEED} | gzip > $@

# SC_OPTIONS=-a -r 1 -d 25 -z 0.166 -p 50 -u 0.2 -s ${SEED} -v
# #KM_OPTIONS=-k 7 -r 128 -l -w -v -s ${SEED}

# %.scode.gz: pairs.100.gz
# 	zcat $< | grep -P '^<$*' | scode -i 50 ${SC_OPTIONS} | gzip > $@

# %.kmeans.gz: %.scode.gz
# 	zcat $< | perl -ne 'print if s/^1://' | wkmeans ${KM_OPTIONS} | gzip > $@

# out.key: pairs.100.gz
# 	for f in add.v argument.n ask.v different.a important.a interest.n paper.n win.v;\
# 	do make $$f.kmeans.gz & done; wait;\
# 	for f in add.v argument.n ask.v different.a important.a interest.n paper.n win.v;\
# 	do zcat $< | grep -P '<'$$f'.[^\d]' | find-sense.py $$f.kmeans.gz >> $@; done

KM_OPTIONS=-r 128 -l -w -v -s ${SEED}
out2.key: pairs.100.gz
	zcat $< | grep -P '^<add.v' | scode -i 50 ${SC_OPTIONS} | perl -ne 'print if s/^0://' | wkmeans ${KM_OPTIONS} -k 6 | gzip > km1.gz &\
	zcat $< | grep -P '^<ask.v' | scode -i 50 ${SC_OPTIONS} | perl -ne 'print if s/^0://' | wkmeans ${KM_OPTIONS} -k 7 | gzip > km2.gz &\
	zcat $< | grep -P '^<win.v' | scode -i 50 ${SC_OPTIONS} | perl -ne 'print if s/^0://' | wkmeans ${KM_OPTIONS} -k 4 | gzip > km3.gz &\
	zcat $< | grep -P '^<argument.n' | scode -i 50 ${SC_OPTIONS} | perl -ne 'print if s/^0://' | wkmeans ${KM_OPTIONS} -k 7 | gzip > km4.gz &\
	zcat $< | grep -P '^<interest.n' | scode -i 50 ${SC_OPTIONS} | perl -ne 'print if s/^0://' | wkmeans ${KM_OPTIONS} -k 7 | gzip > km5.gz &\
	zcat $< | grep -P '^<paper.n' | scode -i 50 ${SC_OPTIONS} | perl -ne 'print if s/^0://' | wkmeans ${KM_OPTIONS} -k 7 | gzip > km6.gz &\
	zcat $< | grep -P '^<different.[aj]' | scode -i 50 ${SC_OPTIONS} | perl -ne 'print if s/^0://' | wkmeans ${KM_OPTIONS} -k 5 | gzip > km7.gz &\
	zcat $< | grep -P '^<important.[aj]' | scode -i 50 ${SC_OPTIONS} | perl -ne 'print if s/^0://' | wkmeans ${KM_OPTIONS} -k 5 | gzip > km8.gz &\
	wait
	zcat km1.gz | grep -P '^<add.v.[^\d]' | sed 's/^<add.v.\(.*\)>\s\(.*\)/add.v \1 \2\/1/g' >> $@
	zcat km2.gz | grep -P '^<ask.v.[^\d]' | sed 's/^<ask.v.\(.*\)>\s\(.*\)/ask.v \1 \2\/1/g' >> $@
	zcat km3.gz | grep -P '^<win.v.[^\d]' | sed 's/^<win.v.\(.*\)>\s\(.*\)/win.v \1 \2\/1/g' >> $@
	zcat km4.gz | grep -P '^<argument.n.[^\d]' | sed 's/^<argument.n.\(.*\)>\s\(.*\)/argument.n \1 \2\/1/g' >> $@
	zcat km5.gz | grep -P '^<interest.n.[^\d]' | sed 's/^<interest.n.\(.*\)>\s\(.*\)/interest.n \1 \2\/1/g' >> $@
	zcat km6.gz | grep -P '^<paper.n.[^\d]' | sed 's/^<paper.n.\(.*\)>\s\(.*\)/paper.n \1 \2\/1/g' >> $@
	zcat km7.gz | grep -P '^<different.a.[^\d]' | sed 's/^<different.a.\(.*\)>\s\(.*\)/different.a \1 \2\/1/g' >> $@
	zcat km8.gz | grep -P '^<important.a.[^\d]' | sed 's/^<important.a.\(.*\)>\s\(.*\)/important.a \1 \2\/1/g' >> $@

out.key: pairs.100.gz
	zcat $< | grep -P '^<add.v' | scode -i 50 ${SC_OPTIONS} | perl -ne 'print if s/^1://' | wkmeans ${KM_OPTIONS} -k 6 | gzip > km1.gz &\
	zcat $< | grep -P '^<ask.v' | scode -i 50 ${SC_OPTIONS} | perl -ne 'print if s/^1://' | wkmeans ${KM_OPTIONS} -k 7 | gzip > km2.gz &\
	zcat $< | grep -P '^<win.v' | scode -i 50 ${SC_OPTIONS} | perl -ne 'print if s/^1://' | wkmeans ${KM_OPTIONS} -k 4 | gzip > km3.gz &\
	zcat $< | grep -P '^<argument.n' | scode -i 50 ${SC_OPTIONS} | perl -ne 'print if s/^1://' | wkmeans ${KM_OPTIONS} -k 7 | gzip > km4.gz &\
	zcat $< | grep -P '^<interest.n' | scode -i 50 ${SC_OPTIONS} | perl -ne 'print if s/^1://' | wkmeans ${KM_OPTIONS} -k 7 | gzip > km5.gz &\
	zcat $< | grep -P '^<paper.n' | scode -i 50 ${SC_OPTIONS} | perl -ne 'print if s/^1://' | wkmeans ${KM_OPTIONS} -k 7 | gzip > km6.gz &\
	zcat $< | grep -P '^<different.[aj]' | scode -i 50 ${SC_OPTIONS} | perl -ne 'print if s/^1://' | wkmeans ${KM_OPTIONS} -k 5 | gzip > km7.gz &\
	zcat $< | grep -P '^<important.[aj]' | scode -i 50 ${SC_OPTIONS} | perl -ne 'print if s/^1://' | wkmeans ${KM_OPTIONS} -k 5 | gzip > km8.gz &\
	wait
	zcat $< | grep -P '^<add.v.[^\d]' | find-sense.py km1.gz >> $@
	zcat $< | grep -P '^<ask.v.[^\d]' | find-sense.py km2.gz >> $@
	zcat $< | grep -P '^<win.v.[^\d]' | find-sense.py km3.gz >> $@
	zcat $< | grep -P '^<argument.n.[^\d]' | find-sense.py km4.gz >> $@
	zcat $< | grep -P '^<interest.n.[^\d]' | find-sense.py km5.gz >> $@
	zcat $< | grep -P '^<paper.n.[^\d]' | find-sense.py km6.gz >> $@
	zcat $< | grep -P '^<different.a.[^\d]' | find-sense.py km7.gz >> $@
	zcat $< | grep -P '^<important.a.[^\d]' | find-sense.py km8.gz >> $@

y-gold-cluster.key: pairs.100.gz
	y-cluster.pl ${SEED} gold > $@

y-7-cluster.key: pairs.100.gz
	y-cluster.pl ${SEED} 7 > $@

x-gold-cluster.key: pairs.100.gz
	x-cluster.pl ${SEED} gold > $@

x-7-cluster.key: pairs.100.gz
	x-cluster.pl ${SEED} 7 > $@

x+y-gold-cluster.key: pairs.100.gz
	x+y-cluster.pl ${SEED} gold > $@

x+y-7-cluster.key: pairs.100.gz
	x+y-cluster.pl ${SEED} 7 > $@

sampled.tok1.gz sampled.pos1.gz: tok1.gz pos1.gz lemma1.gz sample-lines.py
	./sample-lines.py ${SEED} 120000 tok1.gz pos1.gz lemma1.gz

global.sub1.gz global.sub2.gz: # train.lm.gz
	zcat sampled.tok1.gz | tail -n +00001 | head -20000 |\
	fastsubs ${FS_OPTIONS} train.lm.gz | gzip > global.sub1.gz &\
	zcat sampled.tok1.gz | tail -n +20001 | head -20000 |\
	fastsubs ${FS_OPTIONS} train.lm.gz | gzip > global.sub2.gz &\
	wait

global.sub3.gz global.sub4.gz: #train.lm.gz
	zcat sampled.tok1.gz | tail -n +40001 | head -20000 |\
	fastsubs ${FS_OPTIONS} train.lm.gz | gzip > global.sub3.gz &\
	zcat sampled.tok1.gz | tail -n +60001 | head -20000 |\
	fastsubs ${FS_OPTIONS} train.lm.gz | gzip > global.sub4.gz &\
	wait

global.sub5.gz global.sub6.gz: #train.lm.gz
	zcat sampled.tok1.gz | tail -n +80001 | head -20000 |\
	fastsubs ${FS_OPTIONS} train.lm.gz | gzip > global.sub5.gz &\
	zcat sampled.tok1.gz | tail -n +100001 | head -20000 |\
	fastsubs ${FS_OPTIONS} train.lm.gz | gzip > global.sub6.gz &\
	wait

global.sub.gz: global.sub1.gz global.sub2.gz global.sub3.gz global.sub4.gz global.sub5.gz global.sub6.gz
	zcat $^ | grep -v -P '^</s>' | gzip > $@

verb.sub.gz noun.sub.gz adj.sub.gz: global.sub.gz
	zcat $< | ./split-vnj.py sampled.lemma1.gz sampled.pos1.gz

verb.pairs.100.gz: verb.sub.gz
	perl -le 'print "$<" for 1..100' | xargs zcat | wordsub -s ${SEED} | gzip > $@

noun.pairs.100.gz: noun.sub.gz
	perl -le 'print "$<" for 1..100' | xargs zcat | wordsub -s ${SEED} | gzip > $@

adj.pairs.100.gz: adj.sub.gz
	perl -le 'print "$<" for 1..100' | xargs zcat | wordsub -s ${SEED} | gzip > $@

SC_OPTIONS=-a -r 1 -d 25 -z 0.166 -p 50 -u 0.2 -s ${SEED} -v
KM_OPTIONS=-k 32 -r 128 -l -w -v -s ${SEED}
.SECONDARY:
%.scode.gz: %.pairs.100.gz
	zcat $< | scode -i 50 ${SC_OPTIONS} | gzip > $@

# k=100	total	100	90.71
# k=200	total	200	91.09
# k=400	total	400	91.23
%.kmeans.gz: %.scode.gz
	zcat $< | perl -ne 'print if s/^1://' | wkmeans ${KM_OPTIONS} | gzip > $@

%.all.key: %.all.pairs.100.gz %.all.kmeans.gz sense-find.py
	# adj.all.key, noun.all.key, verb.all.key
	zcat $< | grep -P "^<\w+\.\w+\.\d+>" | ./sense-find.py $*.all.kmeans.gz > $@

out3.key: pairs.100.gz
	zcat $< | grep -P '^<add.v.[^\d]' | find-sense-unk.py verb.kmeans.gz > $@
	zcat $< | grep -P '^<ask.v.[^\d]' | find-sense-unk.py verb.kmeans.gz >> $@
	zcat $< | grep -P '^<win.v.[^\d]' | find-sense-unk.py verb.kmeans.gz >> $@
	zcat $< | grep -P '^<argument.n.[^\d]' | find-sense-unk.py noun.kmeans.gz >> $@
	zcat $< | grep -P '^<interest.n.[^\d]' | find-sense-unk.py noun.kmeans.gz >> $@
	zcat $< | grep -P '^<paper.n.[^\d]' | find-sense-unk.py noun.kmeans.gz >> $@
	zcat $< | grep -P '^<different.a.[^\d]' | find-sense-unk.py adj.kmeans.gz >> $@
	zcat $< | grep -P '^<important.a.[^\d]' | find-sense-unk.py adj.kmeans.gz >> $@

y-%-cluster-test.key: pairs.100.gz
	y-cluster-test.pl ${SEED} $* > $@

pos-cluster-test: adj.all.scode.gz noun.all.scode.gz verb.all.scode.gz
	-mkdir kmeans
	-mkdir keys
	./y-cluster-pos-test.py ${SEED} 32 64 128 256

#variance test:
%.var:
	./variance.pl $* > $@

%.var.plot-context: %.var
	./var-prep-plot-context.py $* /scratch/1/obaskaya/task13/test_data/keys/gold > $@

# context-based variance test
pos.variance.test-context: noun.var.plot-context verb.var.plot-context adj.var.plot-context
	tar -cvf var-test.context.tar *.var.plot-context
	mv var-test.context.tar ~

%.var.plot-word: %.var
	./var-prep-plot-word.py $* /scratch/1/obaskaya/task13/test_data/keys/gold > $@

# word-based variance test
pos.variance.test-word: noun.var.plot-word verb.var.plot-word adj.var.plot-word
	tar -cvf var-test.word.tar *.var.plot-word
	mv var-test.word.tar ~

### HDP Experiments ###
test.pairs.gz: #pairs.100.gz
	zcat $< | grep -P "^<\w+\..\.\d{1,3}>" | gzip > $@

TEST_WORDS=$(shell ls ../test_data/contexts | sed 's/.xml//g' | sort)
NSAMPLE=1000
hdp-input-create: test.pairs.gz #target.sub.gz
	python wordsub-collect.py $< ${SEED} ${NSAMPLE} ${TEST_WORDS}

# Data sampling bug'undan dolayi.
noksan.hdp-input-create: test.pairs.gz #target.sub.gz
	python wordsub-collect.py $< ${SEED} ${NSAMPLE} book.n trace.n

# main experiment target
#hdp.exp-%: hdp-wsi/run_wsi.sh ./hdp-topics-stat.py
	#cd hdp-wsi/; ./run_wsi.sh; wait
	#cp hdp-wsi/wsi_output/tm_wsi eval/$@.ans
	#cp hdp-wsi/wsi_output/tm_wsi.topics eval/$@.topics
	#./hdp-topics-stat.py $@.ans > eval/$@.dist
	#wait

# parameter optimization
hdp.exp-alpha-%: hdp-wsi/run_wsi.sh ./hdp-topics-stat.py
	cd hdp-wsi/; ./run_wsi.sh $*; wait
	cp hdp-wsi/wsi_output/tm_wsi eval/$@.ans
	cp hdp-wsi/wsi_output/tm_wsi.topics eval/$@.topics
	./hdp-topics-stat.py $@.ans > eval/$@.dist
	wait

### Evaluation ###
#echo "hdp-1 hdp-2 hdp-3" | xargs -n 1 | perl -lne 'm/hdp-(.*)/; print $1'
EVAL=../test_data/scoring/
eval.%: eval/%.ans
	java -jar ${EVAL}jaccard-index.jar ${GOLD_ALL} $< > eval/$*.sup.ji.eval
	java -jar ${EVAL}positional-tau.jar ${GOLD_ALL} $< > eval/$*.sup.pt.eval
	java -jar ${EVAL}weighted-ndcg.jar ${GOLD_ALL} $< > eval/$*.sup.wndcg.eval
	java -jar ${EVAL}single-sense-precision.jar ${GOLD_SINGLE} $< > eval/$*.sup.ssp.eval
	java -jar ${EVAL}fuzzy-bcubed.jar ${GOLD_ALL} $< > eval/$*.un.fb.eval
	java -jar ${EVAL}fuzzy-nmi.jar ${GOLD_ALL} $< > eval/$*.un.fnmi.eval
	tail -n 2 eval/$*.*.eval > eval/$*.scores
	rm -rf eval/*.eval





