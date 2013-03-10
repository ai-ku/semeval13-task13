### 1.1 BIN INSTALLATION
bin:
	cd ../bin; make

### 1.2 COMMON OPTIONS
SRILM_PATH=/opt/srilm/bin/i686-m64
export PATH := ../../bin:.:${SRILM_PATH}:${PATH} # Binaries in the bin directory
SEED=1  # Random seed
NCPU=7 # Number of threads/processes to use for parallel computations
MATLAB_PATH=/mnt/opt/matlab/linux64/R2011a/bin/matlab -nojvm -nodisplay
BIN=../bin/
DATA=../data/tokenized/
### 1.3 INPUT files:
TRAIN=${DATA}train.ukwac.tok.gz # ukWaC Corpus wc=88214600 2247153469 12385653002
TEST=${DATA}test.ukwac.tok.gz  # ukWaC Test Corpus wc= 39203 998193 5509360
EVAL=../trial_data/evaluation/
GOLD=../trial_data/evaluation/keys/gold-standard/trial.gold-standard.key
BASELINE=../trial_data/evaluation/keys/baselines/

### 2.2 SRILM options:
LM_NGRAM=4# n-gram order
LM_VOCAB=100 # words seen less than this in GETTRAIN will be replaced with <unk>
LM_MTYPE=i686-m64 # architecture for compiling srilm

ukwac.split: #splitting data into training and test for perplexity calc.
	../bin/data_splitter.py

#TODO: Time ve wc'ler daha duzeltilmedi
ukwac.tokenize: ## time=1h30m, wc=88214600 2247153469 12385653002
	tokenize.py

trial.all.gz: trial.gz trial.ngram.gz trial.gold.gz trial.pos.gz trial.word.gz trial.id.gz
test.all.gz: test.gz test.ngram.gz test.pos.gz test.word.gz test.id.gz 
	
%.tok.gz: ../%_data
	#tokenize method trial.tok.gz test.tok.gz
	# method tokenize diye duzeltmek gerekiyor.
	../bin/$*_data_parser.py | gzip > $@


#TODO prepare.% #training/test
%.gz: ../%_data
	#parse method
	../bin/$*_data_parser.py | gzip > $@

%.ngram.gz: %.gz
	zcat $< | cut -f2 | gzip > $@

trial.gold.gz: ../trial_data/evaluation/keys/gold-standard/trial.gold-standard.key
	#zcat $< | cut -f3 | gzip > $@
	cat $< | gzip > $@

# number of cluster, k
trial.k.gz: ../trial_data
	cat ${BASELINE}all-senses.key | awk '{if (NR % 50 == 1) print $$1"\t"NF-2;}' | gzip  > $@

%.pos.gz: %.gz
	zcat $< | perl -lane 'print $$F[2]' | gzip > $@
	
%.target.gz: %.gz
	zcat $< | perl -lane 'print $$F[3]' | gzip > $@

%.word.gz: %.gz
	zcat $< | perl -lane 'print $$F[1]' | gzip > $@

%.id.gz: %.gz
	zcat $< | perl -lane 'print $$F[1]," ", $$F[0]' | gzip > $@

%.vocab.gz: ${DATA}%.tok.gz  ## LM_VOCAB=100: time=2219s wc=672335 672009 5983977
	#awk '{if ($2 >= 20) {print $0}}' | gzip > $@
	zcat $< | ngram-count -write-order 1 -text - -write - | \
	awk '{if ($$2 >= ${LM_VOCAB}) {print $1}}' | gzip > $@ 
	#zcat $< | ngram-count -write-order 1 -text - -write - | \
	#perl -lane 'print $$F[0] if $$F[1] >= ${LM_VOCAB}' | gzip > $@

ukwac.lm.gz: ukwac.vocab.gz ${TRAIN}
	zcat ${TRAIN} | ngram-count -order ${LM_NGRAM} -kndiscount \
	-interpolate -unk -vocab $< -text - -lm $@

ukwac.ppl.gz: 
	#zcat $*.tok.gz | \
	#ngram -order ${LM_NGRAM} -unk -lm $< -ppl - -debug 2 | gzip > $@
	zcat ${TEST} | ngram -order ${LM_NGRAM} \
	-unk -lm ukwac.lm.gz -ppl - -debug 2 | gzip > $@

%.ppl.gz:
	#test.ppl.gz trial.ppl.gz
	zcat $*.tok.gz | ngram -order ${LM_NGRAM} \
	-unk -lm ukwac.lm.gz -ppl - -debug 2 | gzip > $@

### 2.3 FASTSUBS options:
FS_NSUB=100 # go until you have this many substitutes
FS_PSUB=1.0 # or this much cumulative probability
FS_OPTIONS=-n ${FS_NSUB} -p ${FS_PSUB}

%.sub.gz: %.ngram.gz ukwac.lm.gz  ## FS_NSUB=100 FS_PSUB=1 
	zcat $< | ../bin/fastsubs ${FS_OPTIONS} ukwac.lm.gz | grep -P '^__XX__\t' | gzip > $@

%.localize: #%.sub.gz %.word.gz
	-mkdir -p $*/word/raw/; 
	-mkdir -p $*/word/gold/
	-mkdir -p $*/pos/raw/
	-mkdir -p $*/pos/gold/
	../bin/localize.py $*

%.unk: %.vocab.gz %.tok.gz # Calculates unknown word ratio
	unknown.pl $< $*.tok.gz > $@

KNN=50
DIS=2#Manhattan

# calc distance with DIS
trial.knn.gz: trial.sub.gz
	zcat $< | ../bin/preinput.py | ../bin/dists -k ${KNN} \
	-v -d ${DIS} -p ${NCPU} 2> knn${DIS}.err | gzip > $@ 

# calc distance with all type of metrics
%.knn:
	../bin/task13.py -f calc_dists -i $* -r "*"

#make trial.word.raw_spect.wkmeans
#make trial.word.raw.wkmeans
%.wkmeans:
	../bin/task13.py -f run_wkmeans -i $* -r "*"

%.spectral:
	../bin/task13.py -f run_spectral -i $* -r "*" > $@ 2> $@.err

### WORDSUB ###
WORDSUB=12 # Number of random substitutes per word

%.prewordsub.gz: #%.sub.gz %.target.gz
	#-mkdir $*/word/subs/
	# call: trial.prewordsub.gz
	../bin/pre_wordsub.py $*.sub.gz $*.target.gz  | gzip > $@
%.wordsub:
	../bin/task13.py -f run_wordsub -i $* -r "*" --nsubs=${WORDSUB} 2> $@.err

### SCODE ###

# trial.word.wordsubs.scode
%.scode:
	../bin/task13.py -f run_scode -i $* -r "*"  #> $@ 2> $@.err

# wordsub -> scode -> kmeans ->  mapping
trial.word.%.scode.ans: trial/word/ans/%.scode.ans trial/word/scode/%.scode.gz trial/word/wordsubs/%.pairs.gz
	../bin/calc_clust.py $< trial/word/scode/$*.scode.gz \
	trial/word/wordsubs/$*.pairs.gz 1 ${WORDSUB} | ../bin/evaluate.py \
	-g trial/word/gold/$*.gold -m 1 > eval/4/$*.ans

### EXPERIMENTS ###

# trial.exp4
trial.exp%.evaluation: eval/
	-mkdir eval/$*/
	-rm -rf eval/$*/*
	for fname in $(shell find trial/word/ans/ -name "*.ans"); do \
		ff=$$(echo $${fname}| sed 's/\//./g' | sed 's/ans.//'); \
		make $${ff}; \
	done

### EVALUATIONS ###

ungraded.%.gold:
	-mkdir -p $*/pos/ungraded_gold
	-mkdir -p $*/word/ungraded_gold
	for i in $*/word/gold/ $*/pos/gold/; do \
		../bin/ung_gold.py $$i; \
	done


EARG=--no-remapping
%.key: baselines/
	java -jar ${EVAL}supervised/gk-gamma.jar ${GOLD} ${BASELINE}$@ > baselines/$*.sup.gkgamma.eval
	java -jar ${EVAL}supervised/jaccard-index.jar ${EARG} ${GOLD} ${BASELINE}$@ > baselines/$*.sup.ji.eval
	java -jar ${EVAL}supervised/weighted-ndcg.jar ${EARG} ${GOLD} ${BASELINE}$@ >  baselines/$*.sup.wndcg.eval
	java -jar ${EVAL}supervised/weighted-tau.jar ${EARG} ${GOLD} ${BASELINE}$@ > baselines/$*.sup.wtau.eval
	#unsupervised
	#java -jar ${EVAL}unsupervised/fuzzy-b-cubed.jar ${GOLD} ${BASELINE}$@ > baselines/$*.uns.fbcubed.eval
	#java -jar ${EVAL}unsupervised/fuzzy-nmi.jar ${GOLD} ${BASELINE}$@ > baselines/$*.uns.fnmi.eval
	#java -jar ${EVAL}unsupervised/vmeasure.jar ${GOLD} ${BASELINE}$@  all > baselines/$*.uns.vm.eval
	#java -jar ${EVAL}unsupervised/fscore.jar ${GOLD} ${BASELINE}$@ all > baselines/$*.uns.fs.eval
	tail -n 2 baselines/$*.*.eval > baselines/$*.scores
	#rm -rf baselines/*.eval


%.ans:
	#supervised:
	java -jar ${EVAL}supervised/gk-gamma.jar ${GOLD} eval/$@ > eval/$*.sup.gkgamma.eval
	java -jar ${EVAL}supervised/jaccard-index.jar ${GOLD}  eval/$@ > eval/$*.sup.ji.eval
	java -jar ${EVAL}supervised/weighted-ndcg.jar ${GOLD}  eval/$@ >  eval/$*.sup.wndcg.eval
	java -jar ${EVAL}supervised/weighted-tau.jar ${GOLD}  eval/$@ > eval/$*.sup.wtau.eval
	#unsupervised
	#java -jar ${EVAL}unsupervised/fuzzy-b-cubed.jar ${GOLD} eval/$@ > eval/$*.uns.fbcubed.eval
	#java -jar ${EVAL}unsupervised/fuzzy-nmi.jar ${GOLD} eval/$@ > eval/$*.uns.fnmi.eval
	#java -jar ${EVAL}unsupervised/vmeasure.jar ${GOLD} eval/$@  all > eval/$*.uns.vm.eval
	#java -jar ${EVAL}unsupervised/fscore.jar ${GOLD} eval/$@ all > eval/$*.uns.fs.eval
	tail -n 2 eval/$*.*.eval > eval/$*.scores
	rm -rf eval/*.eval


# CLEANING

%.gz.clean:
	rm -rf $*.gz $*.word.gz $*.id.gz $*.pos.gz $*.ngram.gz $*.gold.gz

%.clean: %/
	rm -rf $*/pos/gold/*
	rm -rf $*/pos/raw/*
	rm -rf $*/pos/ungraded_gold/*
	rm -rf $*/word/gold/*
	rm -rf $*/word/raw/*
	rm -rf $*/word/ungraded_gold/*

